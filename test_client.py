"""Example gRPC client implementation."""

from GrpcPluin.client.caller import GrpcRequestHandler
from GrpcPluin.client.structures import METHODS, Request


def main() -> None:
    """Main function to test gRPC client."""
    handler = GrpcRequestHandler()

    result = handler.call(
        request=Request(
            method=METHODS.POST,
            url="/text/",
            body={"name": "far", "family": "ghorbani", "age": 4},
        )
    )

    print(result)


if __name__ == "__main__":
    main()
