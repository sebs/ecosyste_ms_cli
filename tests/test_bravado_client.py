"""Tests for the Bravado API client."""

from unittest import mock

import pytest
import yaml

from ecosystems_cli.bravado_client import BravadoClientFactory, get_client
from ecosystems_cli.exceptions import (
    InvalidAPIError,
    InvalidOperationError,
)


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


class TestBravadoClientFactory:
    """Test the BravadoClientFactory class."""

    def test_init_with_custom_specs_dir(self, mock_spec_file):
        """Test factory initialization with custom specs directory."""
        factory = BravadoClientFactory(specs_dir=mock_spec_file)
        assert factory.specs_dir == mock_spec_file

    def test_discover_apis(self, mock_spec_file):
        """Test API discovery from specs directory."""
        factory = BravadoClientFactory(specs_dir=mock_spec_file)
        apis = factory._discover_apis()
        assert "test" in apis

    def test_get_client_invalid_api(self, mock_spec_file):
        """Test getting client for non-existent API."""
        factory = BravadoClientFactory(specs_dir=mock_spec_file)
        with pytest.raises(InvalidAPIError):
            factory.get_client("nonexistent")

    @mock.patch("ecosystems_cli.bravado_client.SwaggerClient.from_spec")
    def test_get_client_success(self, mock_from_spec, mock_spec_file):
        """Test successful client creation."""
        # Arrange
        mock_client = mock.Mock()
        mock_client.swagger_spec = mock.Mock()
        mock_client.swagger_spec.api_url = "https://test.example.com/api/v1"
        mock_client.swagger_spec.http_client = None
        mock_from_spec.return_value = mock_client

        factory = BravadoClientFactory(specs_dir=mock_spec_file)

        # Act
        client = factory.get_client("test")

        # Assert
        assert client is not None
        mock_from_spec.assert_called_once()

    @mock.patch("ecosystems_cli.bravado_client.SwaggerClient.from_spec")
    def test_get_client_with_mailto(self, mock_from_spec, mock_spec_file):
        """Test client creation with mailto parameter."""
        # Arrange
        mock_client = mock.Mock()
        mock_client.swagger_spec = mock.Mock()
        mock_client.swagger_spec.http_client = None
        mock_from_spec.return_value = mock_client

        factory = BravadoClientFactory(specs_dir=mock_spec_file)

        # Act
        client = factory.get_client("test", mailto="test@example.com")

        # Assert
        assert client is not None
        # Mailto is included in User-Agent but not passed to from_spec
        # Just verify the call was made
        mock_from_spec.assert_called_once()

    @mock.patch("ecosystems_cli.bravado_client.SwaggerClient.from_spec")
    def test_get_client_caching(self, mock_from_spec, mock_spec_file):
        """Test that clients are cached."""
        # Arrange
        mock_client = mock.Mock()
        mock_client.swagger_spec = mock.Mock()
        mock_client.swagger_spec.http_client = None
        mock_from_spec.return_value = mock_client

        factory = BravadoClientFactory(specs_dir=mock_spec_file)

        # Act
        client1 = factory.get_client("test", timeout=20)
        client2 = factory.get_client("test", timeout=20)

        # Assert
        assert client1 is client2
        mock_from_spec.assert_called_once()

    def test_build_operation_map(self, mock_spec_file, mock_spec):
        """Test operation mapping building."""
        factory = BravadoClientFactory(specs_dir=mock_spec_file)
        operation_map = factory._build_operation_map("test", mock_spec)

        assert "getTest" in operation_map
        assert "getItem" in operation_map
        assert operation_map["getTest"]["path"] == "/test"
        assert operation_map["getTest"]["method"] == "GET"
        assert operation_map["getItem"]["path"] == "/items/{itemId}"

    @mock.patch("ecosystems_cli.bravado_client.SwaggerClient.from_spec")
    def test_list_operations(self, mock_from_spec, mock_spec_file):
        """Test listing operations."""
        # Arrange
        mock_client = mock.Mock()
        mock_client.swagger_spec = mock.Mock()
        mock_client.swagger_spec.http_client = None
        mock_from_spec.return_value = mock_client

        factory = BravadoClientFactory(specs_dir=mock_spec_file)

        # Act
        operations = factory.list_operations("test")

        # Assert
        assert len(operations) == 2
        operation_ids = [op["id"] for op in operations]
        assert "getTest" in operation_ids
        assert "getItem" in operation_ids

    @mock.patch("ecosystems_cli.bravado_client.SwaggerClient.from_spec")
    def test_call_invalid_operation(self, mock_from_spec, mock_spec_file):
        """Test calling non-existent operation."""
        # Arrange
        mock_client = mock.Mock()
        mock_client.swagger_spec = mock.Mock()
        mock_client.swagger_spec.http_client = None
        mock_from_spec.return_value = mock_client

        factory = BravadoClientFactory(specs_dir=mock_spec_file)

        # Act & Assert
        with pytest.raises(InvalidOperationError):
            factory.call("test", "nonexistentOperation")


class TestGetClient:
    """Test the get_client convenience function."""

    @mock.patch("ecosystems_cli.bravado_client._factory.get_client")
    def test_get_client_delegates_to_factory(self, mock_factory_get_client):
        """Test that get_client delegates to factory."""
        # Act
        get_client("test", timeout=30, mailto="test@example.com")

        # Assert
        mock_factory_get_client.assert_called_once_with("test", base_url=None, timeout=30, mailto="test@example.com")
