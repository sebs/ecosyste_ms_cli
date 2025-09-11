"""Handler for docker API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class DockerOperationHandler(OperationHandler):
    """Handler for docker API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for docker API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        handlers = {
            "getPackages": self._handle_query_params,
            "getPackage": self._handle_get_package,
            "getPackageVersions": self._handle_get_package_versions,
            "getPackageVersion": self._handle_get_package_version,
            "usage": self._handle_no_params,
            "usageEcosystem": self._handle_usage_ecosystem,
            "usagePackage": self._handle_usage_package,
        }

        handler = handlers.get(operation_id, self._handle_default)
        return handler(args, kwargs)

    def _handle_get_package(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getPackage operation parameters."""
        path_params = {}

        package_name = args[0] if args else kwargs.get("packageName")
        if package_name:
            path_params["packageName"] = package_name

        return path_params, {}

    def _handle_get_package_versions(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getPackageVersions operation parameters."""
        path_params = {}
        query_params = {}

        package_name = args[0] if args else kwargs.pop("packageName", None)
        if package_name:
            path_params["packageName"] = package_name

        # Add remaining kwargs as query parameters
        query_params.update({k: v for k, v in kwargs.items() if v is not None})

        return path_params, query_params

    def _handle_get_package_version(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getPackageVersion operation parameters."""
        path_params = {}

        if len(args) >= 2:
            path_params["packageName"] = args[0]
            path_params["versionNumber"] = args[1]
        else:
            if "packageName" in kwargs:
                path_params["packageName"] = kwargs["packageName"]
            if "versionNumber" in kwargs:
                path_params["versionNumber"] = kwargs["versionNumber"]

        return path_params, {}

    def _handle_usage_ecosystem(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle usageEcosystem operation parameters."""
        path_params = {}

        ecosystem = args[0] if args else kwargs.get("ecosystem")
        if ecosystem:
            path_params["ecosystem"] = ecosystem

        return path_params, {}

    def _handle_usage_package(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle usagePackage operation parameters."""
        path_params = {}

        if len(args) >= 2:
            path_params["ecosystem"] = args[0]
            path_params["package"] = args[1]
        else:
            if "ecosystem" in kwargs:
                path_params["ecosystem"] = kwargs["ecosystem"]
            if "package" in kwargs:
                path_params["package"] = kwargs["package"]

        return path_params, {}

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
