"""Base exception handler for gRPC server exceptions."""

from typing import Any


class BaseExceptionHandler:
    """Base class for custom exception handlers.

    This is a placeholder for custom exception handling logic.
    Subclasses should implement the handle method.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize exception handler."""
        pass

    def handle(self, exception: Exception) -> Any:
        """Handle an exception.

        Args:
            exception: The exception to handle

        Returns:
            Processed exception or response

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError("Each exception handler must define a handle method")
