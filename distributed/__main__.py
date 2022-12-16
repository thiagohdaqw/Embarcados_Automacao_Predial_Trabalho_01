import time
import signal
import RPi.GPIO as gpio
from queue import Queue

from distributed import setup
from distributed.util import config
from distributed.central import server
from distributed.sensors import dht22, persons, relay, touch

def main(to_exit):
    central_config, distributed_config = config.load_configs()

    room = setup.init(distributed_config)

    producer_queue = server.init(
        central_config['ip_servidor_central'],
        central_config['porta_servidor_central'],
        room,
    )

    persons.init(room)
    touch.init(room, producer_queue)

    dhtDevice = dht22.init(room, producer_queue)

    to_exit.append(dhtDevice)

    while True:
        if room.lamp_on_time > 0:
            relay.update_lamps(room.gpio, True)
            room.lamp_on_time -= room.main_delay

        relay.read_relay(room)

        producer_queue.put_nowait(room)
        time.sleep(room.main_delay)


if __name__ == "__main__":
    to_exit = []

    try:
        main(to_exit)
    finally:
        signal.alarm(0)
        # gpio.cleanup()

        for x in to_exit:
            x.exit()
