"""Base class for operation handlers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


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
