import logging
from central.building.building import Building
from .http import build_json_response


logger = logging.getLogger('actions')


def get_building(body: str, building: Building):
    return build_json_response(building.asdict())


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
