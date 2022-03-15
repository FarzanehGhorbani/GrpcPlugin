from GrpcPlugin.GrpcFramem.client import caller


result=caller(url="/signup",method="post",body={"name":"test"})
result2=caller(url="/signup",method="PUT",body={"name":"test"})
print(result)
print(result2)