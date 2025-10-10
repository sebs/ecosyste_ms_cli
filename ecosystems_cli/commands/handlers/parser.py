"""Handler for parser API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class ParserOperationHandler(OperationHandler):
    """Handler for parser API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for parser API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        handlers = {
            "createJob": self._handle_create_job,
            "jobFormats": self._handle_no_params,
            "getJob": self._handle_get_job,
        }

        handler = handlers.get(operation_id, self._handle_default)
        return handler(args, kwargs)

    def _handle_create_job(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle createJob operation parameters."""
        query_params = {}

        url = args[0] if args else kwargs.get("url")
        if url:
            query_params["url"] = url

        return {}, query_params

    def _handle_get_job(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getJob operation parameters."""
        path_params = {}

        # Try multiple parameter name variations
        job_id = args[0] if args else kwargs.get("jobID") or kwargs.get("jobid") or kwargs.get("job_id")
        if job_id:
            path_params["jobID"] = job_id

        return path_params, {}

    def _handle_no_params(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle operations with no parameters."""
        return {}, {}

    def _handle_default(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Default handler for unknown operations."""
        return {}, {}
