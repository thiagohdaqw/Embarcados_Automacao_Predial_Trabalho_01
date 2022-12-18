import os
import time
from queue import Queue
from socket import socket, MSG_WAITALL

from distributed.util.json import from_json
from distributed.util.bytes import int_from_bytes
from distributed.model.room import Room
import distributed.central.executor as executor


def consume(conn: socket, room: Room, producer_queue: Queue):
    while True:
        data_len = read_or_exit(conn, 4)
        data = read_or_exit(conn, int_from_bytes(data_len))

        command = from_json(data)

        feedback = executor.execute_command(command, room)

        if feedback:
            producer_queue.put_nowait(feedback)
            

def read_or_exit(conn, length):
    data = conn.recv(length, MSG_WAITALL)

    if not data:
        print('Connection with Central Server were lost')
        os._exit(1)

    return data