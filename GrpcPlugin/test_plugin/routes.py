from ..GrpcFrame.router import Router
from ..protos.base_proto_pb2 import Response
from .requests import SignInBody

router=Router()

@router(method=['POST','GET'],url='/signup',response_model="text")
async def test(request,context):
    return Response(status_code=200,result=True,message='I m have to method',body=request.body)

