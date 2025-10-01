"""Bravado-based API client for ecosystems CLI."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from bravado.client import SwaggerClient
from bravado.exception import (
    HTTPBadRequest,
    HTTPForbidden,
    HTTPNotFound,
    HTTPServerError,
    HTTPTooManyRequests,
    HTTPUnauthorized,
)
from bravado_core.exception import SwaggerValidationError

from ecosystems_cli import __version__
from ecosystems_cli.constants import (
    API_BASE_URL_TEMPLATE,
    API_SPECS_DIR,
    DEFAULT_TIMEOUT,
    OPENAPI_FILE_EXTENSION,
)
from ecosystems_cli.exceptions import (
    APIAuthenticationError,
    APIConnectionError,
    APIHTTPError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
    APITimeoutError,
    InvalidAPIError,
    InvalidOperationError,
)


class BravadoClientFactory:
    """Factory for creating and managing Bravado API clients."""

    def __init__(self, specs_dir: Optional[Path] = None):
        """Initialize the factory.

        Args:
            specs_dir: Directory containing OpenAPI specs. Defaults to project's apis directory.
        """
        if specs_dir is None:
            specs_dir = Path(__file__).parent.parent / API_SPECS_DIR
        self.specs_dir = Path(specs_dir)
        self._clients: Dict[str, SwaggerClient] = {}
        self._specs: Dict[str, Dict[str, Any]] = {}
        self._operation_map: Dict[str, Dict[str, Any]] = {}

    def _discover_apis(self) -> List[str]:
        """Discover all available API specs."""
        if not self.specs_dir.exists():
            return []
        # Extract API name from filename by removing extension
        # e.g., "test.openapi.yaml" -> "test"
        return [f.name.replace(OPENAPI_FILE_EXTENSION, "") for f in self.specs_dir.glob(f"*{OPENAPI_FILE_EXTENSION}")]

    def _get_default_base_url(self, api_name: str, spec: Dict[str, Any]) -> str:
        """Get default base URL from OpenAPI specification."""
        servers = spec.get("servers", [])
        if servers and "url" in servers[0]:
            return servers[0]["url"]
        return API_BASE_URL_TEMPLATE.format(api_name=api_name)

    def _build_operation_map(self, api_name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Build operation ID to path/method mapping."""
        operation_map = {}
        paths = spec.get("paths", {})

        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.lower() in ["get", "post", "put", "delete", "patch"]:
                    operation_id = operation.get("operationId")
                    if operation_id:
                        operation_map[operation_id] = {
                            "path": path,
                            "method": method.upper(),
                            "operation": operation,
                            "summary": operation.get("summary", ""),
                            "description": operation.get("description", ""),
                        }

        return operation_map

    def get_client(
        self,
        api_name: str,
        base_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        mailto: Optional[str] = None,
    ) -> SwaggerClient:
        """Get or create a Bravado client for the specified API.

        Args:
            api_name: Name of the API
            base_url: Override base URL
            timeout: Request timeout in seconds
            mailto: Email for polite pool access

        Returns:
            Configured SwaggerClient instance

        Raises:
            InvalidAPIError: If API spec not found
        """
        cache_key = f"{api_name}:{base_url}:{timeout}:{mailto}"

        if cache_key in self._clients:
            return self._clients[cache_key]

        # Load spec file
        spec_path = self.specs_dir / f"{api_name}{OPENAPI_FILE_EXTENSION}"
        if not spec_path.exists():
            raise InvalidAPIError(api_name)

        # Build user agent
        user_agent = f"ecosyste_ms_cli ({__version__})"
        if mailto:
            user_agent += f" mailto:{mailto}"

        # Configure Bravado
        config = {
            "validate_requests": True,
            "validate_responses": False,
            "use_models": True,
            "formats": [],
        }

        request_headers = {
            "User-Agent": user_agent,
        }

        # Load spec file
        try:
            import yaml

            with open(spec_path, "r") as f:
                spec_dict = yaml.safe_load(f)
        except FileNotFoundError:
            raise InvalidAPIError(api_name)
        except Exception as e:
            raise APIConnectionError(f"Failed to load spec for {api_name}: {str(e)}")

        # Create client using from_spec
        try:
            # Determine origin URL (base URL from spec or override)
            origin_url = base_url if base_url else self._get_default_base_url(api_name, spec_dict)

            # Create client from spec dict
            client = SwaggerClient.from_spec(
                spec_dict=spec_dict,
                origin_url=origin_url,
                config=config,
                http_client=None,
            )

            # Set request headers on the client's http_client
            if hasattr(client.swagger_spec, "http_client") and client.swagger_spec.http_client:
                client.swagger_spec.http_client.set_basic_auth = lambda *args: None
                for header_name, header_value in request_headers.items():
                    client.swagger_spec.http_client.set_api_key(
                        host="", api_key=header_value, param_name=header_name, param_in="header"
                    )

            # Override base URL if specified
            if base_url:
                client.swagger_spec.api_url = base_url

            # Cache client and spec
            self._clients[cache_key] = client
            self._specs[api_name] = spec_dict
            self._operation_map[api_name] = self._build_operation_map(api_name, spec_dict)

            return client

        except Exception as e:
            raise APIConnectionError(f"Failed to create client for {api_name}: {str(e)}")

    def call(
        self,
        api_name: str,
        operation_id: str,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = DEFAULT_TIMEOUT,
        mailto: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Call an API operation by operation ID.

        Args:
            api_name: Name of the API
            operation_id: Operation ID from OpenAPI spec
            path_params: Path parameters
            query_params: Query parameters
            body: Request body
            headers: Additional headers
            timeout: Request timeout
            mailto: Email for polite pool
            base_url: Override base URL

        Returns:
            API response as dictionary

        Raises:
            InvalidOperationError: If operation ID not found
            Various API errors based on response
        """
        client = self.get_client(api_name, base_url=base_url, timeout=timeout, mailto=mailto)

        # Get operation mapping
        if api_name not in self._operation_map:
            raise InvalidAPIError(api_name)

        if operation_id not in self._operation_map[api_name]:
            raise InvalidOperationError(operation_id)

        # Get the resource and operation from Bravado client
        # Bravado organizes operations by tags/resources
        try:
            # Try to find the operation in client resources
            operation_found = False
            result = None

            # Iterate through all resources to find the operation
            for resource_name in dir(client):
                if resource_name.startswith("_"):
                    continue

                resource = getattr(client, resource_name)
                if hasattr(resource, operation_id):
                    operation_found = True
                    operation_func = getattr(resource, operation_id)

                    # Build kwargs
                    kwargs = {}
                    if path_params:
                        kwargs.update(path_params)
                    if query_params:
                        kwargs.update(query_params)
                    if body:
                        kwargs.update(body)

                    # Add mailto to query params if provided
                    if mailto and "mailto" not in kwargs:
                        kwargs["mailto"] = mailto

                    # Call operation
                    try:
                        future = operation_func(**kwargs)
                        result = future.result(timeout=timeout)
                        break
                    except Exception as e:
                        result = self._handle_bravado_error(e)
                        if isinstance(result, Exception):
                            raise result
                        break

            if not operation_found:
                raise InvalidOperationError(operation_id)

            # Handle response
            if hasattr(result, "__dict__"):
                # Bravado model - convert to dict
                return self._model_to_dict(result)
            elif isinstance(result, dict):
                return result
            elif isinstance(result, list):
                return {"items": result}
            else:
                return {"result": result}

        except Exception as e:
            if isinstance(
                e,
                (
                    InvalidOperationError,
                    APIConnectionError,
                    APIHTTPError,
                    APIAuthenticationError,
                    APINotFoundError,
                    APIRateLimitError,
                    APIServerError,
                    APITimeoutError,
                ),
            ):
                raise
            raise APIConnectionError(f"Failed to call operation {operation_id}: {str(e)}")

    def _model_to_dict(self, obj: Any) -> Any:
        """Convert Bravado model to dictionary recursively."""
        if hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith("_"):
                    result[key] = self._model_to_dict(value)
            return result
        elif isinstance(obj, list):
            return [self._model_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._model_to_dict(v) for k, v in obj.items()}
        else:
            return obj

    def _handle_bravado_error(self, error: Exception) -> Exception:
        """Convert Bravado exceptions to custom exceptions."""
        if isinstance(error, HTTPUnauthorized):
            return APIAuthenticationError(str(error))
        elif isinstance(error, HTTPNotFound):
            return APINotFoundError(str(error))
        elif isinstance(error, HTTPTooManyRequests):
            # Parse rate limit headers if available
            response = getattr(error, "response", None)
            if response:
                headers = response.headers
                rate_limit_info = {}

                if "X-RateLimit-Limit" in headers:
                    try:
                        rate_limit_info["limit"] = int(headers["X-RateLimit-Limit"])
                    except ValueError:
                        pass

                if "X-RateLimit-Remaining" in headers:
                    try:
                        rate_limit_info["remaining"] = int(headers["X-RateLimit-Remaining"])
                    except ValueError:
                        pass

                if "X-RateLimit-Reset" in headers:
                    try:
                        reset_timestamp = int(headers["X-RateLimit-Reset"])
                        reset_datetime = datetime.fromtimestamp(reset_timestamp, tz=timezone.utc)
                        rate_limit_info["reset_time"] = reset_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
                    except (ValueError, OSError):
                        pass

                if "Retry-After" in headers:
                    try:
                        rate_limit_info["retry_after"] = int(headers["Retry-After"])
                    except ValueError:
                        pass

                return APIRateLimitError(
                    limit=rate_limit_info.get("limit"),
                    remaining=rate_limit_info.get("remaining"),
                    reset_time=rate_limit_info.get("reset_time"),
                    retry_after=rate_limit_info.get("retry_after"),
                )
            return APIRateLimitError()
        elif isinstance(error, HTTPServerError):
            status_code = getattr(error, "status_code", 500)
            return APIServerError(status_code, str(error))
        elif isinstance(error, (HTTPBadRequest, HTTPForbidden)):
            status_code = getattr(error, "status_code", 400)
            return APIHTTPError(status_code, str(error))
        elif isinstance(error, SwaggerValidationError):
            return APIHTTPError(400, f"Validation error: {str(error)}")
        else:
            return error

    def list_operations(self, api_name: str) -> List[Dict[str, str]]:
        """List all operations for an API.

        Args:
            api_name: Name of the API

        Returns:
            List of operation information dictionaries
        """
        # Ensure client is loaded to populate operation map
        self.get_client(api_name)

        if api_name not in self._operation_map:
            return []

        operations = []
        for op_id, details in self._operation_map[api_name].items():
            operations.append(
                {
                    "id": op_id,
                    "method": details["method"],
                    "path": details["path"],
                    "summary": details["summary"],
                }
            )

        return operations


# Global factory instance
_factory = BravadoClientFactory()


def get_client(
    api_name: str,
    base_url: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
    mailto: Optional[str] = None,
) -> SwaggerClient:
    """Get API client for specified API.

    Args:
        api_name: Name of the API
        base_url: Base URL for the API. If not provided, uses default.
        timeout: Timeout in seconds for HTTP requests.
        mailto: Email address for polite pool access.

    Returns:
        Configured SwaggerClient instance
    """
    return _factory.get_client(api_name, base_url=base_url, timeout=timeout, mailto=mailto)
