from connector import MessageQueue, Message
from socket import socket

def handler_func(conn: socket, queue: MessageQueue):
    msg = conn.recv(500)

    queue.put((Message.BROADCAST, msg))
