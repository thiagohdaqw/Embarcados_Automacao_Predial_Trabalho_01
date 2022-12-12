import re
import os
import pathlib
import mimetypes
from enum import Enum
from typing import Callable
from central.server.server import Server

PAGES_PATH = pathlib.Path(os.path.dirname(__file__)) / '../assets/'
ROOT_PAGE = 'index.html'
VALIDATION_REGEX = r'[a-z]+\.(css|html|js|json)'

HttpHandler = Callable[[str], bytes]


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'


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
        method, resource, request = data.decode('utf-8').split(' ', 3)

        if (method, resource) in self.routes:
            return self.routes[(method, resource)](request)

        return self.routes[(HttpMethod.GET.value, '*')](resource)


def handle_http_get_static_file(resource: str) -> bytes:
    filename = ROOT_PAGE if resource == '/' else resource[1:]

    if not validate_filename(filename):
        return build_error_response()

    return build_response_from_file(filename)


def build_error_response():
    return build_response_from_file('notfound.html', b'404')


def build_response_from_file(filename, status_code=b'200'):
    path = PAGES_PATH / filename
    contentType = mimetypes.guess_type(path)[0]

    with open(path, 'rb') as file:
        return build_response(file.read(), contentType=contentType.encode('utf-8'), status_code=status_code)


def build_response(body: bytes, contentType=b'text/html', status_code=b'200'):
    response = b'HTTP/1.1 ' + status_code + b'\n'
    response += b'Content-Type: ' + contentType + b'; charset=utf-8\n'
    response += b'Connection: Closed\n\n'
    response += body
    return response + b'\n'


def validate_filename(filename):
    if not re.fullmatch(VALIDATION_REGEX, filename):
        return False

    if not (PAGES_PATH / filename).is_file():
        return False

    return True
