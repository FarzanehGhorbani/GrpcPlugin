from google.protobuf.struct_pb2 import Struct
from ..protos.base_proto_pb2 import Response
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name



class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class InternalErrorException(Exception):
    def __init__(self):
        ...


def def_internal_error_exception(exc:InternalErrorException):
    return Response(
        status_code=500,
        message=f"Internal Server Error",
        body=Struct(),
        result=False
    )