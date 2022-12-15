import threading
from queue import Queue
import RPi.GPIO as gpio

from distributed.model.room import Room, RoomGPIO


def init(room: Room, roomGPIO: RoomGPIO, producer_queue: Queue[Room], sensors=['door', 'smoke', 'window', 'presence']):
    for sensor in sensors:
        threading.Thread(target=handle_touch_event, args=(
            sensor, room, roomGPIO, producer_queue)).start()


def handle_touch_event(sensor_name, room, roomGPIO, producer_queue):
    pin = getattr(roomGPIO, sensor_name)
    current_value = gpio.input(pin)

    setattr(room, sensor_name, bool(gpio.input(pin)))

    start_edge = gpio.RISING if current_value == gpio.LOW else gpio.FALLING
    end_edge = gpio.FALLING if current_value == gpio.LOW else gpio.RISING

    while True:
        notify_on_edge(start_edge, pin, sensor_name, room, producer_queue)
        notify_on_edge(end_edge, pin, sensor_name, room, producer_queue)


def notify_on_edge(edge, pin, sensor_name, room, producer_queue):
    gpio.wait_for_edge(pin, edge)

    setattr(room, sensor_name, bool(gpio.input(pin)))
    producer_queue.put_nowait(room)
