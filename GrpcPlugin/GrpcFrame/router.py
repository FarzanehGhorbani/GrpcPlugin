from typing import Union,Dict,List
import functools
import inspect
from .enums import ResponseModelType,Method
from .middleware import BaseMiddleware
from ..protos.base_proto_pb2 import Request,Response
from .exception import InternalErrorException,def_internal_error_exception
from . import logger


class Router:
    routers_list:List[object]=[]
  
    def __init__(self) -> None:
        self.middlewares:List[BaseMiddleware]=[]
        self.functions:Dict[tuple,callable]={}
        self.exceptions:Dict[Exception,callable]={}
        self.exceptions[InternalErrorException]=def_internal_error_exception
        self.routers_list.append(self)

    def add_middleware(self,middleware:BaseMiddleware) -> None:
        self.middlewares.append(middleware())

    def add_exception_handler(self,exception:Exception,func:callable) -> None:
        self.exceptions[exception]=func

    @staticmethod
    async def async_sync_function_handler(func:callable,*args,**kwargs)->callable:
        """Handle async and sync functions."""
        if inspect.iscoroutinefunction(func):                     
            result = await func(*args,**kwargs)
        else:
            result=func(*args,**kwargs)
        
        return result

    def __call__(self,url:str,method:Union[list,Method],response_model:ResponseModelType=ResponseModelType.json)->callable:
        return self.route_function(url,method,response_model)

    def update_routes_functions_list(self,url:str,method:Union[list,Method],func):
        """
        add new route to routes_function with (url,method) as key and __middleware(function) as value.
        __middleware(function) is a wrapper function that will be called before the function and after the function.

        """
        if isinstance(method,list):
            for m in method:
                self.functions[(url,m)]=func
        else:
            self.functions[(url,method)]=func

    
    def route_function(self,url:str,method:Union[list,Method],response_model:ResponseModelType):
        """Path Operatiin Method Decorator"""
        def actual_decorator(func):
            # add route to route_list
            self.update_routes_functions_list(url,method,func)
            
            @functools.wraps(func)
            async def wrapper(request,context): 
                
                result=await self.async_sync_function_handler(func,request,context)
                
                return result

            return wrapper
        return actual_decorator
    
    def __middleware(self,func):
        """for handle Middlewares"""
        @functools.wraps(func)
        async def wrapper(request,context):
            
            for m in self.middlewares:
                m.request=request
                m.context=context
                request,context=await self.async_sync_function_handler(m.before_function) 
            
            response=await self.async_sync_function_handler(func,request,context)
            
            
            for m in self.middleware_list:
                m.response=response
                response=await self.async_sync_function_handler(m.after_function)
            
            return response
        
        return wrapper

class Router_Manager:

    def __init__(self) -> None:
        self.router_objects_list:List[Router]=[]
        self.router_objects_list=Router.routers_list

    async def dispatch(self,request,context):
        """
        Find the function with the given url and method.
        """
        for router in self.router_objects_list:
            route_function=router.functions.get((request.url,Method(request.method).name),None)
            if route_function is not None:
                try:
                    return await route_function(request,context)
                except Exception as exc :
                    try:
                        return await router.async_sync_function_handler(router.exceptions[type(exc)],exc)
                    except:
                        logger.error(f"Exception: {exc}")
                        return await router.async_sync_function_handler(router.exceptions[InternalErrorException],exc) 
        
        

    






