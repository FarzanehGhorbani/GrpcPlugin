from google.protobuf import json_format
from urllib import parse

class Base:
    def deserialize(self,request_body):
        items=self.__class__.__dict__['__annotations__']
        if set(items.keys())==set(request_body.keys()):
            for item in items.items():
                try:
                    setattr(self,item[0],item[1](request_body[item[0]]))
                except : 
                    raise Exception(f'type({item[0]}) != type({request_body[item[0]]})')



class BodyBase(Base):
    def __init__(self,request_body) -> None:
        data=json_format.MessageToDict(request_body)
        self.deserialize(data)

class QueryParametersBase(Base):
    def __init__(self,url) -> None:
        query=parse.urlsplit(url).query
        params=dict(parse.parse_qsl(query))
        self.deserialize(params)
        
