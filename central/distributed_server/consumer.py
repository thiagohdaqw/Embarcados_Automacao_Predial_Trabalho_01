from central.building.building import Building
from central.util.json import from_json



def consume_distributed_server_message(data: bytes, building: Building):
    data_json = from_json(data)

    if 'type' in data_json:
        if data_json['type'] == 'feedback':
            handle_distributed_feedback(data_json, building)
            return

    building.update_room(**data_json)

def handle_distributed_feedback(data, building):
    building.add_feedback(data['message'])
