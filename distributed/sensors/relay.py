import RPi.GPIO as gpio

from distributed.model.room import Room, RoomGPIO


def read_relay(room: Room):
    room.alarm = bool(gpio.input(room.gpio.alarm))
    room.lamp01 = bool(gpio.input(room.gpio.lamp01))
    room.lamp02 = bool(gpio.input(room.gpio.lamp02))
    room.projector = bool(gpio.input(room.gpio.projector))
    room.air_conditioning = bool(gpio.input(room.gpio.air_conditioning))


def update_relay(room: Room, relay_name: str, value: bool):
    setattr(room, relay_name, value)
    pin = getattr(room.gpio, relay_name)

    gpio.output(pin, gpio.HIGH if value else gpio.LOW)


def update_lamps(roomGPIO: RoomGPIO, value: bool):
    lamps = ['lamp01', 'lamp02']
    
    for lamp in lamps:
        pin = getattr(roomGPIO, lamp)

        gpio.output(pin, gpio.HIGH if value else gpio.LOW)
