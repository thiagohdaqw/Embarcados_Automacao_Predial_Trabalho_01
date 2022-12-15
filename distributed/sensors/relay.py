import RPi.GPIO as gpio

from distributed.model.room import Room, RoomGPIO


def read_relay(room: Room, roomGPIO: RoomGPIO):
    room.alarm = bool(gpio.input(roomGPIO.alarm))
    room.lamp01 = bool(gpio.input(roomGPIO.lamp01))
    room.lamp02 = bool(gpio.input(roomGPIO.lamp02))
    room.projector = bool(gpio.input(roomGPIO.projector))
    room.air_conditioning = bool(gpio.input(roomGPIO.air_conditioning))