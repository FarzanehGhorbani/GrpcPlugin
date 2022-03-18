# from urllib import parse
# url = "/default.html?ct=32&op=92&item=98"
# print(parse.urlsplit(url))

class SignInQueryParams:
    key:int
    type_user:str

class Request:
    path:str
    query_params:SignInQueryParams
    host:str=None
    schema:str=None


class SignInBody:
    username:str
    age:int