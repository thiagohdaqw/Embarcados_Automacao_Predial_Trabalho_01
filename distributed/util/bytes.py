

def int_to_bytes(value: int, signed=False):
    return value.to_bytes(4, 'little', signed=signed)


def int_from_bytes(value: bytes, signed=False):
    return int.from_bytes(value, 'little', signed=signed)
