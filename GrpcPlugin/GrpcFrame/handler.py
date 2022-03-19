from ..protos.base_proto_pb2_grpc import HTTPHandlerServicer
from ..protos.base_proto_pb2_grpc import add_HTTPHandlerServicer_to_server
import grpc
from ..protos.base_proto_pb2 import Response
from .router import Router_Manager

class HTTPService(HTTPHandlerServicer):
    async def Dispatch(self, request, context): 
        router_manage=Router_Manager()
        return await router_manage.dispatch(request)
        
        



async def serve() -> None:
    server = grpc.aio.server()
    add_HTTPHandlerServicer_to_server(HTTPService(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()