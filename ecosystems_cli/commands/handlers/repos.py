"""Handler for repos API operations."""

from typing import Any, Dict, List, Optional, Tuple

from .base import OperationHandler


class ReposOperationHandler(OperationHandler):
    """Handler for repos API operations."""

    # Operation parameter configuration
    # Maps operation_id -> list of (api_param_name, lowercase_variants)
    OPERATION_PARAMS = {
        "topic": [("topic", ["topic"])],
        "getHost": [("hostName", ["hostname"])],
        "getHostOwners": [("hostName", ["hostname"])],
        "lookupHostOwner": [("HostName", ["hostname"])],
        "getHostOwner": [("hostName", ["hostname"]), ("ownerLogin", ["ownerlogin"])],
        "getHostOwnerRepositories": [("hostName", ["hostname"]), ("ownerLogin", ["ownerlogin"])],
        "getHostRepositories": [("hostName", ["hostname"])],
        "getHostRepositoryNames": [("hostName", ["hostname"])],
        "getHostOwnerNames": [("hostName", ["hostname"])],
        "getHostRepository": [("hostName", ["hostname"]), ("repositoryName", ["repositoryname"])],
        "getHostRepositoryManifests": [("hostName", ["hostname"]), ("repositoryName", ["repositoryname"])],
        "getHostRepositoryTags": [("hostName", ["hostname"]), ("repositoryName", ["repositoryname"])],
        "getHostRepositoryTag": [("hostName", ["hostname"]), ("repositoryName", ["repositoryname"]), ("tag", ["tag"])],
        "getHostRepositoryTagManifests": [("hostName", ["hostname"]), ("repositoryName", ["repositoryname"]), ("tag", ["tag"])],
        "getHostRepositoryReleases": [("hostName", ["hostname"]), ("repositoryName", ["repositoryname"])],
        "getHostRepositorySbom": [("hostName", ["hostname"]), ("repositoryName", ["repositoryname"])],
        "getHostRepositoryRelease": [
            ("hostName", ["hostname"]),
            ("repositoryName", ["repositoryname"]),
            ("release", ["release"]),
        ],
        "usageEcosystem": [("ecosystem", ["ecosystem"])],
        "usagePackage": [("ecosystem", ["ecosystem"]), ("package", ["package"])],
        "usagePackageDependencies": [("ecosystem", ["ecosystem"]), ("package", ["package"])],
    }

    def _extract_param(self, kwargs: dict, api_name: str, lowercase_variants: List[str]) -> Optional[str]:
        """Extract parameter from kwargs, trying API name first, then lowercase variants.

        Args:
            kwargs: Keyword arguments dict
            api_name: The API parameter name (exact case)
            lowercase_variants: List of lowercase parameter name variants to try

        Returns:
            Parameter value if found, None otherwise
        """
        # Try exact API name first
        if api_name in kwargs:
            return kwargs.pop(api_name)

        # Try lowercase variants
        for variant in lowercase_variants:
            if variant in kwargs:
                return kwargs.pop(variant)

        return None

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for repos API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        path_params = {}
        query_params = {}

        # Get parameter configuration for this operation
        param_config = self.OPERATION_PARAMS.get(operation_id, [])

        # Extract path parameters from args or kwargs
        for i, (api_name, lowercase_variants) in enumerate(param_config):
            if i < len(args):
                # Use positional argument
                path_params[api_name] = args[i]
            else:
                # Try to extract from kwargs
                value = self._extract_param(kwargs, api_name, lowercase_variants)
                if value is not None:
                    path_params[api_name] = value

        # For all operations, remaining kwargs are query parameters
        for key, value in kwargs.items():
            if value is not None:
                query_params[key] = value

        return path_params, query_params
