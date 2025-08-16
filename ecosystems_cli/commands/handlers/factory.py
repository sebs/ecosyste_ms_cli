"""Factory for creating operation handlers."""

from typing import Dict, Type

from .advisories import AdvisoriesOperationHandler
from .archives import ArchivesOperationHandler
from .base import OperationHandler
from .default import DefaultOperationHandler
from .packages import PackagesOperationHandler
from .resolver import ResolverOperationHandler


class OperationHandlerFactory:
    """Factory for creating operation handlers."""

    _handlers: Dict[str, Type[OperationHandler]] = {
        "advisories": AdvisoriesOperationHandler,
        "packages": PackagesOperationHandler,
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
