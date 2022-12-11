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

Address = namedtuple('Address', 'ip port')
MessageQueue = Queue[tuple[MessageType, bytes]]
ReadableHandler = Callable[[bytes, MessageQueue], None]

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
        for conn in self.clients:
            conn.sendall(message)

    def register_readable_handler(self, func: ReadableHandler):
        self.readable_funcs.append(func)

    def connect(self, address: Address):
        client_socket = socket(AF_INET, SOCK_STREAM)
        
        for _ in range(10):
            try:
                print(f"[{address}]: Tentando se conectar")

                client_socket.connect(address)
                client_socket.setblocking(False)

                self.clients.add(client_socket)
                self.message_queues[client_socket] = Queue()
                
                print(f"[{address}]: Conexão estabelecida com sucesso")
                return
            except OSError:
                print(f"[{address}]: Falha em estabelecer conexão. Tentando novamente em 5 segundos...")
                time.sleep(5)

        print(f"[{address}]: Tentativas maxima de conexão alcançada")
        client_socket.close()

    def disconnect(self, conn: socket):
        if conn in self.clients:
            self.clients.remove(conn)
        if conn in self.outputs:
            self.outputs.remove(conn)
        if conn in self.message_queues:
            del self.message_queues[conn]
        print(f"[{Address(*conn.getsockname())}]: Desconectado")
        conn.close()

    def _manage_readable_event(self, conn: socket):
        data = conn.recv(500)

        if not data:
            self.disconnect(conn)
            return
        
        for func in self.readable_funcs:
            func(data, self.message_queues[conn])
