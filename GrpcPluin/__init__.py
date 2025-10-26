"""gRPC Plugin - A framework for building gRPC servers and clients."""

from concurrent import futures

from grpc import server

from .Frame.connector import GrpcComposer, GrpcConfigs, GrpcConnector
from .Frame.manager import GrpcManager
from .Frame.router import METHODS, GrpcRouter
from .proto.base_proto_pb2_grpc import (
    GrpcHandlerStub,
    add_GrpcHandlerServicer_to_server,
)

# Create a global router instance
router = GrpcRouter()

# Create a composer for the gRPC service
composer = GrpcComposer(
    stub=GrpcHandlerStub,
    service_provider=add_GrpcHandlerServicer_to_server,
    servicer=GrpcManager(router=router),
)

# Create a connector for managing the gRPC server
connector = GrpcConnector(
    server=server(thread_pool=futures.ThreadPoolExecutor(max_workers=10)),
    composers=[composer],
    configs=GrpcConfigs(server_uri="0.0.0.0:50052"),
)

__all__ = [
    "router",
    "connector",
    "METHODS",
    "GrpcRouter",
    "GrpcConnector",
    "GrpcManager",
    "GrpcComposer",
    "GrpcConfigs",
]
