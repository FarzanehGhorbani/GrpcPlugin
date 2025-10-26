"""Data structures for gRPC client requests and responses."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class METHODS(str, Enum):
    """HTTP methods supported by the gRPC service."""

    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


@dataclass
class Request:
    """Client request structure.
    
    Attributes:
        method: HTTP method
        url: Request URL path
        body: Request body data as dictionary
    """
    method: METHODS
    url: str
    body: dict[str, Any]


@dataclass
class Response:
    """Client response structure.
    
    Attributes:
        result: Whether the request was successful
        status: HTTP status code
        data: Response data payload
        message: Optional response message
    """
    result: bool
    status: int
    data: Optional[dict[str, Any]] = None
    message: Optional[str] = None
