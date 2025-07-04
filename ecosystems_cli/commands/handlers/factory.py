"""Factory for creating operation handlers."""

from .archives import ArchivesOperationHandler
from .base import OperationHandler
from .default import DefaultOperationHandler
from .resolver import ResolverOperationHandler


class OperationHandlerFactory:
    """Factory for creating operation handlers."""

    _handlers = {
        "resolver": ResolverOperationHandler,
        "archives": ArchivesOperationHandler,
    }

    @classmethod
    def get_handler(cls, api_name: str) -> OperationHandler:
        """Get the appropriate handler for an API.

        Args:
            api_name: Name of the API

        Returns:
            OperationHandler instance for the API
        """
        handler_class = cls._handlers.get(api_name, DefaultOperationHandler)
        return handler_class()
