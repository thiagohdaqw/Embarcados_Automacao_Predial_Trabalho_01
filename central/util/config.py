import sys
from . import json


def get_config():
    if len(sys.argv) != 2:
        print("Uso: python",
              sys.argv[0], "central_config_json_file")
        sys.exit(1)

    return json.read_json(sys.argv[1])
