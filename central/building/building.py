
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

    def __init__(self):
        self.rooms = {}
        self.connectionsRooms = {}
        self.temperature = -273.15
        self.humidity = 0
        self.alarm_system = False
        self.alarm = False
        self.persons = 0

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

        for key, value in kwargs.items():
            setattr(room, key, value)

        self.update_averages()
        self.update_persons()

        self.alarm |= kwargs.get('alarm', self.alarm)

    def update_averages(self):
        temperatures = list(map(lambda r: r.temperature, filter(lambda r: r.temperature is not None, self.rooms.values())))
        humidities = list(map(lambda r: r.humidity, filter(lambda r: r.humidity is not None, self.rooms.values())))

        if humidities:
            self.humidity = mean(humidities)
        if temperatures:
            self.temperature = mean(temperatures)

    def update_persons(self):
        self.persons = sum(room.persons for room in self.rooms.values())

    def disable_alarm_system(self):
        self.alarm_system = False
        self.alarm = False

        rooms_with_alarm_on = filter(lambda room: room.online and room.alarm, self.rooms.values())
        rooms_connections = map(lambda room: room.connection, rooms_with_alarm_on)

        distributed_server_producer.send_broadcast_message(
            rooms_connections,
            {
                'type': CommandType.RELAY.value,
                'sensor_name': 'alarm',
                'value': False
            }
        )

    def enable_alarm_system(self):
        sensors_must_be_off = ['presence', 'door', 'window', 'smoke', 'alarm']
        sensors = dict()

        for room in self.rooms.values():
            for sensor in sensors_must_be_off:
                if getattr(room, sensor):
                    sensors[room.name] = sensors.get(room.name, [])
                    sensors[room.name].append(sensor)
        
        if not sensors:
            self.alarm_system = True

        return sensors        

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

    def asdict(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'alarm_system': self.alarm_system,
            'alarm': self.alarm,
            'persons': self.persons,
            'rooms': [room.asdict() for room in self.rooms.values()]
        }
