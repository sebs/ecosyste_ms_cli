"""Base class for operation handlers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class OperationHandler(ABC):
    """Base class for operation handlers."""

    @abstractmethod
    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build path and query parameters for an operation.

        Args:
            operation_id: The operation ID to handle
            args: Positional arguments passed to the command
            kwargs: Keyword arguments passed to the command

        Returns:
            Tuple of (path_params, query_params)
        """
        pass

    def build_click_params(self, operation: dict) -> List:
        """Build Click parameter decorators from OpenAPI operation.

        Default implementation that can be overridden by specific handlers.

        Args:
            operation: OpenAPI operation definition

        Returns:
            List of Click parameter decorators
        """
        from ecosystems_cli.helpers.click_params import build_click_decorators

        parameters = operation.get("parameters", [])
        return build_click_decorators(parameters)
