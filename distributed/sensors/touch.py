import threading
from queue import Queue
import RPi.GPIO as gpio

from distributed.model.room import Room


def init(room: Room, producer_queue: Queue[Room], sensors=['door', 'smoke', 'window', 'presence']):
    for sensor in sensors:
        threading.Thread(target=handle_touch_event, args=(
            sensor, room, producer_queue)).start()


def handle_touch_event(sensor_name, room, producer_queue):
    pin = getattr(room.gpio, sensor_name)
    current_value = gpio.input(pin)

    setattr(room, sensor_name, bool(current_value))

    queue = Queue()

    gpio.add_event_detect(pin, gpio.BOTH, callback=queue.put)

    while True:
        queue.get()
        setattr(room, sensor_name, bool(gpio.input(pin)))
        producer_queue.put_nowait(room)
