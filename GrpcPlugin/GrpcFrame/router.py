from collections import OrderedDict
from typing import Union,Dict,List
import functools
import inspect
from .enums import ResponseModelType,Method
from .middleware import BaseMiddleware
from ..protos.base_proto_pb2 import Request,Response
from .exception import InternalErrorException,def_internal_error_exception
from . import logger
from google.protobuf import json_format
from .request_response_bases import BodyBase,QueryParametersBase
from urllib import parse
from typing import List


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
    async def async_sync_function_handler(func:callable,*args)->callable:
        """Handle async and sync functions."""
        if inspect.iscoroutinefunction(func):                     
            result = await func(*args)
        else:
            result=func(*args)
        
        return result

    def __call__(self,url:str,method:Union[list,Method],response_model:ResponseModelType=ResponseModelType.json)->callable:
        return self.route_function(url,method,response_model)

    def update_routes_functions_list(self,url:str,method:Union[list,Method],func,*args):
        """
        add new route to routes_function with (url,method) as key and __middleware(function) as value.
        __middleware(function) is a wrapper function that will be called before the function and after the function.

        """
        if isinstance(method,list):
            for m in method:
                self.functions[(url,m)]=self.__middleware(func)
        else:
            self.functions[(url,method)]=self.__middleware(func)

    
    def route_function(self,url:str,method:Union[list,Method],response_model:ResponseModelType):
        """Path Operatiin Method Decorator"""
        def actual_decorator(func):
           
            
            @functools.wraps(func)
            async def wrapper(*args): 
                
                result=await self.async_sync_function_handler(func,args)
                
                return result
            
            self.update_routes_functions_list(url,method,func)
            return wrapper
        return actual_decorator

    @staticmethod
    def get_function_parameters(func)->list:
        function_parameters=inspect.signature(func).parameters.values()
        parameters_dict:dict={}
        for param in function_parameters:
            parameters_dict[param.name]=param.annotation
        
        return parameters_dict

    def deserialize_function_parameters(self,func,request):
        function_parameters=self.get_function_parameters(func)
        data=list()
        for key,value in function_parameters.items():
            if issubclass(value,BodyBase):
                data.append(function_parameters[key](request.body))
            elif issubclass(value,QueryParametersBase):
                data.append(function_parameters[key](request.url))
        return data
    
    async def run_middleware_functions(self,func_name,args):
        request=args
        if func_name=='before_funcction':
            async for m in self.middlewares:
                m.request=request
                request=await self.async_sync_function_handler(m.before_function) 
            
            return (request)
        else:
            response=args
            for m in self.middlewares:
                m.response=response
                response=await self.async_sync_function_handler(m.after_function)      
            return response

    async def run_path_function(self,func,request):
        data=self.deserialize_function_parameters(func,request)
            
        response = await self.async_sync_function_handler(func,*data)

        return response

    def __middleware(self,func):
        """for handle Middlewares"""
        @functools.wraps(func)
        async def middleware_wrapper(request):
            
            request=await self.run_middleware_functions('before_function',request)
                                    
            response=await self.run_path_function(func,request)
            
            response=await self.run_middleware_functions('after_function',response)
                  
            return response
        
        return middleware_wrapper

class Router_Manager:

    def __init__(self) -> None:
        self.router_objects_list:List[Router]=[]
        self.router_objects_list=Router.routers_list

    async def dispatch(self,request):
        """
        Find the function with the given url and method.
        """
        for router in self.router_objects_list:
            url=parse.urlsplit(request.url).path
            route_function=router.functions.get((url,Method(request.method).name),None)
            if route_function is not None:
                try:
                    return await router.async_sync_function_handler(route_function,request)
                except Exception as exc :
                    try:
                        return await router.async_sync_function_handler(router.exceptions[type(exc)],exc)
                    except:
                        logger.error(f"Exception: {exc}")
                        return await router.async_sync_function_handler(router.exceptions[InternalErrorException],exc) 
        
        

    






