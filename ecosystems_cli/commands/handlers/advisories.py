"""Handler for advisories API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class AdvisoriesOperationHandler(OperationHandler):
    """Handler for advisories API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for advisories API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        path_params = {}
        query_params = {}

        if operation_id == "getAdvisory":
            # The advisory UUID is a path parameter
            if args:
                path_params["advisoryUUID"] = args[0]
            elif "advisoryUUID" in kwargs:
                path_params["advisoryUUID"] = kwargs.pop("advisoryUUID")
            elif "advisoryuuid" in kwargs:
                # Handle lowercased version from click
                path_params["advisoryUUID"] = kwargs.pop("advisoryuuid")
        elif operation_id == "getAdvisories":
            # All parameters are query parameters
            for key, value in kwargs.items():
                if value is not None:
                    query_params[key] = value
        elif operation_id == "getAdvisoriesPackages":
            # No parameters for this operation
            pass

        return path_params, query_params
