"""Enumerations and data structures for the gRPC frame."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from pydantic import BaseModel


class METHODS(str, Enum):
    """HTTP methods supported by the gRPC service."""

    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


@dataclass
class FunctionDetails:
    """Details about a registered route handler function.

    Attributes:
        func: The handler function to call
        response_model: Optional Pydantic model for response validation
    """

    func: Callable
    response_model: Optional[type[BaseModel]] = None
