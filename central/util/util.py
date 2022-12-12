import os
import json


def read_json(file, dir=os.getcwd()):
    with open(dir + '/' + file, 'rb') as f:
        return json.load(f)


def logger(address, msg):
    # TODO: use logging module
    print(f'[{address.host}, {address.port}]:', msg)
