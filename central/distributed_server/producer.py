from socket import socket
from typing import Iterable
from central.util.bytes import int_to_bytes
from central.util.json import to_json


def send_direct_message(conn: socket, message: dict):
    json = to_json(message)
    conn.sendall(int_to_bytes(len(json)))
    conn.sendall(json)


def send_broadcast_message(clients: Iterable[socket], message: dict):
    for conn in clients:
        send_direct_message(conn, message)
