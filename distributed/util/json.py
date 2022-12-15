import os
import json


def read_json_file(file, dir=os.getcwd()):
    with open(dir + '/' + file, 'rb') as f:
        return json.load(f)

def to_json(dict) -> bytes:
    return json.dumps(dict).encode('utf-8')

def from_json(data: bytes) -> dict:
    return json.loads(data)