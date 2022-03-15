import imp
from typing import Union,Dict
from enum import Enum
import functools
import inspect
from urllib import request
from .enums import ResponseModelType,Method



def router(url:str,method:Method,response_model:ResponseModelType=ResponseModelType.none):
    return Router().decorator(url,method,response_model)
    

class Router:
    routes_function:Dict[tuple,callable]={}

    def __init__(self) -> None:
        pass

    def router(self,url:str,method:Method,response_model:ResponseModelType=ResponseModelType.none):
        return self.decorator(url,method,response_model)

    def decorator(self,url:str,method:Union[list,Method],response_model:ResponseModelType):
        def actual_decorator(func):
            # add route to route_list
            if isinstance(method,list):
                for m in method:
                    Router.routes_function[(url,m)]=func
            else:
                Router.routes_function[(url,method)]=func
            @functools.wraps(func)
            async def wrapper(request,context): 
                if inspect.iscoroutinefunction(func):                     
                    result = await func(request,context)
                else:
                    result=func(request,context)
                
                return result

            return wrapper
        return actual_decorator