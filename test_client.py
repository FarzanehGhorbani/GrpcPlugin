from GrpcPlugin.GrpcFramem.client import caller


result=caller(url="/signup",method="post",body={"name":"test"})
print(result)