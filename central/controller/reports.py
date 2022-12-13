import random
from .http import build_json_response

def get_current_report(request: str) -> bytes:
    response = {
        'general': {
            'temperature': 25.6,
            'alarmSystem': True,
            'alarm': bool(random.randint(0, 1)),
        },
        'rooms': [
            {
                'name': 'Sala 01',
                'persons': 10,
                'temperature': 25.1,
                'smoke': True,
                'lamp01': True,
                'lamp02': False,
                'window': False,
                'projector': True,
                'airConditioning': False,
                'presence': False,
                'online': True
            },
            {
                'name': 'Sala 02',
                'persons': 10,
                'temperature': 26,
                'smoke': True,
                'lamp01': True,
                'lamp02': False,
                'window': False,
                'projector': True,
                'air-conditioning': False,
                'presence': False,
                'online': False
            },
            {
                'name': 'Sala 03',
                'persons': 10,
                'temperature': 26,
                'smoke': True,
                'lamp01': True,
                'lamp02': False,
                'window': False,
                'projector': True,
                'air-conditioning': False,
                'presence': False,
                'online': True
            }
        ]
    }

    response['rooms']
    return build_json_response(response)