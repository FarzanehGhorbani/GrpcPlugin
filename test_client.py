from GrpcPlugin.GrpcFrame.client import caller

result=caller(url="/signup?user_id=32&token=test",method="post",body={"username":"farzaneh","age":12,"email":"far@gmail.com"})
print(result.status_code)

