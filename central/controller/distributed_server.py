from central.server.server import MessageQueue, MessageType


def handle_distributed_server_message(data: bytes, queue: MessageQueue):
    queue.append((MessageType.BROADCAST, data))
