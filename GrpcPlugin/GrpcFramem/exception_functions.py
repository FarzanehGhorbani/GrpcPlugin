
from .exception import InternalErrorException, UnicornException,NotFoundException
from ..protos.base_proto_pb2 import Response
from google.protobuf.struct_pb2 import Struct

async def unicorn_exception_handler(exc: UnicornException):
    return Response(
        status_code=418,
        message=f"message:{exc.name}",
        body=Struct(),
        result=False
    )
async def def_not_found_exception(exc: NotFoundException):
    return Response(
        status_code=404,
        message=exc.message,
        body=Struct(),
        result=False
    )

def custome_internal_exception(exc: InternalErrorException):
    return Response(
        status_code=500,
        message=f"Internal Server Error Customized",
        body=Struct(),
        result=False
    )
