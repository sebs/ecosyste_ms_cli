"""Handler for diff API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class DiffOperationHandler(OperationHandler):
    """Handler for diff API operations.

    Handles parameter mapping for diff API operations including:
    - createJob: Submit diff job with two URLs to compare
    - getJob: Get job status and results by job ID
    """

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for diff API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        handlers = {
            "createJob": self._handle_create_job,
            "getJob": self._handle_get_job,
        }

        handler = handlers.get(operation_id, self._handle_default)
        return handler(args, kwargs)

    def _handle_create_job(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle createJob operation parameters.

        Requires two URLs to compare. Can be provided as:
        - Positional arguments: diff create-job url1 url2
        - Named arguments: diff create-job --url-1 url1 --url-2 url2
        """
        query_params = {}

        if len(args) >= 2:
            query_params["url_1"] = args[0]
            query_params["url_2"] = args[1]
        else:
            # Try to get from kwargs
            url_1 = kwargs.get("url_1")
            url_2 = kwargs.get("url_2")

            if url_1:
                query_params["url_1"] = url_1
            if url_2:
                query_params["url_2"] = url_2

        # Note: API validation will handle missing required parameters
        return {}, query_params

    def _handle_get_job(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Handle getJob operation parameters."""
        path_params = {}

        job_id = args[0] if args else kwargs.get("job_id")
        if job_id:
            path_params["jobID"] = job_id

        return path_params, {}

    def _handle_default(self, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Default handler for unknown operations."""
        return {}, {}
