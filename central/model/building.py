
from room import Room
from statistics import mean
from socket import socket
from collections import deque
import dataclasses


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
        self.temperature = -273.15
        self.humidity = 0
        self.alarm_system = False
        self.alarm = False

    def register_room(self, name: str, conn: socket):
        self.remove_room(conn)
        room = Room(name, online=True)
        self.rooms[name] = room
        self.connectionsRooms[conn] = room
        self.messages_queues[room] = deque()

    def disconnect_room(self, conn):
        if conn in self.connectionsRooms:
            self.connectionsRooms[conn].online = False

    def update_room(self, name, **kwargs):
        room = self.rooms[name]

        for key, value in kwargs.items():
            setattr(room, key, value)

        self.update_averages()
        self.update_persons()

    def get_room_message(self, conn):
        return self.connectionsRooms[conn].message_queue.popleft()

    def has_messages(self, conn):
        return len(self.connectionsRooms[conn].message_queue) > 0

    def update_averages(self):
        self.temperature = mean(room.temperature for room in self.rooms.values())
        self.humidity = mean(room.humidity for room in self.rooms.values())

    def update_persons(self):
        self.persons = sum(room.persons for room in self.rooms.values())

    def asdict(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'alarm_system': self.alarm_system,
            'alarm': self.alarm,
            'persons': self.persons,
            'rooms': [dataclasses.asdict(room) for room in self.rooms.values()]
        }
