"""Factory for creating operation handlers."""

from typing import Dict, Type

from .advisories import AdvisoriesOperationHandler
from .archives import ArchivesOperationHandler
from .base import OperationHandler
from .commits import CommitsOperationHandler
from .default import DefaultOperationHandler
from .issues import IssuesOperationHandler
from .packages import PackagesOperationHandler
from .repos import ReposOperationHandler
from .resolver import ResolverOperationHandler
from .sponsors import SponsorsOperationHandler
from .timeline import TimelineOperationHandler


class OperationHandlerFactory:
    """Factory for creating operation handlers."""

    _handlers: Dict[str, Type[OperationHandler]] = {
        "advisories": AdvisoriesOperationHandler,
        "commits": CommitsOperationHandler,
        "issues": IssuesOperationHandler,
        "packages": PackagesOperationHandler,
        "repos": ReposOperationHandler,
        "resolver": ResolverOperationHandler,
        "archives": ArchivesOperationHandler,
        "sponsors": SponsorsOperationHandler,
        "timeline": TimelineOperationHandler,
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
