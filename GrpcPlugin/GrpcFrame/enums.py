from enum import Enum

class ResponseModelType(Enum):
    json=0
    text=1


class Method(Enum):
    GET = 0
    POST = 1
    PUT=2
    DELETE=3