import os
import json


def read_json_file(file, dir=os.getcwd()):
    with open(dir + '/' + file, 'rb') as f:
        return json.load(f)

def from_json(data):
    return json.loads(data)
