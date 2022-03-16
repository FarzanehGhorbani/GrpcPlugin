
from urllib import response
from .router import Router
from ..protos.base_proto_pb2 import Response
from .exception import UnicornException
from google.protobuf.struct_pb2 import Struct
from .middleware import BaseMiddleware
class M(BaseMiddleware):
    def before_function(self):
        return self.request,self.context
        

    def after_function(self):
        if self.response.result==True:
            self.response.message='successful'
        return self.response


router=Router()
router.add_middleware(M)



@router(method=['POST','GET'],url='/signup',response_model="text")
async def test(request,context):
    return Response(status_code=200,result=True,message='I m have to method',body=request.body)




async def unicorn_exception_handler(request,exc: UnicornException):
    return Response(
        status_code=418,
        message={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
        body=Struct(),
        result=False
    )

router.add_exception_handler(UnicornException,unicorn_exception_handler)














