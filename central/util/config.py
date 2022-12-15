import sys
import logging
from . import json


def get_config():
    if len(sys.argv) != 2:
        logging.getLogger('console').error("Uso: python -m central central_config_json_file")
        sys.exit(1)

    return json.read_json_file(sys.argv[1])
