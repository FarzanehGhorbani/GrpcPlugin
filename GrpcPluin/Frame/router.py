"""Router for handling gRPC server routes."""

from typing import Any, Callable

from pydantic import BaseModel, ValidationError

from .enums import FunctionDetails, METHODS
from .exceptions.exceptions import NotFoundException, InvalidArgumentException


class GrpcRouter:
    """Router for registering and dispatching gRPC routes.

    This router manages route registration, argument validation,
    and function invocation for gRPC server requests.
    """

    def __init__(self) -> None:
        """Initialize the router with empty routes and middlewares."""
        self.routes: dict[str, dict[str, FunctionDetails]] = {
            "GET": {},
            "PUT": {},
            "DELETE": {},
            "POST": {},
        }
        self.middlewares: list[Callable] = []

    def __call__(
        self,
        url: str,
        methods: list[METHODS] | None = None,
        response_model: type[BaseModel] | None = None,
    ) -> Callable:
        """Decorator to register a route handler.

        Args:
            url: URL path for the route
            methods: List of HTTP methods (default: [GET])
            response_model: Optional Pydantic model for response validation

        Returns:
            Decorator function

        Example:
            @router(url="/users", methods=[METHODS.POST])
            def create_user(user: User):
                return {"id": 1}
        """
        if methods is None:
            methods = [METHODS.GET]

        def decorator(func: Callable) -> Callable:
            """Inner decorator that registers the function."""
            for method in methods:
                self.routes[method.value][url] = FunctionDetails(
                    func=func, response_model=response_model
                )
            return func

        return decorator

    def _routing(self, method: str, url: str) -> FunctionDetails:
        """Find a registered route handler.

        Args:
            method: HTTP method as string
            url: URL path

        Returns:
            Function details for the route

        Raises:
            NotFoundException: If the route is not found
        """
        try:
            return self.routes[method][url]
        except KeyError:
            raise NotFoundException(f"No handler found for {method} {url}")

    def _declare_function_argument(self, func: Callable, request_data: dict) -> dict:
        """Extract and validate function arguments from request data.

        Args:
            func: Handler function
            request_data: Request body data as dictionary

        Returns:
            Dictionary of validated arguments

        Raises:
            InvalidArgumentException: If validation fails
        """
        try:
            func_params: dict[str, Any] = {}
            annotations = getattr(func, "__annotations__", {})

            for key, annotation_type in annotations.items():
                # Skip 'return' annotation
                if key == "return":
                    continue

                # Check if it's a Pydantic model
                if self._is_pydantic_model(annotation_type):
                    func_params[key] = annotation_type(**request_data)
                elif key in request_data:
                    func_params[key] = annotation_type(request_data[key])

            return func_params

        except ValidationError as error:
            error_details = error.json()
            raise InvalidArgumentException(f"Validation failed:\n{error_details}")

    @staticmethod
    def _is_pydantic_model(cls: type) -> bool:
        """Check if a class is a Pydantic model.

        Args:
            cls: Class to check

        Returns:
            True if it's a Pydantic model
        """
        return isinstance(cls, type) and issubclass(cls, BaseModel)

    def _call(self, func: Callable, request_data: dict) -> Any:
        """Call a handler function with request data.

        Args:
            func: Handler function to call
            request_data: Dictionary of function arguments

        Returns:
            Function return value
        """
        return func(**request_data)

    def add_middleware(self, func: Callable) -> None:
        """Add middleware function.

        Args:
            func: Middleware function to add
        """
        self.middlewares.append(func)
