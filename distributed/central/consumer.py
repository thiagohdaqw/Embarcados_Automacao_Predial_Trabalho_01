from queue import Queue
from socket import socket, MSG_WAITALL

from distributed.util.json import from_json
from distributed.util.bytes import int_from_bytes
from distributed.model.room import Room
import distributed.central.executor as executor


def consume(conn: socket, room: Room, producer_queue: Queue):
    while True:
        data_len = conn.recv(4, MSG_WAITALL)
        data = conn.recv(int_from_bytes(data_len), MSG_WAITALL)

        command = from_json(data)

        feedback = executor.execute_command(command, room)

        if feedback:
            producer_queue.put_nowait(feedback)
