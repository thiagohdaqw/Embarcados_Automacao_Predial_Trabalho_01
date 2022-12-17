import logging

from central.building.building import Building
from central.util.json import from_json
from .http import build_json_response


logger = logging.getLogger('actions')


def toggle_relay(body, building: Building):
    data = from_json(body[0])
    
    building.toggle_room_relay(data)

    logger.info(f'{data["room_name"]},toggle,{data["relay_name"]}')
    return build_json_response(
        {
            'success': True,
            'message': f'O comando para alternar o valor do sensor {data["relay_name"]} foi enviado com sucesso'
        }
    )
