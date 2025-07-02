"""API client for ecosystems CLI using requests."""

from typing import Any, Dict, List, Optional

import requests

from ecosystems_cli.constants import (
    API_BASE_URL_TEMPLATE,
    DEFAULT_CONTENT_TYPE,
    DEFAULT_TIMEOUT,
    ERROR_API_ONLY,
    ERROR_OPERATION_NOT_FOUND,
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
        self.spec = load_api_spec(api_name)
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

        response = requests.request(
            method=method, url=url, params=query_params, json=body, headers=headers, timeout=self.timeout
        )

        # Raise exception for error status codes
        response.raise_for_status()

        # Return JSON response if available, otherwise return response text
        try:
            return response.json()
        except ValueError:
            return {"text": response.text}

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
            raise ValueError(ERROR_OPERATION_NOT_FOUND.format(operation_id=operation_id, api_name=self.api_name))

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
            raise ValueError(ERROR_API_ONLY.format(api_name="repos"))
        return self.call("topics")

    def get_topic(self, topic_name: str) -> Dict[str, Any]:
        """Get a specific topic (repos API)."""
        if self.api_name != "repos":
            raise ValueError(ERROR_API_ONLY.format(api_name="repos"))
        return self.call("topic", path_params={"topic": topic_name})

    def get_registries(self) -> Dict[str, Any]:
        """Get all registries (packages API)."""
        if self.api_name != "packages":
            raise ValueError(ERROR_API_ONLY.format(api_name="packages"))
        return self.call("getRegistries")

    def get_registry(self, registry_name: str) -> Dict[str, Any]:
        """Get a specific registry (packages API)."""
        if self.api_name != "packages":
            raise ValueError(ERROR_API_ONLY.format(api_name="packages"))
        return self.call("getRegistry", path_params={"registryName": registry_name})

    # Additional convenience methods for packages API

    def get_package(self, registry_name: str, package_name: str) -> Dict[str, Any]:
        """Get a specific package from a registry (packages API)."""
        if self.api_name != "packages":
            raise ValueError(ERROR_API_ONLY.format(api_name="packages"))
        return self.call("getPackage", path_params={"registryName": registry_name, "packageName": package_name})

    def get_package_version(self, registry_name: str, package_name: str, version: str) -> Dict[str, Any]:
        """Get a specific package version (packages API)."""
        if self.api_name != "packages":
            raise ValueError(ERROR_API_ONLY.format(api_name="packages"))
        return self.call(
            "getPackageVersion", path_params={"registryName": registry_name, "packageName": package_name, "version": version}
        )

    # Additional convenience methods for repos API

    def get_hosts(self) -> Dict[str, Any]:
        """Get all repository hosts (repos API)."""
        if self.api_name != "repos":
            raise ValueError(ERROR_API_ONLY.format(api_name="repos"))
        return self.call("getRegistries")

    def get_host(self, host_name: str) -> Dict[str, Any]:
        """Get a specific repository host (repos API)."""
        if self.api_name != "repos":
            raise ValueError(ERROR_API_ONLY.format(api_name="repos"))
        return self.call("getHost", path_params={"hostName": host_name})

    def get_repository(self, host_name: str, owner: str, repo: str) -> Dict[str, Any]:
        """Get a specific repository (repos API)."""
        if self.api_name != "repos":
            raise ValueError(ERROR_API_ONLY.format(api_name="repos"))
        return self.call("getHostRepository", path_params={"hostName": host_name, "repositoryName": f"{owner}/{repo}"})

    # Additional convenience methods for summary API

    def get_repo_summary(self, url: str) -> Dict[str, Any]:
        """Get summary for a repository by URL (summary API)."""
        if self.api_name != "summary":
            raise ValueError(ERROR_API_ONLY.format(api_name="summary"))
        return self.call("repo", query_params={"url": url})

    def get_package_summary(self, url: str) -> Dict[str, Any]:
        """Get summary for a package by URL (summary API)."""
        if self.api_name != "summary":
            raise ValueError(ERROR_API_ONLY.format(api_name="summary"))
        return self.call("package", query_params={"url": url})


def get_client(api_name: str, base_url: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT) -> APIClient:
    """Get API client for specified API.

    Args:
        api_name: Name of the API (packages, repos, summary)
        base_url: Base URL for the API. If not provided, uses default.
        timeout: Timeout in seconds for HTTP requests. Default is 20 seconds.
    """
    return APIClient(api_name=api_name, base_url=base_url, timeout=timeout)
