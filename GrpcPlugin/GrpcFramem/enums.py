from enum import Enum

class ResponseModelType(Enum):
    none=1
    text=2
    json=3


class Method(Enum):
    GET = 0
    POST = 1
    PUT=2
    DELETE=3