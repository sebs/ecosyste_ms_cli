"""Docker API operation handler."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class DockerOperationHandler(OperationHandler):
    """Handler for docker API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for docker API operations."""
        path_params = {}
        query_params = {}
        all_args = list(args) + list(kwargs.values())

        if operation_id == "getPackage" and len(all_args) >= 1:
            path_params["packageName"] = all_args[0]
        elif operation_id == "getPackageVersions" and len(all_args) >= 1:
            path_params["packageName"] = all_args[0]
        elif operation_id == "getPackageVersion" and len(all_args) >= 2:
            path_params["packageName"] = all_args[0]
            path_params["versionNumber"] = all_args[1]
        elif operation_id == "usageEcosystem" and len(all_args) >= 1:
            path_params["ecosystem"] = all_args[0]
        elif operation_id == "usagePackage" and len(all_args) >= 2:
            path_params["ecosystem"] = all_args[0]
            path_params["package"] = all_args[1]

        return path_params, query_params
