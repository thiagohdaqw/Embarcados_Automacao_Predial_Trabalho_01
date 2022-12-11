import pathlib
import re
import os

PAGES_PATH = pathlib.Path(os.path.dirname(__file__)) / 'pages/'
ROOT_PAGE = 'index.html'
VALIDATION_REGEX = r'[a-z]+\.(css|html|js)'


def handle_get_method(data: str) -> bytes:
    _, filename, _ = data.split(' ', 3)

    filename = ROOT_PAGE if filename == '/' else filename[1:]

    if not validate_filename(filename):
        return build_error_response()

    return build_response_from_file(b'200', filename)


def build_response_from_file(status_code, filename):
    response = b'HTTP/1.1 ' + status_code + b'\n'
    response += b'Content-Type: text/html; charset=utf-8\n'
    response += b'Connection: Closed\n\n'

    with open(PAGES_PATH / filename, 'rb') as file:
        response += file.read()

    return response


def build_error_response():
    return build_response_from_file(b'404', 'notfound.html')


def validate_filename(filename):
    if not re.fullmatch(VALIDATION_REGEX, filename):
        return False

    if not (PAGES_PATH / filename).is_file():
        return False

    return True
