import time
import signal
import RPi.GPIO as gpio
from queue import Queue

from distributed import setup
from distributed.util import config
from distributed.central import server
import distributed.central.command as command
from distributed.model.room import Room
from distributed.sensors import dht22, persons, relay, touch

def main(to_exit):
    central_config, distributed_config = config.load_configs()

    room, roomGPIO = setup.init(distributed_config)

    command_queue = Queue()

    producer_queue = server.init(
        central_config['ip_servidor_central'],
        central_config['porta_servidor_central'],
        room,
        command_queue
    )

    persons.init(room, roomGPIO)
    touch.init(room, roomGPIO, producer_queue)

    dhtDevice = dht22.init(room, roomGPIO, producer_queue)

    to_exit.append(dhtDevice)

    while True:
        if not command_queue.empty():
            command.handle(command_queue, room)

        relay.read_relay(room, roomGPIO)

        producer_queue.put_nowait(room)
        time.sleep(0.5)


if __name__ == "__main__":
    to_exit = []

    try:
        main(to_exit)
    finally:
        signal.alarm(0)
        # gpio.cleanup()

        for x in to_exit:
            x.exit()
