import signal
from adafruit_dht import DHT22
from queue import Queue
from functools import partial

from distributed.model.room import RoomGPIO, Room


def init(room: Room, roomGPIO: RoomGPIO, producer_queue: Queue[Room]):
    dhtDevice = DHT22(roomGPIO.dth22)

    handler = partial(dht22_handler, dhtDevice=dhtDevice,
                      room=room, producer_queue=producer_queue)

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(2)

    return dhtDevice


def dht22_handler(signum, frame, dhtDevice: DHT22, room: Room, producer_queue: Queue[Room]):
    signal.alarm(2)

    for _ in range(5):
        try:
            dhtDevice.measure()
            room.humidity = dhtDevice.humidity
            room.temperature = dhtDevice.temperature
            producer_queue.put_nowait(room)
            return
        except RuntimeError:
            continue
