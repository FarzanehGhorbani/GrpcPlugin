
from .router import Router
from .exception_functions import *
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
router.add_exception_handler(UnicornException,unicorn_exception_handler)
router.add_exception_handler(NotFoundException,def_not_found_exception)
router.add_exception_handler(InternalErrorException,custome_internal_exception)


@router(method=['POST','GET'],url='/signup',response_model="text")
async def test(request,context):
    raise ValueError('failed')
    # return Response(status_code=200,result=True,message='I m have to method',body=request.body)




















