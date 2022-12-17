import logging
from .http import build_json_response
from central.building.building import Building
from central.util.json import from_json

logger = logging.getLogger('actions')


def get_building(body: str, building: Building):
    return build_json_response(building.asdict())


def update_lamps(body, building: Building):
    data = from_json(body[0])

    building.update_lamps(data['value'])

    logger.info(f',update {data["value"]},lamps')
    return build_json_response({
        'success': True,
        'message': 'O comando para atualizar as lampadas do prédio foi enviado'
    })

def update_relays(body, building: Building):
    data = from_json(body[0])

    building.update_relays(data['value'])

    logger.info(f',update {data["value"]},relays')
    return build_json_response({
        'success': True,
        'message': 'O comando para atualizar das cargas do prédio foi enviado'
    })


def toogle_alarm_system(body, building: Building):
    logger.info(',toggle,alarm system')

    message = ''
    success = True

    if building.alarm_system:
        if building.disable_alarms():
            message = 'O comando para a desativação do sistema de alarme foi enviado com sucesso'
        else:
            message = 'Nao foi possivel realizar o comando, o predio esta em chamas!'
    else:
        sensors = building.enable_alarm_system()

        if sensors:
            message = f'Não foi possível acionar o sistema de alarme, os seguintes sensores estão ativados: {sensors}'
            success = False
        else:
            message = 'O comando para a ativação do sistema de alarme foi enviado com sucesso'

    return build_json_response({
        'success': success,
        'message': message
    })
