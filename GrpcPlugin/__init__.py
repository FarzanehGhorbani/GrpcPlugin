from .GrpcFrame.handler import serve
import asyncio
from .test_plugin import routes

def run_server():
    asyncio.run(serve())
