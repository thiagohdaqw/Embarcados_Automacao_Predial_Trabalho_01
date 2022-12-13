import os
import re
import pathlib
import mimetypes
import json
from enum import Enum


PAGES_PATH = pathlib.Path(os.path.dirname(__file__)) / '../assets/'
ROOT_PAGE = 'index.html'
VALIDATION_REGEX = r'([a-z]+/?)+\.(css|html|js|json|png)'


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'


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

def build_json_response(data):
    body = json.dumps(data).encode('utf-8')
    return build_response(body, contentType=b'application/json')

def build_response(body: bytes, contentType=b'text/html', status_code=b'200'):
    response = b'HTTP/1.1 ' + status_code + b'\n'
    response += b'Content-Type: ' + contentType + b'; charset=utf-8\n'
    response += b'Access-Control-Allow-Origin: *\n'
    response += b'Connection: Closed\n\n'
    response += body
    return response + b'\n'


def validate_filename(filename):
    if not re.fullmatch(VALIDATION_REGEX, filename):
        return False

    if not (PAGES_PATH / filename).is_file():
        return False

    return True
