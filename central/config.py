import os
import json
import sys
import util


def get_configs():
    if len(sys.argv) != 4:
        print("Uso: python",
              sys.argv[0], "central_config_json_file config_separator config_room_json_files")
        sys.exit(1)

    central_config = util.read_json(sys.argv[1])
    config_separator = sys.argv[2]
    room_configs = [util.read_json(path)
                    for path in sys.argv[3].split(config_separator)]

    return central_config, room_configs
