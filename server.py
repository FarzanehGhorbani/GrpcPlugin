"""Example gRPC server implementation."""

from GrpcPluin import METHODS, connector, router
from pydantic import BaseModel


class Name(BaseModel):
    """Name model for user name."""

    name: str


class Family(BaseModel):
    """Family model for user family."""

    family: str


class ResponseModel(BaseModel):
    """Response model for the endpoint."""

    name: str
    family: str
    age: int


@router(url="/text/", methods=[METHODS.POST], response_model=ResponseModel)
def get(name: Name, family: Family, age: int) -> dict:
    """Example handler function.

    Args:
        name: User's name
        family: User's family name
        age: User's age

    Returns:
        Response dictionary
    """
    # print("get")
    # raise Exception("Example exception")
    return {"name": "far", "family": "ghorbani", "age": age}


if __name__ == "__main__":
    connector.install_app()
