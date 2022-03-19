from ..GrpcFrame.request_response_bases import BodyBase,QueryParametersBase


class UrlParameter(QueryParametersBase):
    user_id:int
    token:str



class Body(BodyBase):
    username:str
    email:str
    age:int


