"""Handler for dependabot API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class DependabotOperationHandler(OperationHandler):
    """Handler for dependabot API operations.

    Handles parameter mapping for dependabot API operations including:
    - Package operations: getPackages, getPackage, getEcosystemPackages
    - Repository operations: getHost, getHostRepository, getHostRepositoryIssues
    - Advisory operations: getAdvisories, getAdvisory
    - Lookup operations: repositoriesLookup

    Supports hierarchical path parameters like /hosts/{hostName}/repositories/{repoName}/issues/{issueNumber}
    """

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for dependabot API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        handlers = {
            "getPackages": self._handle_query_params,
            "getPackageEcosystems": self._handle_no_params,
            "getEcosystemPackages": self._handle_ecosystem_packages,
            "getPackage": self._handle_get_package,
            "getIssuePackages": self._handle_issue_packages,
            "repositoriesLookup": self._handle_repositories_lookup,
            "getRegistries": self._handle_query_params,
            "getHost": self._handle_get_host,
            "getHostRepositories": self._handle_host_repositories,
            "getHostRepository": self._handle_host_repository,
            "getHostRepositoryIssues": self._handle_host_repository_issues,
            "getHostRepositoryIssue": self._handle_host_repository_issue,
            "getAdvisories": self._handle_query_params,
            "getAdvisory": self._handle_get_advisory,
        }

        handler = handlers.get(operation_id, self._handle_default)
        return handler(args, kwargs)

    def _handle_ecosystem_packages(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getEcosystemPackages operation parameters."""
        path_params = {}
        query_params = {}

        ecosystem = args[0] if args else kwargs.pop("ecosystem", None)
        if ecosystem:
            path_params["ecosystem"] = ecosystem

        # Add remaining kwargs as query parameters
        query_params.update({k: v for k, v in kwargs.items() if v is not None})

        return path_params, query_params

    def _handle_get_package(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getPackage operation parameters."""
        path_params = {}

        if len(args) >= 2:
            path_params["ecosystem"] = args[0]
            path_params["name"] = args[1]
        else:
            if "ecosystem" in kwargs:
                path_params["ecosystem"] = kwargs["ecosystem"]
            if "name" in kwargs:
                path_params["name"] = kwargs["name"]

        return path_params, {}

    def _handle_issue_packages(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getIssuePackages operation parameters."""
        path_params = {}

        issue_id = args[0] if args else kwargs.get("issueId")
        if issue_id:
            path_params["issueId"] = issue_id

        return path_params, {}

    def _handle_repositories_lookup(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle repositoriesLookup operation parameters."""
        query_params = {}

        url = args[0] if args else kwargs.get("url")
        if url:
            query_params["url"] = url

        return {}, query_params

    def _handle_get_host(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getHost operation parameters."""
        path_params = {}
        query_params = {}

        host_name = args[0] if args else kwargs.pop("hostName", None)
        if host_name:
            path_params["hostName"] = host_name

        # Add remaining kwargs as query parameters
        query_params.update({k: v for k, v in kwargs.items() if v is not None})

        return path_params, query_params

    def _handle_host_repositories(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getHostRepositories operation parameters."""
        path_params = {}
        query_params = {}

        host_name = args[0] if args else kwargs.pop("hostName", None)
        if host_name:
            path_params["hostName"] = host_name

        # Add remaining kwargs as query parameters
        query_params.update({k: v for k, v in kwargs.items() if v is not None})

        return path_params, query_params

    def _handle_host_repository(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getHostRepository operation parameters."""
        path_params = {}

        if len(args) >= 2:
            path_params["hostName"] = args[0]
            path_params["repoName"] = args[1]
        else:
            if "hostName" in kwargs:
                path_params["hostName"] = kwargs["hostName"]
            if "repoName" in kwargs:
                path_params["repoName"] = kwargs["repoName"]

        return path_params, {}

    def _handle_host_repository_issues(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getHostRepositoryIssues operation parameters."""
        path_params = {}
        query_params = {}

        if len(args) >= 2:
            path_params["hostName"] = args[0]
            path_params["repoName"] = args[1]
        else:
            if "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            if "repoName" in kwargs:
                path_params["repoName"] = kwargs.pop("repoName")

        # Add remaining kwargs as query parameters
        query_params.update({k: v for k, v in kwargs.items() if v is not None})

        return path_params, query_params

    def _handle_host_repository_issue(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getHostRepositoryIssue operation parameters."""
        path_params = {}

        if len(args) >= 3:
            path_params["hostName"] = args[0]
            path_params["repoName"] = args[1]
            path_params["issueNumber"] = args[2]
        else:
            if "hostName" in kwargs:
                path_params["hostName"] = kwargs["hostName"]
            if "repoName" in kwargs:
                path_params["repoName"] = kwargs["repoName"]
            if "issueNumber" in kwargs:
                path_params["issueNumber"] = kwargs["issueNumber"]

        return path_params, {}

    def _handle_get_advisory(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getAdvisory operation parameters."""
        path_params = {}
        query_params = {}

        advisory_id = args[0] if args else kwargs.pop("advisoryId", None)
        if advisory_id:
            path_params["advisoryId"] = advisory_id

        # Add remaining kwargs as query parameters
        query_params.update({k: v for k, v in kwargs.items() if v is not None})

        return path_params, query_params

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
