from asyncio import Handle
from ..protos.base_proto_pb2 import Request,Response
from ..protos.base_proto_pb2_grpc import HTTPHandlerServicer,add_HTTPHandlerServicer_to_server
import grpc
from .router import Router
from .enums import Method

class HTTPService(HTTPHandlerServicer):
    async def Dispatch(self, request, context):
        try:
            route_function=Router.routes_function[request.url,Method(request.method).name]
        except:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Method not Found! with url: {request.url} and method: {Method(request.method).name}')
            return Response(status_code=404,result=False,message='Method not Found! with url: '+request.url+' and method: '+Method(request.method).name)
        return await route_function(request,context)

class Handler(HTTPService):
    ...

        
        



async def serve() -> None:
    server = grpc.aio.server()
    add_HTTPHandlerServicer_to_server(Handler(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


















