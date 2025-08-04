"""Test to prove and document the method name mismatch in api_client.py"""

from unittest.mock import patch

from ecosystems_cli.api_client import APIClient


class TestAPIClientMethodMismatch:
    """Tests documenting the method name mismatch issue."""

    def test_get_hosts_calls_getRegistries_operation(self):
        """Test proving that get_hosts() calls 'getRegistries' operation.

        This test documents an inconsistency:
        - The method is named get_hosts()
        - The endpoint is /hosts
        - But the OpenAPI operation ID is 'getRegistries'
        - The response contains Host objects, not Registry objects

        This appears to be an inconsistency in the OpenAPI specification itself.
        """
        # Create a repos API client
        client = APIClient("repos", base_url="https://api.example.com", timeout=10)

        # Mock the call method
        with patch.object(client, "call") as mock_call:
            mock_call.return_value = [{"name": "github.com", "type": "host"}, {"name": "gitlab.com", "type": "host"}]

            # Call get_hosts()
            result = client.get_hosts()

            # Verify it calls 'getRegistries' (not 'getHosts')
            mock_call.assert_called_once_with("getRegistries")

            # The result contains host data, not registry data
            assert result[0]["type"] == "host"

    def test_semantic_difference_between_apis(self):
        """Test showing repos API uses different terminology than packages API.

        - Packages API: registries (npm, pypi, rubygems)
        - Repos API: hosts (github.com, gitlab.com, bitbucket.org)

        Despite different concepts, repos API reuses 'getRegistries' operation name.
        """
        packages_client = APIClient("packages", base_url="https://api.example.com", timeout=10)
        repos_client = APIClient("repos", base_url="https://api.example.com", timeout=10)

        with patch.object(packages_client, "call") as mock_packages, patch.object(repos_client, "call") as mock_repos:

            # Both methods call 'getRegistries' but mean different things
            packages_client.get_registries()
            repos_client.get_hosts()

            mock_packages.assert_called_with("getRegistries")
            mock_repos.assert_called_with("getRegistries")

            # This is confusing because:
            # - Package registries: npm, pypi, etc.
            # - Repository hosts: github.com, gitlab.com, etc.
            # These are completely different concepts

    def test_openapi_spec_mismatch(self):
        """Test documenting the OpenAPI specification issue.

        From repos.openapi.yaml:
        - Endpoint: /hosts
        - Operation ID: getRegistries
        - Returns: Array of Host objects

        The operation ID doesn't match the endpoint or return type.
        """
        # This test documents the issue found in the OpenAPI spec
        # The fix should probably be in the OpenAPI spec, not the Python code

        client = APIClient("repos", base_url="https://api.example.com", timeout=10)

        # The current implementation follows the OpenAPI spec correctly
        # even though the spec itself has a naming inconsistency
        assert hasattr(client, "get_hosts")

        # If we examine the implementation:
        # - get_hosts() method name matches the endpoint /hosts
        # - It calls getRegistries because that's the operation ID
        # - This is technically correct per the OpenAPI spec
