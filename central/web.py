import re
import os
import json
import pathlib
import mimetypes

PAGES_PATH = pathlib.Path(os.path.dirname(__file__)) / 'pages/'
ROOT_PAGE = 'index.html'
VALIDATION_REGEX = r'[a-z]+\.(css|html|js|json)'


def handle_get_method(data: str) -> bytes:
    _, filename, *_ = data.split(' ', 3)

    filename = ROOT_PAGE if filename == '/' else filename[1:]

    if filename in DYNAMIC_ROUTES:
        return DYNAMIC_ROUTES[filename]()

    if not validate_filename(filename):
        return build_error_response()

    return build_response_from_file(filename)


def build_report_json():
    body = b'{"ola": 1}\n'
    return build_response(body, b'application/json')


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
    return response


def validate_filename(filename):
    if not re.fullmatch(VALIDATION_REGEX, filename):
        return False

    if not (PAGES_PATH / filename).is_file():
        return False

    return True


DYNAMIC_ROUTES = {
    'report.json': build_report_json
}
