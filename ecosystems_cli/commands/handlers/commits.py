"""Handler for commits API operations."""

from typing import Any, Dict, Optional, Tuple

from .base import OperationHandler


class CommitsOperationHandler(OperationHandler):
    """Handler for commits API operations."""

    # CLI parameter names
    CLI_PARAM_HOST_NAME = "hostname"
    CLI_PARAM_REPO_NAME = "reponame"

    # OpenAPI parameter names
    API_PARAM_HOST_NAME = "hostName"
    API_PARAM_REPO_NAME = "repoName"

    def _extract_param(self, kwargs: dict, cli_name: str, api_name: str) -> Optional[str]:
        """Extract parameter from kwargs, trying both CLI and API names."""
        if api_name in kwargs:
            return kwargs.pop(api_name)
        elif cli_name in kwargs:
            return kwargs.pop(cli_name)
        return None

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for commits API operations.

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
                path_params[self.API_PARAM_HOST_NAME] = args[0]
            else:
                host_name = self._extract_param(kwargs, self.CLI_PARAM_HOST_NAME, self.API_PARAM_HOST_NAME)
                if host_name:
                    path_params[self.API_PARAM_HOST_NAME] = host_name

        elif operation_id == "getHostRepositories":
            # The host name is a path parameter
            if args:
                path_params[self.API_PARAM_HOST_NAME] = args[0]
            else:
                host_name = self._extract_param(kwargs, self.CLI_PARAM_HOST_NAME, self.API_PARAM_HOST_NAME)
                if host_name:
                    path_params[self.API_PARAM_HOST_NAME] = host_name

        elif operation_id == "getHostRepository":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repoName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repoName" in kwargs:
                    path_params["repoName"] = kwargs.pop("repoName")
                elif "reponame" in kwargs:
                    path_params["repoName"] = kwargs.pop("reponame")

        elif operation_id == "getRepositoryCommits":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repoName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repoName" in kwargs:
                    path_params["repoName"] = kwargs.pop("repoName")
                elif "reponame" in kwargs:
                    path_params["repoName"] = kwargs.pop("reponame")

        # For all operations, remaining kwargs are query parameters
        for key, value in kwargs.items():
            if value is not None:
                query_params[key] = value

        return path_params, query_params
