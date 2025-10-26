"""Exception handling for gRPC client errors."""

import re
import grpc
from datetime import datetime


class GrpcException(Exception):
    """Custom exception for gRPC client errors.

    Attributes:
        url: The URL that caused the error
        status_code: gRPC status code
        details: Error details message
        created_time: Timestamp when the error was created
    """

    def __init__(
        self,
        url: str,
        status_code: grpc.StatusCode,
        details: str | None,
        debug_error_string: str,
    ) -> None:
        """Initialize gRPC exception.

        Args:
            url: The URL that caused the error
            status_code: gRPC status code from the error
            details: Error details message
            debug_error_string: Full debug error string
        """
        super().__init__(details)
        self.url: str = url
        self.status_code: grpc.StatusCode = status_code
        self.details: str | None = details
        self.created_time: datetime = self._parse_created_time(debug_error_string)

    @staticmethod
    def _parse_created_time(error_string: str) -> datetime:
        """Parse created_time from debug error string.

        Args:
            error_string: Debug error string containing timestamp

        Returns:
            Parsed datetime object

        Raises:
            ValueError: If timestamp cannot be parsed
        """
        pattern = r'created_time:"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})'
        match = re.search(pattern, error_string)

        if match is None:
            return datetime.now()

        time_str = match.group(1)
        return datetime.fromisoformat(time_str)

    def __str__(self) -> str:
        """Return formatted error message."""
        return (
            f"gRPC Error:\n"
            f"  URL: {self.url}\n"
            f"  Status Code: {self.status_code}\n"
            f"  Details: {self.details}\n"
            f"  Created Time: {self.created_time}"
        )
