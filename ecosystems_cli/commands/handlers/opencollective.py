"""Handler for opencollective API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class OpenCollectiveOperationHandler(OperationHandler):
    """Handler for opencollective API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for opencollective API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        handlers = {
            "getProjects": self._handle_query_params,
            "getProject": self._handle_get_project,
            "lookupProject": self._handle_lookup_project,
            "getProjectPackages": self._handle_no_params,
            "getCollectives": self._handle_query_params,
            "getCollective": self._handle_get_collective,
            "getCollectiveProjects": self._handle_get_collective_projects,
        }

        handler = handlers.get(operation_id, self._handle_default)
        return handler(args, kwargs)

    def _handle_get_project(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getProject operation parameters."""
        path_params = {}

        project_id = args[0] if args else kwargs.get("id")
        if project_id:
            path_params["id"] = project_id

        return path_params, {}

    def _handle_get_collective(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getCollective operation parameters."""
        path_params = {}

        collective_id = args[0] if args else kwargs.get("id")
        if collective_id:
            path_params["id"] = collective_id

        return path_params, {}

    def _handle_get_collective_projects(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getCollectiveProjects operation parameters."""
        path_params = {}

        slug = args[0] if args else kwargs.get("slug")
        if slug:
            path_params["slug"] = slug

        return path_params, {}

    def _handle_lookup_project(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle lookupProject operation parameters."""
        query_params = {}

        url = args[0] if args else kwargs.get("url")
        if url:
            query_params["url"] = url

        return {}, query_params

    def _handle_query_params(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle operations that only have query parameters."""
        query_params = {k: v for k, v in kwargs.items() if v is not None}
        return {}, query_params

    def _handle_no_params(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle operations with no parameters."""
        return {}, {}

    def _handle_default(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Default handler for unknown operations."""
        return {}, {}
