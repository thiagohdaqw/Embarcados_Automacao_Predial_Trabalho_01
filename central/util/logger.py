import logging
import sys


def init():
    init_console_logger()
    init_actions_logger()

def init_console_logger():
    logger = logging.getLogger('console')
    logger.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(logging.Formatter('[%(conn)s]: %(message)s'))

    logger.addHandler(stdout_handler)

def init_actions_logger():
    logger = logging.getLogger('actions')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('central_logs.csv')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s,%(conn)s,%(message)s'))

    logger.addHandler(file_handler)
