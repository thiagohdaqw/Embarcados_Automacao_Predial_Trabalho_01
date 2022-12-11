import select
from enum import Enum
from queue import Queue
from typing import List, Callable
from collections import namedtuple
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket

class Message(Enum):
    DIRECT = 0
    BROADCAST = 1

Address = namedtuple('Address', 'ip port')
MessageQueue = Queue[tuple[Message, bytes]]
ReadableHandler = Callable[[socket, MessageQueue], None]

class DistributedServerConnector:
    
    clients: set[socket]
    outputs: set[socket]

    readable_funcs = List[ReadableHandler]

    message_queues: dict[socket, MessageQueue]

    def __init__(self):
        self.clients = set()
        self.outputs = set()
        self.readable_funcs = []
        self.writeable_funcs = []
        self.message_queues = {}

    def serve(self):
        while True:
            readables, writeables, _ = select.select(self.clients, self.outputs, [])

            for r in readables:
                for readable_func in self.readable_funcs:
                    readable_func(r, self.message_queues[r])

                if not self.message_queues[r].empty():
                    self.outputs.add(r)

            for w in writeables:
                self.send_message(w)

    def send_message(self, conn: socket):
        if self.message_queues[conn].empty():
            return

        type, message = self.message_queues[conn].get_nowait()

        if type == Message.DIRECT:
            self.send_direct_message(conn, message)
        if type == Message.BROADCAST:
            self.send_broadcast_message(message)

        if self.message_queues[conn].empty():
            self.outputs.remove(conn)

    def send_direct_message(self, conn: socket, message: bytes):
        conn.sendall(message)

    def send_broadcast_message(self, message: bytes):
        for conn in self.clients:
            conn.sendall(message)

    def register_readable_handler(self, func: ReadableHandler):
        self.readable_funcs.append(func)

    def connect(self, address: Address):
        client_socket = socket(AF_INET, SOCK_STREAM)
        
        try:
            print(f"[{address}]: Tentando se conectar")

            client_socket.connect(address)
            client_socket.setblocking(False)

            self.clients.add(client_socket)
            self.message_queues[client_socket] = Queue()
            
            print(f"[{address}]: Conexão estabelecida com sucesso")
        except OSError:
            print(f"[{address}]: Falha em estabelecer conexão")
            client_socket.close()
