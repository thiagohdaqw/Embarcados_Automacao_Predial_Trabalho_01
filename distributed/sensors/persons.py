import RPi.GPIO as gpio
import time


import threading
from distributed.model.room import RoomGPIO, Room


def init(room: Room, roomGPIO: RoomGPIO):
    gpio.add_event_detect(roomGPIO.door_in, gpio.RISING)
    gpio.add_event_detect(roomGPIO.door_out, gpio.RISING)

    threading.Thread(target=run_persons_counter, args=(room, roomGPIO)).start()


def run_persons_counter(room: Room, roomGPIO: RoomGPIO):
    while True:
        if gpio.event_detected(roomGPIO.door_in):
            room.persons += 1

        if gpio.event_detected(roomGPIO.door_out):
            room.persons -= 1

        time.sleep(0.05)
