"""Server-side gRPC exceptions."""

from grpc import StatusCode


class BaseGrpcServerException(Exception):
    """Base exception for all gRPC server errors.

    Attributes:
        code: gRPC status code
        details: Error details message
    """

    code: StatusCode = StatusCode.UNKNOWN
    details: str = "An unknown error occurred"

    def __init__(self, details: str | None = None) -> None:
        """Initialize base gRPC server exception.

        Args:
            details: Optional custom error details
        """
        super().__init__(self.details)
        if details:
            self.details = details


class NotFoundException(BaseGrpcServerException):
    """Raised when a requested URL is not found."""

    code = StatusCode.NOT_FOUND
    details = "This URL was not found"


class InvalidArgumentException(BaseGrpcServerException):
    """Raised when request arguments are invalid."""

    code = StatusCode.INVALID_ARGUMENT
    details = "Invalid argument"

    def __init__(self, extra_details: str = "") -> None:
        """Initialize invalid argument exception.

        Args:
            extra_details: Additional error details
        """
        super().__init__()
        if extra_details:
            self.details = f"{self.details}: {extra_details}"


EXCEPTIONS_MAPPING = {
    StatusCode.NOT_FOUND: 404,
    StatusCode.INVALID_ARGUMENT: 400,
    StatusCode.INTERNAL: 500,
    StatusCode.UNAVAILABLE: 503,
    StatusCode.UNAUTHENTICATED: 401,
    StatusCode.RESOURCE_EXHAUSTED: 429,
    StatusCode.FAILED_PRECONDITION: 400,
    StatusCode.ABORTED: 409,
    StatusCode.OUT_OF_RANGE: 400,
    StatusCode.UNIMPLEMENTED: 501,
    StatusCode.OK: 200,
}
