import select
import time
from enum import Enum
from queue import Queue
from typing import List, Callable
from collections import namedtuple
from socket import AF_INET, SOCK_STREAM, socket

class MessageType(Enum):
    DIRECT = 0
    BROADCAST = 1

Address = namedtuple('Address', 'host port')
MessageQueue = Queue[tuple[MessageType, bytes]]
ReadableHandler = Callable[[bytes, MessageQueue], None]

class DistributedServerConnector:
    
    clients: dict[Address, socket]

    inputs: set[socket]
    outputs: set[socket]

    readable_funcs = List[ReadableHandler]

    message_queues: dict[socket, MessageQueue]

    timeout: float

    def __init__(self, timeout = 5.0):
        self.clients = {}
        self.outputs = set()
        self.inputs = set()
        self.readable_funcs = []
        self.writeable_funcs = []
        self.message_queues = {}
        self.timeout = timeout

    def serve(self):
        while True:
            self.reconnect()

            readables, writeables, _ = select.select(self.inputs, self.outputs, [], self.timeout)

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

    def reconnect(self):
        disconnecteds = filter(lambda i: i[1] not in self.inputs, self.clients.items())

        for address, _ in disconnecteds:
            self.connect(address)

    def connect(self, address: Address):
        client_socket = socket(AF_INET, SOCK_STREAM)
        self.clients[address] = client_socket
        
        try:
            print(f"[{address}]: Tentando se conectar")

            client_socket.connect(address)
            client_socket.setblocking(False)

            self.inputs.add(client_socket)
            self.message_queues[client_socket] = Queue()
            
            print(f"[{address}]: Conexão estabelecida com sucesso")
            return
        except OSError:
            print(f"[{address}]: Falha em estabelecer conexão")

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
                print(f"[{address}]: Desconectado")
                return

    def _manage_readable_event(self, conn: socket):
        data = conn.recv(500)

        if not data:
            self.disconnect(conn)
            return
        
        for func in self.readable_funcs:
            func(data, self.message_queues[conn])

        if not self.message_queues[conn].empty():
            self.outputs.add(conn)
