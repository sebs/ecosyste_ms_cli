"""Handler for issues API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class IssuesOperationHandler(OperationHandler):
    """Handler for issues API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for issues API operations.

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
        if operation_id == "getHost":
            # The host name is a path parameter
            if args:
                path_params["hostName"] = args[0]
            elif "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            elif "hostname" in kwargs:
                path_params["hostName"] = kwargs.pop("hostname")

        elif operation_id == "getHostRepositories":
            # The host name is a path parameter
            if args:
                path_params["hostName"] = args[0]
            elif "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            elif "hostname" in kwargs:
                path_params["hostName"] = kwargs.pop("hostname")

        elif operation_id == "getHostRepository":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")

        elif operation_id == "getHostRepositoryIssues":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")

        elif operation_id == "getHostRepositoryIssue":
            # The host name, repository name, and issue number are path parameters
            if len(args) >= 3:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
                path_params["issueNumber"] = args[2]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")
                if "issueNumber" in kwargs:
                    path_params["issueNumber"] = kwargs.pop("issueNumber")
                elif "issuenumber" in kwargs:
                    path_params["issueNumber"] = kwargs.pop("issuenumber")
                elif "issue_number" in kwargs:
                    path_params["issueNumber"] = kwargs.pop("issue_number")

        # For all operations, remaining kwargs are query parameters
        for key, value in kwargs.items():
            if value is not None:
                query_params[key] = value

        return path_params, query_params
