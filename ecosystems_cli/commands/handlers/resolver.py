"""Handler for resolver API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class ResolverOperationHandler(OperationHandler):
    """Handler for resolver API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for resolver API operations."""
        # Special handling for createJob which has multiple parameters
        if operation_id == "createJob" and len(args) >= 2:
            query_params = {"package_name": args[0], "registry": args[1]}
            if kwargs.get("before"):
                query_params["before"] = kwargs["before"]
            if kwargs.get("version"):
                query_params["version"] = kwargs["version"]
            return {}, query_params

        # Configuration for simple operations
        operation_config = {
            "getJob": ("path", {"jobID": 0}, 1),
        }

        config = operation_config.get(operation_id)
        if config:
            param_type, param_mapping, required_args = config
            if len(args) >= required_args:
                if param_type == "path":
                    path_params = {name: args[idx] for name, idx in param_mapping.items()}
                    return path_params, {}

        return {}, {}
