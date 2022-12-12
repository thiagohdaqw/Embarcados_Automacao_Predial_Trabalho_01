import select
import threading
from enum import Enum
from ..util import util
from typing import List, Callable
from collections import namedtuple, deque
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket


class MessageType(Enum):
    DIRECT = 0
    BROADCAST = 1


Address = namedtuple('Address', 'host port')
MessageQueue = deque[tuple[MessageType, bytes]]


ReadableHandler = Callable[[bytes, MessageQueue], None]
HttpHandler = Callable[[bytes], bytes]


def create_server_socket(address: Address) -> socket:
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    server.setblocking(False)
    server.listen(10)
    return server


class Server:

    server_central: socket
    server_web:     socket

    inputs:     set[socket]
    outputs:    set[socket]

    readable_callbacks: List[ReadableHandler]
    http_callback:      HttpHandler

    message_queues: dict[socket, MessageQueue]

    def __init__(self, server_central: Address, server_web: Address):
        self.outputs = set()
        self.inputs = set()
        self.readable_callbacks = []
        self.message_queues = {}
        self.http_callbacks = {}

        self.server_central = create_server_socket(server_central)
        self.server_web = create_server_socket(server_web)

        self.inputs.add(self.server_central)
        self.inputs.add(self.server_web)

        util.logger(server_web,
                    f'\033[0;33mServidor Central\033[0m aguardando conexões em: \033[0;32m{server_central.host}:{server_central.port}\033[0m')
        util.logger(server_web,
                    f'\033[0;33mServidor Web\033[0m aguardando conexões em: \033[0;32mhttp://{server_web.host}:{server_web.port}/\033[0m')

    def serve(self):
        while True:
            readables, writeables, _ = select.select(
                self.inputs, self.outputs, [])

            for r in readables:
                self._manage_readable_event(r)

            for w in writeables:
                self.send_message(w)

    def send_message(self, conn: socket):
        if len(self.message_queues[conn]) == 0:
            return

        type, message = self.message_queues[conn].popleft()

        if type == MessageType.DIRECT:
            self.send_direct_message(conn, message)
        if type == MessageType.BROADCAST:
            self.send_broadcast_message(message)

        if len(self.message_queues[conn]) == 0:
            self.outputs.remove(conn)

    def send_direct_message(self, conn: socket, message: bytes):
        conn.sendall(message)

    def send_broadcast_message(self, message: bytes):
        clients = filter(lambda c: c != self.server_central and c != self.server_web, self.inputs)
        for conn in clients:
            self.send_direct_message(conn, message)

    def register_readable_handler(self, callback: ReadableHandler):
        self.readable_callbacks.append(callback)

    def register_http_handler(self, callback: HttpHandler):
        self.http_callback = callback

    def disconnect(self, conn: socket):
        if conn in self.inputs:
            self.inputs.remove(conn)
        if conn in self.outputs:
            self.outputs.remove(conn)
        if conn in self.message_queues:
            del self.message_queues[conn]

        util.logger(Address(*conn.getsockname()), "Desconectado")

    def _manage_readable_event(self, conn: socket):
        if conn is self.server_web:
            self._manage_server_web_readable_event()
            return
        if conn is self.server_central:
            self._manage_server_central_readable_event()
            return

        self._manage_clients_readable_event(conn)

    def _manage_clients_readable_event(self, conn: socket):
        data = conn.recv(1024)

        if not data:
            self.disconnect(conn)
            return

        for func in self.readable_callbacks:
            func(data, self.message_queues[conn])

        if len(self.message_queues[conn]) > 0:
            self.outputs.add(conn)

    def _manage_server_central_readable_event(self):
        conn, addr = self.server_central.accept()

        util.logger(Address(*addr), "Nova conexão de Servidor Distribuido")

        self.inputs.add(conn)
        self.message_queues[conn] = deque()

    def _manage_server_web_readable_event(self):
        conn, addr = self.server_web.accept()

        util.logger(Address(*addr), "Nova conexão Web")

        threading.Thread(target=self._handle_http_connection,
                         args=(conn,)).start()

    def _handle_http_connection(self, conn: socket):
        with conn:
            data = conn.recv(1024)

            if not data:
                return

            response = self.http_callback(data)
            conn.sendall(response)
