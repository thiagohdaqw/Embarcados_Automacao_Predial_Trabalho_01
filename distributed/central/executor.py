from enum import Enum
from queue import Queue
from typing import Optional

from distributed.model.room import Room, RoomGPIO
import distributed.sensors.relay as relay

class CommandType(Enum):
    RELAY = 1
    PRESENCE = 2


def execute_command(command:dict, room: Room) -> Optional[dict]:
    command_type = command['type']

    if command_type in COMMAND_EXECUTOR:
        return COMMAND_EXECUTOR[command_type](command, room)


def handle_relay_command(command, room):
    relay_name = command['relay_name']
    value = command['value']
    
    relay.update_relay(room, relay_name, value)

    return {
        'type': 'feedback',
        'message': f'{relay_name} relay {"enabled" if value else "disabled"} with success'
    }


def handle_presence_command(command, room):
    seconds = command['seconds']

    room.lamp_on_time = seconds

    return {
        'type': 'feedback',
        'message': f'lamps were enabled with success for {seconds} seconds'
    }

COMMAND_EXECUTOR = {
    CommandType.RELAY.value:    handle_relay_command,
    CommandType.PRESENCE.value: handle_presence_command,
}
