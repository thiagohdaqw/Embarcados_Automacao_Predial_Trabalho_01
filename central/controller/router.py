from .http import HttpMethod, handle_http_get_static_file
from typing import Callable
from central.server.server import Server

HttpHandler = Callable[[str], bytes]


class HttpRouter:

    routes: dict[tuple[str, str], HttpHandler]

    server: Server

    def __init__(self, server: Server):
        self.routes = {}
        self.server = server

        self.register_route(HttpMethod.GET, '*', handle_http_get_static_file)

    def register_route(self, method: HttpMethod, path: str, callback: HttpHandler):
        self.routes[(method.value, path)] = callback

    def handle_http_message(self, data: bytes) -> bytes:
        method, resource, request = data.decode('utf-8').split(' ', 2)

        if (method, resource) in self.routes:
            return self.routes[(method, resource)](request)

        return self.routes[(HttpMethod.GET.value, '*')](resource)
