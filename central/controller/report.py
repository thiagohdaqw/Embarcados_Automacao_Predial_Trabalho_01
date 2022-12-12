from .http import build_response

def get_current_report(request: str) -> bytes:
    body = b'{"ola": 1}'
    return build_response(body, 'application/json')