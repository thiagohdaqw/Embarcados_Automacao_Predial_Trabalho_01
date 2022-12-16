import logging
from .http import build_json_response
from central.building.building import Building
from central.util.json import from_json

logger = logging.getLogger('actions')


def get_building(body: str, building: Building):
    return build_json_response(building.asdict())


def update_lamps(body, building: Building):
    logging.info(f',update {body["value"]},lamps')

    data = from_json(body)

    building.update_lamps(data['value'])

    return build_json_response({
        'success': True,
        'message': 'O comando para atualizar as lampadas do prédio foi enviado'
    })

def update_relays(body, building: Building):
    logging.info(f',update {body["value"]},relays')

    data = from_json(body)

    building.update_relays(data['value'])

    return build_json_response({
        'success': True,
        'message': 'O comando para atualizar das cargas do prédio foi enviado'
    })


def toogle_alarm_system(body, building: Building):
    logging.info(',toggle,alarm system')

    message = ''
    success = True

    if building.alarm_system:
        building.disable_alarm_system()
        message = 'O comando para a desativação do sistema de alarme foi enviado com sucesso'
    else:
        sensors = building.enable_alarm_system()

        if sensors:
            message = 'Não foi possível acionar o sistema de alarme, os seguintes sensores estão ativados: {sensors}'
            success = False
        else:
            message = 'O comando para a ativação do sistema de alarme foi enviado com sucesso'

    return build_json_response({
        'success': success,
        'message': message
    })
