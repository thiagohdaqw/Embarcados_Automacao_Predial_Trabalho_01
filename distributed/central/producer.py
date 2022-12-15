from socket import socket
from queue import Queue
import dataclasses

from distributed.model.room import Room
from distributed.util.json import to_json
from distributed.util.bytes import int_to_bytes


def produce(conn: socket, queue: Queue[Room]):
    while True:
        room = queue.get()

        data = to_json(dataclasses.asdict(room))

        conn.sendall(int_to_bytes(len(data)))
        conn.sendall(data)
