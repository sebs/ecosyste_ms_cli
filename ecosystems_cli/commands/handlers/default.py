"""Default handler for standard API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class DefaultOperationHandler(OperationHandler):
    """Default handler for standard API operations."""

    # Configuration mapping: operation_id -> (param_type, param_name, arg_count)
    OPERATION_CONFIG = {
        "getProject": ("path", "id", 1),
        "getList": ("path", "id", 1),
        "getListProjects": ("path", "id", 1),
        "getCollection": ("path", "id", 1),
        "getCollectionProjects": ("path", "id", 1),
        "getTopic": ("path", "slug", 1),
        "getCollective": ("path", "id", 1),
        "getCollectiveProjects": ("path", "slug", 1),
        "lookupProject": ("query", "url", 1),
        "createJob": ("query", "url", 1),
        "getJob": ("path", "jobID", 1),
    }

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for standard API operations."""
        all_args = list(args) + list(kwargs.values())

        config = self.OPERATION_CONFIG.get(operation_id)
        if config and len(all_args) >= config[2]:
            param_type, param_name, _ = config
            value = all_args[0]

            if param_type == "path":
                return {param_name: value}, {}
            elif param_type == "query":
                return {}, {param_name: value}

        return {}, {}
