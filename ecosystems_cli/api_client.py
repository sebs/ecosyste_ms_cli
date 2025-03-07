"""API client for ecosystems CLI using requests."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import yaml


class APIClient:
    """Client for interacting with ecosyste.ms APIs."""

    def __init__(self, api_name: str, base_url: Optional[str] = None, timeout: int = 20):
        """Initialize API client.

        Args:
            api_name: Name of the API (packages, repos, summary)
            base_url: Base URL for the API. If not provided, uses default.
            timeout: Timeout in seconds for HTTP requests. Default is 20 seconds.
        """
        self.api_name = api_name
        self.spec = self._load_api_spec()
        self.base_url = base_url or self._get_default_base_url()
        self.endpoints = self._parse_endpoints()
        self.timeout = timeout

    def _load_api_spec(self) -> Dict[str, Any]:
        """Load OpenAPI specification from file."""
        api_file = Path(__file__).parent.parent / "apis" / f"{self.api_name}.openapi.yaml"
        if not api_file.exists():
            raise ValueError(f"API specification for '{self.api_name}' not found")

        with open(api_file, "r") as f:
            return yaml.safe_load(f)

    def _get_default_base_url(self) -> str:
        """Get default base URL from OpenAPI specification."""
        servers = self.spec.get("servers", [])
        if servers and "url" in servers[0]:
            return servers[0]["url"]
        return f"https://{self.api_name}.ecosyste.ms/api/v1"

    def _parse_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """Parse endpoints from OpenAPI specification."""
        endpoints = {}
        paths = self.spec.get("paths", {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method in ["get", "post", "put", "delete", "patch"]:
                    operation_id = details.get("operationId")
                    if operation_id:
                        endpoints[operation_id] = {
                            "path": path,
                            "method": method,
                            "params": self._parse_parameters(details),
                            "description": details.get("description", ""),
                            "summary": details.get("summary", ""),
                            "required_params": self._get_required_params(details),
                        }

        return endpoints

    def _get_required_params(self, details: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Get required parameters from endpoint details."""
        required_params = {}
        for param in details.get("parameters", []):
            if param.get("required", False):
                param_name = param.get("name")
                if param_name:
                    required_params[param_name] = {
                        "in": param.get("in"),
                        "schema": param.get("schema", {}),
                        "description": param.get("description", ""),
                    }
        return required_params

    def _parse_parameters(self, details: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Parse parameters from endpoint details."""
        params = {}
        for param in details.get("parameters", []):
            param_name = param.get("name")
            if param_name:
                params[param_name] = {
                    "in": param.get("in"),
                    "required": param.get("required", False),
                    "schema": param.get("schema", {}),
                    "description": param.get("description", ""),
                }

        return params

    def _build_url(self, path: str, path_params: Dict[str, Any]) -> str:
        """Build URL with path parameters."""
        url = f"{self.base_url}{path}"

        # Replace path parameters
        for param, value in path_params.items():
            url = url.replace(f"{{{param}}}", str(value))

        return url

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
            headers["Content-Type"] = "application/json"

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
            raise ValueError(f"Operation '{operation_id}' not found in {self.api_name} API")

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
            raise ValueError("This method is only available for the repos API")
        return self.call("topics")

    def get_topic(self, topic_name: str) -> Dict[str, Any]:
        """Get a specific topic (repos API)."""
        if self.api_name != "repos":
            raise ValueError("This method is only available for the repos API")
        return self.call("topic", path_params={"topic": topic_name})

    def get_registries(self) -> Dict[str, Any]:
        """Get all registries (packages API)."""
        if self.api_name != "packages":
            raise ValueError("This method is only available for the packages API")
        return self.call("getRegistries")

    def get_registry(self, registry_name: str) -> Dict[str, Any]:
        """Get a specific registry (packages API)."""
        if self.api_name != "packages":
            raise ValueError("This method is only available for the packages API")
        return self.call("getRegistry", path_params={"registryName": registry_name})

    # Additional convenience methods for packages API

    def get_package(self, registry_name: str, package_name: str) -> Dict[str, Any]:
        """Get a specific package from a registry (packages API)."""
        if self.api_name != "packages":
            raise ValueError("This method is only available for the packages API")
        return self.call("getPackage", path_params={"registryName": registry_name, "packageName": package_name})

    def get_package_version(self, registry_name: str, package_name: str, version: str) -> Dict[str, Any]:
        """Get a specific package version (packages API)."""
        if self.api_name != "packages":
            raise ValueError("This method is only available for the packages API")
        return self.call(
            "getPackageVersion", path_params={"registryName": registry_name, "packageName": package_name, "version": version}
        )

    # Additional convenience methods for repos API

    def get_hosts(self) -> Dict[str, Any]:
        """Get all repository hosts (repos API)."""
        if self.api_name != "repos":
            raise ValueError("This method is only available for the repos API")
        return self.call("getRegistries")

    def get_host(self, host_name: str) -> Dict[str, Any]:
        """Get a specific repository host (repos API)."""
        if self.api_name != "repos":
            raise ValueError("This method is only available for the repos API")
        return self.call("getHost", path_params={"hostName": host_name})

    def get_repository(self, host_name: str, owner: str, repo: str) -> Dict[str, Any]:
        """Get a specific repository (repos API)."""
        if self.api_name != "repos":
            raise ValueError("This method is only available for the repos API")
        return self.call("getHostRepository", path_params={"hostName": host_name, "repositoryName": f"{owner}/{repo}"})

    # Additional convenience methods for summary API

    def get_repo_summary(self, url: str) -> Dict[str, Any]:
        """Get summary for a repository by URL (summary API)."""
        if self.api_name != "summary":
            raise ValueError("This method is only available for the summary API")
        return self.call("repo", query_params={"url": url})

    def get_package_summary(self, url: str) -> Dict[str, Any]:
        """Get summary for a package by URL (summary API)."""
        if self.api_name != "summary":
            raise ValueError("This method is only available for the summary API")
        return self.call("package", query_params={"url": url})


def get_client(api_name: str, base_url: Optional[str] = None, timeout: int = 20) -> APIClient:
    """Get API client for specified API.

    Args:
        api_name: Name of the API (packages, repos, summary)
        base_url: Base URL for the API. If not provided, uses default.
        timeout: Timeout in seconds for HTTP requests. Default is 20 seconds.
    """
    return APIClient(api_name=api_name, base_url=base_url, timeout=timeout)
