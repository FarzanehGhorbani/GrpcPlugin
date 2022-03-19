from ..GrpcFrame.router import Router
from ..protos.base_proto_pb2 import Response
from .requests import Body,UrlParameter

from google.protobuf.struct_pb2 import Struct
import json

router=Router()

@router(method=['POST','GET'],url='/signup',response_model="text")
async def test(request:Body,url_parameter:UrlParameter):
    print(request.username)
    print(url_parameter.user_id)
    print(url_parameter.token)
    return Response(status_code=200,result=True,message='I m signup',body=Struct())


# @router(method='POST',url='/signin',response_model="text")
# async def test(request:Request):
#     # data=json_format.MessageToDict(request.body)
#     return Response(status_code=200,result=True,message='I \'m sign in',body=request.body)
