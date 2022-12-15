from queue import Queue
from socket import socket, MSG_WAITALL

from distributed.util.json import from_json
from distributed.util.bytes import int_from_bytes


def consume(conn: socket, queue: Queue):
    while True:
        data_len = conn.recv(4, MSG_WAITALL)
        data = conn.recv(int_from_bytes(data_len), MSG_WAITALL)

        command = from_json(data)
        queue.put_nowait(command)
