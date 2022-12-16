import time
import socket
import threading
from queue import Queue

from distributed.model.room import Room
import distributed.central.consumer as consumer
import distributed.central.producer as producer
from distributed.util.bytes import int_to_bytes


def init(host: str, port: int, room: Room, command_queue: Queue) -> tuple[Queue[Room], Queue]:
    producer_queue = Queue()

    conn = connect_central_server(host, port, room)

    threading.Thread(target=consumer.consume,
                     args=(conn, command_queue)).start()

    threading.Thread(target=producer.produce,
                     args=(conn, producer_queue)).start()

    return producer_queue


def connect_central_server(host, port, room):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            conn.connect((host, port))

            conn.sendall(int_to_bytes(len(room.name)))
            conn.sendall(room.name.encode('utf-8'))
            return conn
        except TimeoutError:
            print("Cant stablish a Server Central connection. Retrying in 5 secs...")
            time.sleep(5)
