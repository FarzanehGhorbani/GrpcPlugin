from .GrpcFramem.handler import serve
import asyncio
from .GrpcFramem import routes

def run_server():
    asyncio.run(serve())
