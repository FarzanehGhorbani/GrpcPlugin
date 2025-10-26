"""gRPC manager for handling server requests."""

import logging
from typing import Any

import grpc
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Struct
from grpc import StatusCode
from grpc._server import _Context  # type: ignore
from pydantic import ValidationError
from GrpcPluin.proto.base_proto_pb2 import Response as GrpcResponse  # type: ignore
from GrpcPluin.proto.base_proto_pb2 import Method as GrpcMethod  # type: ignore
from GrpcPluin.proto.base_proto_pb2_grpc import GrpcHandlerServicer

from .enums import FunctionDetails
from .exceptions.exceptions import BaseGrpcServerException, EXCEPTIONS_MAPPING
from .router import GrpcRouter

logger = logging.getLogger(__name__)


class GrpcManager(GrpcHandlerServicer):
    """gRPC server handler that dispatches requests to registered routes.

    This class implements the gRPC Handler interface and manages
    the routing of requests to appropriate handler functions.
    """

    def __init__(self, router: GrpcRouter) -> None:
        """Initialize the gRPC manager.

        Args:
            router: Router instance to use for dispatching
        """
        self.router: GrpcRouter = router

    def Dispatch(self, request: Any, context: _Context) -> GrpcResponse | _Context:
        """Handle incoming gRPC requests.

        Args:
            request: gRPC request object
            context: gRPC server context

        Returns:
            GrpcResponse on success, context on error
        """
        try:
            # Convert protobuf to Python dict
            body = json_format.MessageToDict(request.body)

            # Find the route handler
            method_str = GrpcMethod.Name(request.method)
            func_detail: FunctionDetails = self.router._routing(
                method=method_str, url=request.url
            )

            # Extract and validate function arguments
            func_arguments: dict[str, Any] = self.router._declare_function_argument(
                func=func_detail.func, request_data=body
            )

            # Call the handler function
            response: dict[str, Any] = self.router._call(
                func=func_detail.func, request_data=func_arguments
            )
            status_code = StatusCode.OK
            result = True
            message = None
            # Validate response against response_model if provided
            if func_detail.response_model is not None:
                try:
                    validated_response = func_detail.response_model(**response)
                    logger.info(f"validation_response: {validated_response}")
                    # Use dict() for compatibility with both Pydantic v1 and v2
                    if hasattr(validated_response, "model_dump"):
                        response = validated_response.model_dump()
                    else:
                        response = validated_response.dict()
                    status_code = StatusCode.OK
                    result = True
                    message = None
                except ValidationError as error:
                    logger.error(f"ValidationError: {type(error)}")
                    logger.error(f"Response validation failed: {error}")
                    status_code = StatusCode.INVALID_ARGUMENT
                    result = False
                    message = "Response does not match expected model"
                    response = {}

            # Convert response to protobuf Struct
            struct_response = Struct()
            struct_response.update(response)
            status_code = EXCEPTIONS_MAPPING[status_code]

            # Return success response
            return GrpcResponse(
                result=result,
                status_code=status_code,
                data=struct_response,
                message=message,
            )

        except BaseGrpcServerException as error:
            # Handle known server exceptions
            # context.set_details(error.details)
            # context.set_code(error.code)
            # return context
            logger.error(f"Server exception: {error}")
            status_code = EXCEPTIONS_MAPPING.get(error.code, StatusCode.INTERNAL)
            return GrpcResponse(
                result=False,
                status_code=status_code,
                data={},
                message=error.details,
            )

        except Exception as error:
            # Handle unexpected exceptions
            logger.error(f"Internal server error: {error}")
            error_message = str(error)
            context.set_details(f"Internal server error: {error_message}")
            context.set_code(StatusCode.INTERNAL)
            return context
