# gRPC Plugin - Python Framework

A flexible Python framework for building gRPC servers with HTTP method routing, automatic request/response validation using Pydantic, and a clean decorator-based API.

## Features

- 🚀 **Simple Decorator API**: Define routes using Python decorators
- 📝 **Automatic Validation**: Built-in Pydantic model validation for requests and responses
- 🎯 **HTTP Method Support**: Supports GET, POST, PUT, DELETE methods
- 🔧 **Type Safe**: Full type hints support
- ⚡ **High Performance**: Built on top of gRPC for high-performance communication
- 🛡️ **Error Handling**: Comprehensive exception handling with detailed error messages

## Installation

```bash
pip install -r requirements.txt
```

### Dependencies

- `grpcio==1.76.0` - gRPC framework
- `protobuf>=6.33.0` - Protocol Buffers
- `pydantic>=2.12.3` - Data validation

## Getting Started

### 1. Define Your Service

Create a Python file for your service (e.g., `my_service.py`):

```python
from pydantic import BaseModel
from GrpcPluin import router, METHODS

# Define Pydantic models for request validation
class UserRequest(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# Register routes using decorators
@router(url="/users", methods=[METHODS.POST])
def create_user(user: UserRequest) -> dict:
    """Create a new user."""
    # Your business logic here
    return {
        "id": 1,
        "name": user.name,
        "email": user.email
    }

@router(url="/users/{id}", methods=[METHODS.GET])
def get_user(id: int) -> dict:
    """Get user by ID."""
    return {
        "id": id,
        "name": "John Doe",
        "email": "john@example.com"
    }

@router(url="/users", methods=[METHODS.GET])
def list_users() -> dict:
    """List all users."""
    return {"users": []}
```

### 2. Start the Server

In your main application file:

```python
from GrpcPluin import connector

if __name__ == "__main__":
    connector.install_app()
```

Run your server:

```bash
python my_service.py
```

The server will start on `0.0.0.0:50052` by default.

### 3. Create a Client

Create a client to interact with your service:

```python
from GrpcPluin.client import GrpcRequestHandler, Request, METHODS

# Initialize the handler
handler = GrpcRequestHandler()

# Make a POST request
request = Request(
    method=METHODS.POST,
    url="/users",
    body={
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
)

try:
    response = handler.call(request, grpc_url="0.0.0.0:50052")
    print(f"Result: {response['result']}")
    print(f"Data: {response['data']}")
except Exception as e:
    print(f"Error: {e}")
```

## API Reference

### Router Decorator

```python
@router(
    url: str,
    methods: list[METHODS] | None = None,
    response_model: type[BaseModel] | None = None
)
```

**Parameters:**
- `url`: URL path for the route (e.g., "/users" or "/users/{id}")
- `methods`: List of HTTP methods (POST, GET, PUT, DELETE). Defaults to [GET]
- `response_model`: Optional Pydantic model for response validation

### Request Handler Function

Handler functions receive request body data and return dictionary responses:

```python
def handler_function(param: ModelType) -> dict:
    # Process the request
    return {"key": "value"}
```

**Notes:**
- Function parameters should use Pydantic model types for automatic validation
- Return a dictionary with your response data
- If `response_model` is provided, the response will be validated against it

### Client Request

```python
from GrpcPluin.client import Request, METHODS

request = Request(
    method=METHODS.POST,  # or METHODS.GET, METHODS.PUT, METHODS.DELETE
    url="/users",
    body={"key": "value"}  # Dictionary of request data
)
```

### Client Response

```python
{
    "result": bool,      # Whether the request succeeded
    "status": int,       # HTTP status code
    "data": dict,        # Response data (optional)
    "message": str       # Error message (optional)
}
```

## Configuration

### Server Configuration

Modify server configuration in `GrpcPluin/__init__.py`:

```python
connector = GrpcConnector(
    server=server(thread_pool=futures.ThreadPoolExecutor(max_workers=10)),
    composers=[composer],
    configs=GrpcConfigs(server_uri="0.0.0.0:50052"),  # Change port here
)
```

### Middleware Support

Add middleware functions to the router:

```python
from GrpcPluin import router

@router.add_middleware
def my_middleware(request):
    # Pre-process request
    return request

# Routes will go through middleware before execution
```

## Protocol Buffers

The framework uses a simple protocol buffer definition for communication:

```protobuf
service GrpcHandler {
    rpc Dispatch(Request) returns (Response);
}

message Request {
    string url = 1;
    Method method = 2;
    google.protobuf.Struct body = 3;
}

message Response {
    bool result = 1;
    int64 status_code = 4;
    optional string message = 2;
    optional google.protobuf.Struct data = 3;
}
```

## Project Structure

```
GrpcPluin/
├── client/              # Client-side components
│   ├── caller.py       # Request handler
│   ├── structures.py   # Request/Response models
│   └── exceptions.py   # Client exceptions
├── Frame/              # Server-side framework
│   ├── router.py       # Route registration and dispatching
│   ├── manager.py      # gRPC server manager
│   ├── connector.py    # Server setup and configuration
│   ├── enums.py        # Enumerations and data structures
│   └── exceptions/     # Server exception handling
└── proto/             # Protocol buffer definitions
    ├── base_proto.proto
    ├── base_proto_pb2.py
    └── base_proto_pb2_grpc.py
```

## Error Handling

The framework provides comprehensive error handling:

- **NotFoundException**: Route not found
- **InvalidArgumentException**: Request validation failed
- **GrpcException**: gRPC communication errors

All errors include detailed messages and status codes.

## Examples

### Simple GET Endpoint

```python
@router(url="/hello")
def hello() -> dict:
    return {"message": "Hello, World!"}
```

### POST with Validation

```python
class CreateOrderRequest(BaseModel):
    product_id: int
    quantity: int
    customer_email: str

@router(url="/orders", methods=[METHODS.POST])
def create_order(order: CreateOrderRequest) -> dict:
    return {
        "order_id": 123,
        "total": order.quantity * 100
    }
```

### GET with Path Parameters

```python
@router(url="/users/{user_id}", methods=[METHODS.GET])
def get_user(user_id: int) -> dict:
    return {"id": user_id, "name": "John"}
```

### Response Validation

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@router(
    url="/users",
    methods=[METHODS.GET],
    response_model=UserResponse  # Validates response structure
)
def get_user() -> dict:
    return {"id": 1, "name": "John", "email": "john@example.com"}
```

## Testing

Create test files to test your endpoints:

```python
from GrpcPluin.client import GrpcRequestHandler, Request, METHODS

handler = GrpcRequestHandler()

# Test GET request
response = handler.call(
    Request(method=METHODS.GET, url="/users", body={}),
    grpc_url="0.0.0.0:50052"
)
```

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
