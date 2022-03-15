from ..protos.base_proto_pb2 import Request
from ..protos.base_proto_pb2_grpc import HTTPHandlerStub
from google.protobuf.struct_pb2 import Struct
import grpc
import asyncio
from .enums import Method

async def async_caller(url:str,method:Method,body:dict):
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = HTTPHandlerStub(channel)
        s=Struct()
        
        try : 
            request=Request(url=url,method=method.upper(),body=s.update(body))
        except :
            raise ValueError("Method Not Allowed")
        
        response = await stub.Dispatch(request)
       

    return response



def caller(url:str,method:str,body:dict):
    loop=asyncio.get_event_loop()
    return loop.run_until_complete(async_caller(url,method,body))






