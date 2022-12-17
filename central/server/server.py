import select
import threading
import logging

from socket import socket, MSG_WAITALL
from typing import List, Callable
from central.building.building import Building
from central.server.socket import Address, create_server_socket
from central.util.bytes import int_from_bytes


ReadableHandler = Callable[[bytes, str, Building], None]
HttpHandler = Callable[[bytes], bytes]

logger = logging.getLogger('console')


class Server:

    server_central: socket
    server_web:     socket

    inputs:     set[socket]

    readable_callbacks: List[ReadableHandler]
    http_callback:      HttpHandler

    building: Building

    def __init__(self, server_central: Address, server_web: Address, building: Building):
        self.building = building

        self.inputs = set()
        self.readable_callbacks = []
        self.message_queues = {}
        self.http_callbacks = {}

        self.server_central = create_server_socket(server_central)
        self.server_web = create_server_socket(server_web)

        self.inputs.add(self.server_central)
        self.inputs.add(self.server_web)

        logger.info(
            f'\033[0;33mServidor Central\033[0m aguardando conexões em: \033[0;32m{server_central.host}:{server_central.port}\033[0m',
            extra={'conn': server_central})
        logger.info(
            f'\033[0;33mServidor Web\033[0m aguardando conexões em: \033[0;32mhttp://{server_web.host}:{server_web.port}/\033[0m',
            extra={'conn': server_web})

    def serve(self):
        while True:
            readables, writeables, _ = select.select(
                self.inputs, [], [])

            for r in readables:
                self._manage_readable_event(r)

    def receive_acknowledgment(self, conn: socket):
        ack = conn.recv(1)
        return int(ack) > 0

    def register_readable_handler(self, callback: ReadableHandler):
        self.readable_callbacks.append(callback)

    def register_http_handler(self, callback: HttpHandler):
        self.http_callback = callback

    def disconnect(self, conn: socket):
        self.building.disconnect_room(conn)

        if conn in self.inputs:
            self.inputs.remove(conn)
        if conn in self.message_queues:
            del self.message_queues[conn]

        logger.info("Fechando conexão", extra={
                    'conn': Address(*conn.getsockname())})

    def _manage_readable_event(self, conn: socket):
        if conn is self.server_web:
            self._manage_server_web_readable_event()
            return
        if conn is self.server_central:
            self._manage_server_central_readable_event()
            return

        self._manage_clients_readable_event(conn)

    def _manage_clients_readable_event(self, conn: socket):
        if not (data_len := self._read_or_disconnect(conn, 4)):
            return

        if not (data := self._read_or_disconnect(conn, int_from_bytes(data_len))):
            return

        for func in self.readable_callbacks:
            func(data, self.building)

    def _manage_server_central_readable_event(self):
        conn, addr = self.server_central.accept()

        if not (data_len := self._read_or_disconnect(conn, 4)):
            return

        if not (data := self._read_or_disconnect(conn, int_from_bytes(data_len))):
            return

        name = data.decode('utf-8')

        logger.info(f"Nova conexão de Servidor Distribuido ({name})",
                    extra={'conn': Address(*addr)})

        self.building.register_room(name, conn)
        self.inputs.add(conn)

    def _manage_server_web_readable_event(self):
        conn, addr = self.server_web.accept()

        logger.info("Nova conexão Web", extra={'conn': Address(*addr)})

        threading.Thread(target=self._handle_http_connection,
                         args=(conn,)).start()

    def _handle_http_connection(self, conn: socket):
        with conn:
            data = conn.recv(1024)

            if not data:
                return

            response = self.http_callback(data)
            conn.sendall(response)

    def _read_or_disconnect(self, conn, length):
        data = conn.recv(length, MSG_WAITALL)

        if not data:
            self.disconnect(conn)
            return None

        return data
