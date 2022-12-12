from typing import NamedTuple
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

class Address(NamedTuple):
    host: str
    port: int

    def __str__(self):
        return f'({self.host}, {self.port})'


def create_server_socket(address: Address) -> socket:
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    server.setblocking(False)
    server.listen(10)
    return server
