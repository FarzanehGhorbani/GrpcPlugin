from asyncio import Handle
from ..protos.base_proto_pb2 import Request,Response
from ..protos.base_proto_pb2_grpc import HTTPHandlerServicer,add_HTTPHandlerServicer_to_server
import grpc
from .router import Router
from .enums import Method

class HTTPService(HTTPHandlerServicer):
    async def Dispatch(self, request, context): 
        return await Router.find_function(request,context)
        



        
        



async def serve() -> None:
    server = grpc.aio.server()
    add_HTTPHandlerServicer_to_server(HTTPService(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


















