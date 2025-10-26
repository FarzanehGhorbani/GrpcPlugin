"""Connector for setting up gRPC server."""

from dataclasses import dataclass
from typing import Any, Callable, TypeVar

import grpc
from grpc._channel import Channel  # type: ignore
from grpc._server import _Server  # type: ignore


T = TypeVar("T")


class GrpcComposer:
    """Composer for setting up gRPC services.

    This class manages the connection between stub, servicer,
    and server for a gRPC service.
    """

    def __init__(
        self,
        stub: Callable[[Channel], T],
        servicer: Any,
        service_provider: Callable[[Any, _Server], None],
    ) -> None:
        """Initialize the gRPC composer.

        Args:
            stub: Stub factory function
            servicer: Service implementation
            service_provider: Function to register servicer with server
        """
        self.stub: Callable[[Channel], T] = stub
        self.servicer: Any = servicer
        self.service_provider: Callable[[Any, _Server], None] = service_provider

    def add_servicer_to_server(self, server: _Server) -> None:
        """Add the servicer to the server.

        Args:
            server: gRPC server instance
        """
        self.service_provider(self.servicer, server)

    def get_stub(self, channel: Channel) -> Any:
        """Create a stub from a channel.

        Args:
            channel: gRPC channel

        Returns:
            Stub instance
        """
        return self.stub(channel)

    @staticmethod
    def get_channel(uri: str) -> Channel:
        """Create an insecure channel to the specified URI.

        Args:
            uri: Server URI (host:port)

        Returns:
            gRPC channel
        """
        return grpc.insecure_channel(uri)


@dataclass
class GrpcConfigs:
    """Configuration for gRPC server."""

    server_uri: str


class GrpcConnector:
    """Connector for managing gRPC server lifecycle.

    This class handles the setup and startup of a gRPC server,
    registering services and managing the server process.
    """

    def __init__(
        self,
        server: _Server,
        composers: list[GrpcComposer],
        configs: GrpcConfigs,
    ) -> None:
        """Initialize the gRPC connector.

        Args:
            server: gRPC server instance
            composers: List of service composers
            configs: Server configuration
        """
        self.server: _Server = server
        self.composers: list[GrpcComposer] = composers
        self.configs: GrpcConfigs = configs

    def _connect(self) -> None:
        """Register services and start the server."""
        # Register all service composers
        for composer in self.composers:
            composer.service_provider(composer.servicer, self.server)

        # Add port and start server
        self.server.add_insecure_port(self.configs.server_uri)
        self.server.start()

        print(f"gRPC server started on {self.configs.server_uri}")
        self.server.wait_for_termination()

    def install_app(self) -> None:
        """Install and start the gRPC application."""
        self._connect()
