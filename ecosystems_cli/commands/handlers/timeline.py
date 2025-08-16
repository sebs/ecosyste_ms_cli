"""Handler for timeline API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class TimelineOperationHandler(OperationHandler):
    """Handler for timeline API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for timeline API operations.

        Args:
            operation_id: The operation ID
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        path_params = {}
        query_params = {}

        if operation_id == "getEvents":
            # Handle pagination parameters - only add if not None
            if kwargs.get("page") is not None:
                query_params["page"] = kwargs["page"]
            if kwargs.get("per_page") is not None:
                query_params["per_page"] = kwargs["per_page"]

        elif operation_id == "getEvent":
            # Handle repository name from kwargs (path params become kwargs in Click)
            # Click converts argument names to lowercase
            if "repoName" in kwargs:
                path_params["repoName"] = kwargs["repoName"]
            elif "reponame" in kwargs:
                path_params["repoName"] = kwargs["reponame"]
            # Handle pagination - only add if not None
            if kwargs.get("page") is not None:
                query_params["page"] = kwargs["page"]
            if kwargs.get("per_page") is not None:
                query_params["per_page"] = kwargs["per_page"]

        return path_params, query_params
