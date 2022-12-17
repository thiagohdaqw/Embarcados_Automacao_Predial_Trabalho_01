import logging
from statistics import mean
from socket import socket
from collections import deque

from central.building.command import CommandType
from central.model.room import Room
import central.distributed_server.producer as distributed_server_producer


logger = logging.getLogger('actions')


class Building:

    rooms: dict[str, Room]
    connectionsRooms: dict[socket, Room]

    feedbacks: list

    temperature:    float
    humidity:       int
    alarm_system:   bool
    alarm:          bool
    persons:        int
    fire:           bool

    def __init__(self):
        self.rooms = {}
        self.connectionsRooms = {}
        self.temperature = -273.15
        self.humidity = 0
        self.alarm_system = False
        self.alarm = False
        self.persons = 0
        self.fire = False
        self.feedbacks = deque()

    @property
    def online_rooms(self):
        return filter(lambda room: room.online, self.rooms.values())

    def register_room(self, name: str, conn: socket):
        room = self.rooms.get(name, Room(name, conn))
        room.online = True
        room.persons = 0
        room.connection = conn

        self.rooms[name] = room
        self.connectionsRooms[conn] = room

    def disconnect_room(self, conn):
        if conn in self.connectionsRooms:
            self.connectionsRooms[conn].online = False
            del self.connectionsRooms[conn]

    def update_room(self, name, **kwargs):
        room = self.rooms[name]

        room_smoke_old = room.smoke
        room_presence_old = room.presence

        for key, value in kwargs.items():
            setattr(room, key, value)

        self.update_averages()
        self.update_persons()

        self.check_presence(room, room_presence_old)
        self.check_fire_detection(room_smoke_old, room.smoke)
        self.check_intrusion_detection(room)

    def update_averages(self):
        temperatures = list(map(lambda r: r.temperature, filter(
            lambda r: r.temperature is not None, self.online_rooms)))
        humidities = list(map(lambda r: r.humidity, filter(
            lambda r: r.humidity is not None, self.online_rooms)))

        if humidities:
            self.humidity = mean(humidities)
        if temperatures:
            self.temperature = mean(temperatures)

    def update_persons(self):
        self.persons = sum(room.persons for room in self.online_rooms)

    def disable_alarms(self):
        rooms_with_fire = list(
            filter(lambda room: room.smoke, self.online_rooms))

        if rooms_with_fire:
            self.fire = True
            return False

        self.alarm_system = False
        self.alarm = False
        self.fire = False
        self.update_relays(False, ['alarm'])

        logger.info(',disable,alarms')
        return True

    def enable_alarm_system(self):
        sensors_must_be_off = ['presence', 'door', 'window', 'smoke', 'alarm']
        sensors = dict()

        for room in self.online_rooms:
            for sensor in sensors_must_be_off:
                if getattr(room, sensor):
                    sensors[room.name] = sensors.get(room.name, [])
                    sensors[room.name].append(sensor)

        if not sensors:
            logger.info(',enable,alarms')
            self.alarm_system = True

        return sensors

    def update_relays(self, value, relays=None):
        if not relays:
            relays = ['lamp01', 'lamp02', 'projector',
                      'air_conditioning', 'alarm']

        if self.fire and not value:
            relays.remove('alarm')

        for relay in relays:
            distributed_server_producer.send_broadcast_message(
                map(lambda room: room.connection, self.online_rooms),
                {
                    'type': CommandType.RELAY.value,
                    'relay_name': relay,
                    'value': value
                }
            )

    def update_lamps(self, value):
        lamps = ['lamp01', 'lamp02']
        self.update_relays(value, lamps)

    def toggle_room_relay(self, command):
        room = self.rooms[command['room_name']]

        if self.fire and command['relay_name'] == 'alarm':
            return None

        distributed_server_producer.send_direct_message(
            room.connection,
            {
                'type': CommandType.RELAY.value,
                'relay_name': command['relay_name'],
                'value': not getattr(room, command['relay_name'])
            }
        )

    def check_fire_detection(self, smoke_old, smoke):
        if smoke_old == False and smoke == True:
            self.fire = True
            self.activate_alarms()
            logger.info(',detected,smoke')

        if smoke_old == True and smoke == False:
            self.disable_alarms()
            logger.info(',liberated,smoke')

    def check_intrusion_detection(self, room):
        if not self.alarm_system:
            return
        
        sensors = ['door', 'presence', 'window']
        for sensor in sensors:
            if getattr(room, sensor):
                self.activate_alarms()
                logger.info(',detected,intrusion')

    def activate_alarms(self):
        self.alarm_system = True
        self.alarm = True

        rooms_without_alarm_off = filter(lambda room: not room.alarm, self.online_rooms)

        for room in rooms_without_alarm_off:
            self.update_relays(True, ['alarm'])

    def check_presence(self, room, presence_old):
        if presence_old == False and room.presence == True and not self.alarm_system:
            distributed_server_producer.send_direct_message(
                room.connection,
                {
                    'type': CommandType.PRESENCE.value,
                    'seconds': 15
                }
            )

    def add_feedback(self, message):
        logger.info(f',feedback,{message}')

        self.feedbacks.append(message)

    def get_feedbacks(self):
        feedbacks = list(self.feedbacks)
        self.feedbacks.clear()
        return feedbacks

    def asdict(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'alarm_system': self.alarm_system,
            'alarm': self.alarm,
            'persons': self.persons,
            'fire': self.fire,
            'rooms': [room.asdict() for room in self.rooms.values()],
            'feedbacks': self.get_feedbacks()
        }
