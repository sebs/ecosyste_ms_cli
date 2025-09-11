"""API client for ecosystems CLI using requests."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from ecosystems_cli import __version__
from ecosystems_cli.constants import (
    API_BASE_URL_TEMPLATE,
    DEFAULT_CONTENT_TYPE,
    DEFAULT_TIMEOUT,
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
    JSONParseError,
)
from ecosystems_cli.helpers.build_url import build_url
from ecosystems_cli.helpers.load_api_spec import load_api_spec
from ecosystems_cli.helpers.parse_endpoints import parse_endpoints
from ecosystems_cli.helpers.parse_parameters import parse_parameters


class APIClient:
    """Client for interacting with ecosyste.ms APIs."""

    def __init__(self, api_name: str, base_url: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT):
        """Initialize API client.

        Args:
            api_name: Name of the API (packages, repos, summary)
            base_url: Base URL for the API. If not provided, uses default.
            timeout: Timeout in seconds for HTTP requests. Default is DEFAULT_TIMEOUT seconds.
        """
        self.api_name = api_name
        try:
            self.spec = load_api_spec(api_name)
        except FileNotFoundError:
            raise InvalidAPIError(api_name)
        self.base_url = base_url or self._get_default_base_url()
        self.endpoints = parse_endpoints(self.spec)
        self.timeout = timeout

    def _get_default_base_url(self) -> str:
        """Get default base URL from OpenAPI specification."""
        servers = self.spec.get("servers", [])
        if servers and "url" in servers[0]:
            return servers[0]["url"]
        return API_BASE_URL_TEMPLATE.format(api_name=self.api_name)

    def _get_required_params(self, details: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Get required parameters from endpoint details (delegated to helper)."""
        return {k: v for k, v in parse_parameters(details).items() if v.get("required", False)}

    def _parse_parameters(self, details: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Parse parameters from endpoint details (delegated to helper)."""
        return parse_parameters(details)

    def _build_url(self, path: str, path_params: Dict[str, Any]) -> str:
        """Build URL with path parameters (delegated to helper)."""
        return build_url(self.base_url, path, path_params)

    def _parse_rate_limit_headers(self, response: requests.Response) -> Dict[str, Any]:
        """Parse rate limiting headers from HTTP response."""
        headers = response.headers
        rate_limit_info = {}

        # Parse X-RateLimit-* headers
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

        # Parse Retry-After header (standard HTTP header)
        if "Retry-After" in headers:
            try:
                rate_limit_info["retry_after"] = int(headers["Retry-After"])
            except ValueError:
                pass

        return rate_limit_info

    def _make_request(
        self,
        method: str,
        path: str,
        path_params: Dict[str, Any] = None,
        query_params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        path_params = path_params or {}
        query_params = query_params or {}
        headers = headers or {}

        url = self._build_url(path, path_params)

        # Set default headers
        if "Content-Type" not in headers:
            headers["Content-Type"] = DEFAULT_CONTENT_TYPE

        # Set user-agent header
        headers["User-Agent"] = f"ecosyste_ms_cli ({__version__})"

        try:
            response = requests.request(
                method=method, url=url, params=query_params, json=body, headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            raise APITimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(f"Failed to connect to API: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise APIConnectionError(f"Request failed: {str(e)}")

        # Handle different HTTP error codes
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # Try to extract error message from response
            error_msg = None
            try:
                error_data = response.json()
                error_msg = error_data.get("error") or error_data.get("message")
            except (ValueError, TypeError, AttributeError):
                # If response is not JSON or malformed, error_msg remains None
                # The actual error text will be included in the exception message
                pass

            if response.status_code == 401:
                raise APIAuthenticationError(str(error_msg))
            elif response.status_code == 404:
                raise APINotFoundError(str(error_msg))
            elif response.status_code == 429:
                # Handle rate limiting
                rate_limit_info = self._parse_rate_limit_headers(response)
                raise APIRateLimitError(
                    limit=rate_limit_info.get("limit"),
                    remaining=rate_limit_info.get("remaining"),
                    reset_time=rate_limit_info.get("reset_time"),
                    retry_after=rate_limit_info.get("retry_after"),
                )
            elif response.status_code >= 500:
                # Include URL in server error for better debugging
                msg = f"Server error at {url}"
                if error_msg:
                    msg += f": {error_msg}"
                raise APIServerError(response.status_code, msg)
            else:
                raise APIHTTPError(response.status_code, str(error_msg))

        # Return JSON response if available, otherwise return response text
        try:
            return response.json()
        except ValueError:
            # Check if response is empty
            if not response.text:
                return {}
            # If we have non-JSON content, raise an error instead of returning text
            raise JSONParseError(f"Expected JSON response but got: {response.text[:100]}...")

    def call(
        self,
        operation_id: str,
        path_params: Dict[str, Any] = None,
        query_params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ) -> Dict[str, Any]:
        """Call API endpoint by operation ID."""
        if operation_id not in self.endpoints:
            raise InvalidOperationError(operation_id)

        endpoint = self.endpoints[operation_id]

        return self._make_request(
            method=endpoint["method"],
            path=endpoint["path"],
            path_params=path_params,
            query_params=query_params,
            body=body,
            headers=headers,
        )

    def list_operations(self) -> List[Dict[str, str]]:
        """List available operations."""
        operations = []

        for op_id, details in self.endpoints.items():
            operations.append(
                {"id": op_id, "method": details["method"].upper(), "path": details["path"], "summary": details["summary"]}
            )

        return operations

    # Convenience methods for common operations can be added here as needed


def get_client(api_name: str, base_url: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT) -> APIClient:
    """Get API client for specified API.

    Args:
        api_name: Name of the API (advisories)
        base_url: Base URL for the API. If not provided, uses default.
        timeout: Timeout in seconds for HTTP requests. Default is 20 seconds.
    """
    return APIClient(api_name=api_name, base_url=base_url, timeout=timeout)
