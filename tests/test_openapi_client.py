"""Tests for the OpenAPI client."""

from unittest import mock

import pytest
import yaml

from ecosystems_cli.exceptions import (
    InvalidAPIError,
    InvalidOperationError,
)
from ecosystems_cli.openapi_client import OpenAPIClientFactory, get_client


@pytest.fixture
def mock_spec():
    """Create a mock OpenAPI spec for testing."""
    return {
        "openapi": "3.0.0",
        "info": {"title": "Test API", "version": "1.0.0"},
        "servers": [{"url": "https://test.example.com/api/v1"}],
        "paths": {
            "/test": {
                "get": {
                    "operationId": "getTest",
                    "summary": "Get test data",
                    "tags": ["test"],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {"schema": {"type": "object", "properties": {"data": {"type": "string"}}}}
                            },
                        }
                    },
                }
            },
            "/items/{itemId}": {
                "get": {
                    "operationId": "getItem",
                    "summary": "Get item by ID",
                    "tags": ["items"],
                    "parameters": [
                        {
                            "name": "itemId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"id": {"type": "string"}, "name": {"type": "string"}},
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
    }


@pytest.fixture
def mock_spec_file(tmp_path, mock_spec):
    """Create a temporary spec file."""
    spec_dir = tmp_path / "apis"
    spec_dir.mkdir()
    spec_file = spec_dir / "test.openapi.yaml"
    with open(spec_file, "w") as f:
        yaml.dump(mock_spec, f)
    return spec_dir


class TestOpenAPIClientFactory:
    """Test the OpenAPIClientFactory class."""

    def test_init_with_custom_specs_dir(self, mock_spec_file):
        """Test factory initialization with custom specs directory."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)
        assert factory.specs_dir == mock_spec_file

    def test_discover_apis(self, mock_spec_file):
        """Test API discovery from specs directory."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)
        apis = factory._discover_apis()
        assert "test" in apis

    def test_get_client_invalid_api(self, mock_spec_file):
        """Test getting client for non-existent API."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)
        with pytest.raises(InvalidAPIError):
            factory.get_client("nonexistent")

    def test_get_client_success(self, mock_spec_file):
        """Test successful client creation."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)

        # Act
        client = factory.get_client("test")

        # Assert
        assert client is not None
        assert client == factory  # get_client returns the factory itself

    def test_get_client_with_mailto(self, mock_spec_file):
        """Test client creation with mailto parameter."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)

        # Act
        client = factory.get_client("test", mailto="test@example.com")

        # Assert
        assert client is not None
        assert client == factory  # get_client returns the factory itself

    def test_get_client_caching(self, mock_spec_file):
        """Test that clients are cached."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)

        # Act
        client1 = factory.get_client("test", timeout=20)
        client2 = factory.get_client("test", timeout=20)

        # Assert
        assert client1 is client2  # Both return the same factory instance
        # Verify OpenAPI instance is cached
        assert "test" in factory._openapi

    def test_build_operation_map(self, mock_spec_file, mock_spec):
        """Test operation mapping building."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)
        operation_map = factory._build_operation_map("test", mock_spec)

        assert "getTest" in operation_map
        assert "getItem" in operation_map
        assert operation_map["getTest"]["path"] == "/test"
        assert operation_map["getTest"]["method"] == "GET"
        assert operation_map["getItem"]["path"] == "/items/{itemId}"

    def test_list_operations(self, mock_spec_file):
        """Test listing operations."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)

        # Act
        operations = factory.list_operations("test")

        # Assert
        assert len(operations) == 2
        operation_ids = [op["id"] for op in operations]
        assert "getTest" in operation_ids
        assert "getItem" in operation_ids

    def test_call_invalid_operation(self, mock_spec_file):
        """Test calling non-existent operation."""
        factory = OpenAPIClientFactory(specs_dir=mock_spec_file)

        # Act & Assert
        with pytest.raises(InvalidOperationError):
            factory.call("test", "nonexistentOperation")


class TestGetClient:
    """Test the get_client convenience function."""

    @mock.patch("ecosystems_cli.openapi_client._factory.get_client")
    def test_get_client_delegates_to_factory(self, mock_factory_get_client):
        """Test that get_client delegates to factory."""
        # Act
        get_client("test", timeout=30, mailto="test@example.com")

        # Assert
        mock_factory_get_client.assert_called_once_with("test", base_url=None, timeout=30, mailto="test@example.com")
