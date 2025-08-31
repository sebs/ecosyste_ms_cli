"""Handler for sponsors API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class SponsorsOperationHandler(OperationHandler):
    """Handler for sponsors API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for sponsors API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        path_params = {}
        query_params = {}

        # Handle path parameters for specific operations
        if operation_id == "getAccount":
            # The login is a path parameter
            if args:
                path_params["login"] = args[0]
            elif "login" in kwargs:
                path_params["login"] = kwargs.pop("login")

        elif operation_id == "listAccountSponsors":
            # The login is a path parameter
            if args:
                path_params["login"] = args[0]
            elif "login" in kwargs:
                path_params["login"] = kwargs.pop("login")

        elif operation_id == "listAccountSponsorships":
            # The login is a path parameter
            if args:
                path_params["login"] = args[0]
            elif "login" in kwargs:
                path_params["login"] = kwargs.pop("login")

        # For all operations, remaining kwargs are query parameters
        for key, value in kwargs.items():
            if value is not None:
                query_params[key] = value

        return path_params, query_params
