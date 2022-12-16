from typing import Callable

from central.server.server import Server
from central.building.building import Building
from .http import HttpMethod, handle_http_get_static_file


HttpHandler = Callable[[str], bytes]


class HttpRouter:

    routes: dict[tuple[str, str], HttpHandler]

    server: Server

    building: Building

    def __init__(self, server: Server, building: Building):
        self.routes = {}
        self.server = server
        self.building = building

    def register_route(self, method: HttpMethod, path: str, callback: HttpHandler):
        self.routes[(method.value, path)] = callback

    def handle_http_message(self, data: bytes) -> bytes:
        method, resource, request = data.decode('utf-8').split(' ', 2)

        if (method, resource) in self.routes:
            _, body = request.split('\n\n', 1)
            return self.routes[(method, resource)](body, self.building)

        return handle_http_get_static_file(resource)
