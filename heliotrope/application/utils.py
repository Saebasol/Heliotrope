import struct

from sanic.exceptions import InvalidUsage


def check_int32(value: int) -> None:
    try:
        struct.pack("i", value)
    except struct.error:
        raise InvalidUsage


def check_int64(value: int) -> None:
    try:
        struct.pack("q", value)
    except struct.error:
        raise InvalidUsage
