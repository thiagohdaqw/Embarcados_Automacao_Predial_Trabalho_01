import sys
from distributed.util.json import read_json_file

def load_configs():
    if len(sys.argv) != 3:
        print('Uso: python -m distributed distributed_config_json_file central_config_json_file')
        sys.exit(1)

    return read_json_file(sys.argv[1]), read_json_file(sys.argv[2])
