import select
import threading
import util
from enum import Enum
from queue import Queue
from typing import List, Callable
from collections import namedtuple
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket


class MessageType(Enum):
    DIRECT = 0
    BROADCAST = 1


class HttpMethod(Enum):
    GET = 'GET'


Address = namedtuple('Address', 'host port')
MessageQueue = Queue[tuple[MessageType, bytes]]

ReadableHandler = Callable[[bytes, MessageQueue], None]
HttpHandler = Callable[[str], bytes]


class Server:

    server: socket
    server_address: Address

    clients: dict[Address, socket]

    inputs: set[socket]
    outputs: set[socket]

    readable_funcs = List[ReadableHandler]
    http_funcs = dict[HttpMethod, HttpHandler]

    message_queues: dict[socket, MessageQueue]

    timeout: float

    def __init__(self, server_address: Address, timeout=5.0):
        self.clients = {}
        self.outputs = set()
        self.inputs = set()
        self.readable_funcs = []
        self.writeable_funcs = []
        self.message_queues = {}
        self.http_funcs = {}
        self.timeout = timeout

        self._init_server(server_address)

    def serve(self):
        while True:
            self.reconnect()

            readables, writeables, _ = select.select(
                self.inputs, self.outputs, [], self.timeout)

            for r in readables:
                self._manage_readable_event(r)

            for w in writeables:
                self.send_message(w)

    def send_message(self, conn: socket):
        if self.message_queues[conn].empty():
            return

        type, message = self.message_queues[conn].get_nowait()

        if type == MessageType.DIRECT:
            self.send_direct_message(conn, message)
        if type == MessageType.BROADCAST:
            self.send_broadcast_message(message)

        if self.message_queues[conn].empty():
            self.outputs.remove(conn)

    def send_direct_message(self, conn: socket, message: bytes):
        conn.sendall(message)

    def send_broadcast_message(self, message: bytes):
        for conn in self.inputs:
            conn.sendall(message)

    def register_readable_handler(self, func: ReadableHandler):
        self.readable_funcs.append(func)

    def register_http_handler(self, method: HttpMethod, func: HttpHandler):
        self.http_funcs[method] = func

    def reconnect(self):
        disconnecteds = filter(
            lambda i: i[1] not in self.inputs, self.clients.items())

        for address, _ in disconnecteds:
            self.connect(address)

    def connect(self, address: Address):
        client_socket = socket(AF_INET, SOCK_STREAM)
        self.clients[address] = client_socket

        try:
            util.logger(address, "Tentando se conectar")

            client_socket.connect(address)
            client_socket.setblocking(False)

            self.inputs.add(client_socket)
            self.message_queues[client_socket] = Queue()

            util.logger(address, "Conexão estabelecida com sucesso")
            return
        except OSError:
            util.logger(address, "Falha em estabelecer conexão")

    def disconnect(self, conn: socket):
        if conn in self.inputs:
            self.inputs.remove(conn)
        if conn in self.outputs:
            self.outputs.remove(conn)
        if conn in self.message_queues:
            del self.message_queues[conn]

        for address, connection in self.clients.items():
            if connection == conn:
                connection.close()
                util.logger(address, "Desconectado")
                return

    def _manage_readable_event(self, conn: socket):
        if conn is self.server:
            self._manage_server_readable_event()
            return

        data = conn.recv(1024)

        if not data:
            self.disconnect(conn)
            return

        for func in self.readable_funcs:
            func(data, self.message_queues[conn])

        if not self.message_queues[conn].empty():
            self.outputs.add(conn)

    def _manage_server_readable_event(self):
        conn, addr = self.server.accept()

        util.logger(Address(*addr), "Nova conexão")

        threading.Thread(target=self._handle_http_connection, args=(conn,)).start()

    def _handle_http_connection(self, conn: socket):
        with conn:
            data = conn.recv(1024)

            if not data:
                return

            text = data.decode('utf-8')

            for method in self.http_funcs.keys():
                if text.startswith(method.value + ' '):
                    response = self.http_funcs[method](text)
                    conn.sendall(response)
                    return

    def _init_server(self, address: Address):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind(address)
        self.server.setblocking(False)
        self.server.listen(10)

        self.inputs.add(self.server)

        util.logger(address, 'Servidor Central aguardando conexões...')
