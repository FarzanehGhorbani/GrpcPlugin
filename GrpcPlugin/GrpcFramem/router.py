from typing import Union,Dict,List
import functools
import inspect
from .enums import ResponseModelType,Method
from .middleware import BaseMiddleware
from ..protos.base_proto_pb2 import Request
from .exception import InternalErrorException,def_internal_error_exception

class Router:
    routes_function:Dict[tuple,callable]={}
    exception_handlers:Dict[Exception,callable]={}

    def __init__(self) -> None:
        self.middleware_list : List[BaseMiddleware] = []
        Router.exception_handlers[InternalErrorException]=def_internal_error_exception
        
    
    def __call__(self,url:str,method:Method,response_model:ResponseModelType=ResponseModelType.none):
        return self.route_method(url,method,response_model)


    def add_middleware(self, middleware:BaseMiddleware):
        """Add middleware to the list of middlewares"""
        self.middleware_list.append(middleware())


    def update_routes_functions_list(self,url:str,method:Union[list,Method],func):
        """
        add new route to routes_function with (url,method) as key and __middleware(function) as value.
        __middleware(function) is a wrapper function that will be called before the function and after the function.

        """
        if isinstance(method,list):
            for m in method:
                Router.routes_function[(url,m)]=self.__middleware(func)
        else:
            Router.routes_function[(url,method)]=self.__middleware(func)


    @staticmethod
    async def funtion_call_handler(func:callable,*args,**kwargs):
        """Handle async and sync functions."""
        if inspect.iscoroutinefunction(func):                     
            result = await func(*args,**kwargs)
        else:
            result=func(*args,**kwargs)
        
        return result


    def route_method(self,url:str,method:Union[list,Method],response_model:ResponseModelType):
        """Path Operatiin Method Decorator"""
        def actual_decorator(func):
            # add route to route_list
            self.update_routes_functions_list(url,method,func)
            
            @functools.wraps(func)
            async def wrapper(request,context): 
                
                result=await Router.funtion_call_handler(func,request,context)
                
                return result

            return wrapper
        return actual_decorator

    
    
    def __middleware(self,func):
        """for handle Middlewares"""
        @functools.wraps(func)
        async def wrapper(request,context):
            
            for m in self.middleware_list:
                m.request=request
                m.context=context
                request,context=await Router.funtion_call_handler(m.before_function) 
            
            response=await Router.funtion_call_handler(func,request,context)
            
            
            for m in self.middleware_list:
                m.response=response
                response=await Router.funtion_call_handler(m.after_function)
            
            return response
        
        return wrapper

    
    def add_exception_handler(self,exc:Exception,func):
        Router.exception_handlers[exc]=func

    
    @classmethod
    async def find_function(cls,request:Request,context):
        route_function=cls.routes_function[request.url,Method(request.method).name]
        try:
            return await route_function(request,context)
        except Exception as exc :
            try:
                return await cls.funtion_call_handler(cls.exception_handlers[type(exc)],exc)
            except:
                print(exc)
                return await cls.funtion_call_handler(cls.exception_handlers[InternalErrorException],exc) 

            




















