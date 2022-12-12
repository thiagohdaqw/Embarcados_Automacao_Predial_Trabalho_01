from central.server.server import MessageQueue, MessageType


def handler_func(data: bytes, queue: MessageQueue):
    queue.append((MessageType.BROADCAST, data))
