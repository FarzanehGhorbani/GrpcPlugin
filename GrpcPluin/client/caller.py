"""gRPC client request handler."""

from typing import Any

import grpc
from google.protobuf.struct_pb2 import Struct
from google.protobuf import json_format
from grpc import RpcError

from GrpcPluin.proto.base_proto_pb2 import Request as GrpcRequest  # type: ignore
from GrpcPluin.proto.base_proto_pb2_grpc import GrpcHandlerStub
from .structures import Request, Response
from .exceptions import GrpcException
from logging import getLogger

logger = getLogger(__name__)


class GrpcRequestHandler:
    """Handler for making gRPC client requests.

    This class encapsulates the logic for making gRPC calls, converting
    between Python types and protobuf types, and handling errors.
    """

    def call(self, request: Request, grpc_url: str = "0.0.0.0:50052") -> dict[str, Any]:
        """Call a gRPC service endpoint.

        Args:
            request: Client request object
            grpc_url: gRPC server URL (host:port)

        Returns:
            Response dictionary with result, status, data, and message

        Raises:
            GrpcException: If the gRPC call fails
        """
        try:
            with grpc.insecure_channel(grpc_url) as channel:
                stub = GrpcHandlerStub(channel)

                # Convert Python dict to protobuf Struct
                request_data = Struct()
                request_data.update(request.body)

                # Make the gRPC call
                grpc_request = GrpcRequest(
                    url=request.url, method=request.method, body=request_data
                )
                response = stub.Dispatch(grpc_request)

                # Convert protobuf Response to Python dict
                return Response(
                    result=response.result,
                    status=response.status_code,
                    data=json_format.MessageToDict(getattr(response, "data", None))
                    or None,
                    message=getattr(response, "message", None) or None,
                ).__dict__

        except RpcError as error:
            # Extract error information
            status_code = getattr(error, "code", lambda: grpc.StatusCode.UNKNOWN)()
            details = getattr(error, "details", lambda: "Unknown error")()
            debug_error_string = getattr(error, "debug_error_string", lambda: "")()

            # Log detailed error on client side (for debugging)
            logger.error(f"gRPC call failed: {error}")

            # Create exception with minimal details for user-facing errors
            exception = GrpcException(
                url=request.url,
                status_code=status_code,
                details=details,
                debug_error_string=debug_error_string,
            )
            raise exception from error
