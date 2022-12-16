from enum import Enum
from dataclasses import dataclass, field


class CommandType(Enum):
    RELAY = 1
    PRESENCE = 2

