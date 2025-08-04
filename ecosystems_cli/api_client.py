"""API client for ecosystems CLI using requests."""

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
                raise APIAuthenticationError(error_msg)
            elif response.status_code == 404:
                raise APINotFoundError(error_msg)
            elif response.status_code >= 500:
                # Include URL in server error for better debugging
                msg = f"Server error at {url}"
                if error_msg:
                    msg += f": {error_msg}"
                raise APIServerError(response.status_code, msg)
            else:
                raise APIHTTPError(response.status_code, error_msg)

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

    # Convenience methods for common operations

    def get_topics(self) -> Dict[str, Any]:
        """Get all topics (repos API)."""
        if self.api_name != "repos":
            raise InvalidAPIError(f"Method get_topics is only available for 'repos' API, not '{self.api_name}'")
        return self.call("topics")

    def get_topic(self, topic_name: str) -> Dict[str, Any]:
        """Get a specific topic (repos API)."""
        if self.api_name != "repos":
            raise InvalidAPIError(f"Method get_topic is only available for 'repos' API, not '{self.api_name}'")
        return self.call("topic", path_params={"topic": topic_name})

    def get_registries(self) -> Dict[str, Any]:
        """Get all registries (packages API)."""
        if self.api_name != "packages":
            raise InvalidAPIError(f"Method get_registries is only available for 'packages' API, not '{self.api_name}'")
        return self.call("getRegistries")

    def get_registry(self, registry_name: str) -> Dict[str, Any]:
        """Get a specific registry (packages API)."""
        if self.api_name != "packages":
            raise InvalidAPIError(f"Method get_registry is only available for 'packages' API, not '{self.api_name}'")
        return self.call("getRegistry", path_params={"registryName": registry_name})

    # Additional convenience methods for packages API

    def get_package(self, registry_name: str, package_name: str) -> Dict[str, Any]:
        """Get a specific package from a registry (packages API)."""
        if self.api_name != "packages":
            raise InvalidAPIError(f"Method get_package is only available for 'packages' API, not '{self.api_name}'")
        return self.call("getRegistryPackage", path_params={"registryName": registry_name, "packageName": package_name})

    def get_package_version(self, registry_name: str, package_name: str, version: str) -> Dict[str, Any]:
        """Get a specific package version (packages API)."""
        if self.api_name != "packages":
            raise InvalidAPIError(f"Method get_package_version is only available for 'packages' API, not '{self.api_name}'")
        return self.call(
            "getRegistryPackageVersion",
            path_params={"registryName": registry_name, "packageName": package_name, "versionNumber": version},
        )

    # Additional convenience methods for repos API

    def get_hosts(self) -> Dict[str, Any]:
        """Get all repository hosts (repos API).

        NOTE: This method calls the 'getRegistries' operation due to an inconsistency
        in the OpenAPI specification. The /hosts endpoint incorrectly uses
        'getRegistries' as its operation ID. This is documented in KNOWN_ISSUES.md.
        """
        if self.api_name != "repos":
            raise InvalidAPIError(f"Method get_hosts is only available for 'repos' API, not '{self.api_name}'")
        return self.call("getRegistries")  # OpenAPI spec uses 'getRegistries' for /hosts endpoint

    def get_host(self, host_name: str) -> Dict[str, Any]:
        """Get a specific repository host (repos API)."""
        if self.api_name != "repos":
            raise InvalidAPIError(f"Method get_host is only available for 'repos' API, not '{self.api_name}'")
        return self.call("getHost", path_params={"hostName": host_name})

    def get_repository(self, host_name: str, owner: str, repo: str) -> Dict[str, Any]:
        """Get a specific repository (repos API)."""
        if self.api_name != "repos":
            raise InvalidAPIError(f"Method get_repository is only available for 'repos' API, not '{self.api_name}'")
        return self.call("getHostRepository", path_params={"hostName": host_name, "repositoryName": f"{owner}/{repo}"})

    # Additional convenience methods for papers API

    def list_papers(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List all papers (papers API)."""
        if self.api_name != "papers":
            raise InvalidAPIError(f"Method list_papers is only available for 'papers' API, not '{self.api_name}'")
        query_params = {}
        if page is not None:
            query_params["page"] = page
        if per_page is not None:
            query_params["per_page"] = per_page
        if sort is not None:
            query_params["sort"] = sort
        if order is not None:
            query_params["order"] = order
        return self.call("listPapers", query_params=query_params if query_params else None)

    def get_paper(self, doi: str) -> Dict[str, Any]:
        """Get a specific paper by DOI (papers API)."""
        if self.api_name != "papers":
            raise InvalidAPIError(f"Method get_paper is only available for 'papers' API, not '{self.api_name}'")
        return self.call("getPaper", path_params={"doi": doi})

    def get_paper_mentions(self, doi: str, page: Optional[int] = None, per_page: Optional[int] = None) -> Dict[str, Any]:
        """List all mentions for a paper (papers API)."""
        if self.api_name != "papers":
            raise InvalidAPIError(f"Method get_paper_mentions is only available for 'papers' API, not '{self.api_name}'")
        query_params = {}
        if page is not None:
            query_params["page"] = page
        if per_page is not None:
            query_params["per_page"] = per_page
        return self.call("listPaperMentions", path_params={"doi": doi}, query_params=query_params if query_params else None)


def get_client(api_name: str, base_url: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT) -> APIClient:
    """Get API client for specified API.

    Args:
        api_name: Name of the API (packages, repos, summary, awesome, papers)
        base_url: Base URL for the API. If not provided, uses default.
        timeout: Timeout in seconds for HTTP requests. Default is 20 seconds.
    """
    return APIClient(api_name=api_name, base_url=base_url, timeout=timeout)
