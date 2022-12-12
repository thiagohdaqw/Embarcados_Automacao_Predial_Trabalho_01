import sys
from . import util


def get_config():
    if len(sys.argv) != 2:
        print("Uso: python",
              sys.argv[0], "central_config_json_file")
        sys.exit(1)

    return util.read_json(sys.argv[1])
