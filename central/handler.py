from server import MessageQueue, MessageType


def handler_func(data: bytes, queue: MessageQueue):
    queue.put((MessageType.BROADCAST, data))
