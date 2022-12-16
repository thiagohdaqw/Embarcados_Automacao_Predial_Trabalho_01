
from statistics import mean
from socket import socket

from central.building.command import CommandType
from central.model.room import Room
import central.distributed_server.producer as distributed_server_producer


class Building:

    rooms: dict[str, Room]
    connectionsRooms: dict[socket, Room]

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


        for key, value in kwargs.items():
            setattr(room, key, value)

        self.update_averages()
        self.update_persons()

        self.check_fire_detection(room_smoke_old, room.smoke)

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
            self.alarm_system = True

        return sensors

    def update_relays(self, value, relays=None):
        if not relays:
            relays = ['lamp01', 'lamp02', 'projector',
                      'air_conditioning', 'alarm']

        for relay in relays:
            distributed_server_producer.send_broadcast_message(
                self.online_rooms,
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

        distributed_server_producer.send_direct_message(
            room.connection,
            {
                'type': CommandType.RELAY.value,
                'sensor_name': command['sensor_name'],
                'value': not getattr(room, command['sensor_name'])
            }
        )

    def check_fire_detection(self, smoke_old, smoke):
        if smoke_old == False and smoke == True:
            self.fire = True
            self.activate_alarms()
        if smoke_old == True and smoke == False:
            self.disable_alarms()

    def activate_alarms(self):
        self.alarm_system = True
        self.alarm = True
        self.update_relays(True, ['alarm'])

    def asdict(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'alarm_system': self.alarm_system,
            'alarm': self.alarm,
            'persons': self.persons,
            'rooms': [room.asdict() for room in self.rooms.values()]
        }
