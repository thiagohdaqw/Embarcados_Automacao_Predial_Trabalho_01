import logging

from central.building.building import Building
from central.util.json import from_json
from .http import build_json_response


logger = logging.getLogger('actions')


def toggle_relay(body, building: Building):
    logger.info(f'{body["room_name"]},toggle,{body["sensor_name"]}')
    
    data = from_json(body)

    building.toggle_room_relay(data)

    return build_json_response(
        {
            'success': True,
            'message': f'O comando para alternar o valor do sensor {building["sensor_name"]} foi enviado com sucesso'
        }
    )
