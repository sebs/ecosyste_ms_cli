"""Handler for archives API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class ArchivesOperationHandler(OperationHandler):
    """Handler for archives API operations."""

    # Configuration: operation_id -> (param_names, required_args_count)
    OPERATION_CONFIG = {
        "list": (["url"], 1),
        "readme": (["url"], 1),
        "changelog": (["url"], 1),
        "repopack": (["url"], 1),
        "contents": (["url", "path"], 2),
    }

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for archives API operations."""
        config = self.OPERATION_CONFIG.get(operation_id)

        if config:
            param_names, required_args = config
            query_params = {}

            # Try to build from positional args first
            if len(args) >= required_args:
                for i, param_name in enumerate(param_names[: len(args)]):
                    query_params[param_name] = args[i]
                return {}, query_params

            # Fall back to kwargs
            if all(param in kwargs for param in param_names):
                for param_name in param_names:
                    query_params[param_name] = kwargs[param_name]
                return {}, query_params

        return {}, {}
