import os
import dataclasses
from queue import Queue
from typing import Union
from socket import socket

from distributed.model.room import Room
from distributed.util.json import to_json
from distributed.util.bytes import int_to_bytes


def produce(conn: socket, queue: Queue[Union[Room,dict]]):
    while True:
        data = queue.get()
        
        if isinstance(data, Room):
            data = dataclasses.asdict(data)

        send_message(conn, data)


def send_message(conn: socket, data: dict):
    try:
        body = to_json(data)
        conn.sendall(int_to_bytes(len(body)))
        conn.sendall(body)
    except (BrokenPipeError, ConnectionResetError):
        print('Connection with Central Server were lost')
        os._exit(1)
    finally:
        del data
        del body
