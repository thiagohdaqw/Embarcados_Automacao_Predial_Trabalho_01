import RPi.GPIO as gpio

from distributed.model.room import Room, RoomGPIO


def init(distributed_config) -> tuple[Room, RoomGPIO]:

    gpio.setmode(gpio.BCM)

    outputs = {output['name']: output['gpio']    for output in distributed_config['outputs']}
    inputs  = {input['name'] : input['gpio']     for input  in distributed_config['input']}

    gpio.setup(list(outputs.values()), gpio.OUT)
    gpio.setup(list(inputs.values()), gpio.IN, pull_up_down=gpio.PUD_UP)

    name = distributed_config['name']
    dth22 = distributed_config['temperature'][0]['gpio']

    room = Room(name)
    roomGPIO = RoomGPIO(name, dth22, **outputs, **inputs)

    return room, roomGPIO
