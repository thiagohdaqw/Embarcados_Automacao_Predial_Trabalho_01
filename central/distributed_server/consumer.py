from central.server.server import MessageQueue, MessageType
from central.model.building import Building
from central.util.json import from_json

def consume_distributed_server_message(data: bytes, building: Building):
    data_json = from_json(data)

    building.update_room(data_json['name'], **data_json)
