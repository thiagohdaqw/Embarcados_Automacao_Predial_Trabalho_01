from enum import Enum
from queue import Queue

from dataclasses import dataclass, field
from distributed.model.room import Room
import distributed.sensors.relay as relay
import distributed.central.producer as producer

class CommandType:
    RELAY = 1
    PRESENCE = 2


def handle(room: Room, command_queue: Queue[dict], producer_queue: Queue):
    command = command_queue.get()
    command_type = command['type']

    if command_type in COMMAND_EXECUTOR:
        COMMAND_EXECUTOR[command_type](room, command, producer_queue)


def handle_relay_command(room, roomGPIO, command, producer_queue):
    relay_name = command['relay_name']
    value = command['value']
    
    relay.update_relay(room, roomGPIO, relay_name, value)

    producer_queue.put_noawait({
        'type': 'feedback',
        'message': f'{relay_name} relay {"enabled" if value else "disabled"} with success'
    })


def handle_presence_command(room, roomGPIO, command, producer_queue):
    ...

COMMAND_EXECUTOR = {
    CommandType.RELAY.value:    handle_relay_command,
    CommandType.PRESENCE.value: handle_presence_command,
}