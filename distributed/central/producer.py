from socket import socket
from queue import Queue
import dataclasses

from distributed.model.room import Room
from distributed.util.json import to_json
from distributed.util.bytes import int_to_bytes


def produce(conn: socket, queue: Queue[Room | dict]):
    while True:
        data = queue.get()
        
        if isinstance(data, Room):
            data = dataclasses.asdict(data)

        send_message(conn, data)


def send_message(conn: socket, data: dict):
    body = to_json(data)
    conn.sendall(int_to_bytes(len(body)))
    conn.sendall(body)

    del data
    del body
