import RPi.GPIO as gpio
import time


import threading
from distributed.model.room import RoomGPIO, Room


def init(room: Room):
    gpio.add_event_detect(room.gpio.door_in, gpio.RISING)
    gpio.add_event_detect(room.gpio.door_out, gpio.RISING)

    threading.Thread(target=run_persons_counter, args=(room,)).start()


def run_persons_counter(room: Room):
    while True:
        if gpio.event_detected(room.gpio.door_in):
            room.persons += 1

        if gpio.event_detected(room.gpio.door_out):
            room.persons -= 1

        time.sleep(0.05)
