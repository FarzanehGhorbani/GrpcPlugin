"""Response data structures for gRPC server."""

from dataclasses import dataclass, field
from typing import Any

# Note: This file contains a custom StatusCode enum that seems redundant
# with grpc.StatusCode. Consider removing it and using grpc.StatusCode directly.


@dataclass
class GrpcResponse:
    """Server response structure.

    Attributes:
        status_code: HTTP status code (default: 200)
        result: Whether the operation was successful (default: True)
        detail: Response detail data
        message: Optional response message
        errors: Dictionary of error information
    """

    status_code: int = 200
    result: bool = True
    detail: dict[str, Any] = field(default_factory=dict)
    message: str | None = None
    errors: dict[str, Any] = field(default_factory=dict)
