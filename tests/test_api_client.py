"""Tests for the API client."""

from pathlib import Path
from unittest import mock

import pytest
import yaml

from ecosystems_cli.api_client import APIClient, get_client
from ecosystems_cli.exceptions import (
    APIAuthenticationError,
    APIHTTPError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
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
                    "parameters": [
                        {
                            "name": "id",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                }
            },
            "/items/{itemId}": {
                "get": {
                    "operationId": "getItem",
                    "summary": "Get item by ID",
                    "parameters": [
                        {
                            "name": "itemId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                }
            },
        },
    }


class TestAPIClient:
    """Test the APIClient class."""

    def test_init_loads_spec(self, monkeypatch, mock_spec):
        """Test that the client loads the API spec on initialization."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)

        # Act
        client = APIClient("test")

        # Assert
        assert client.spec == mock_spec

    def test_get_default_base_url(self, monkeypatch, mock_spec):
        """Test that the client gets the default base URL from the spec."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)

        # Act
        client = APIClient("test")

        # Assert
        assert client.base_url == "https://test.example.com/api/v1"

    def test_parse_endpoints(self, monkeypatch, mock_spec):
        """Test that the client parses endpoints from the spec."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)

        # Act
        client = APIClient("test")

        # Assert
        assert "getTest" in client.endpoints
        assert "getItem" in client.endpoints
        assert client.endpoints["getTest"]["path"] == "/test"
        assert client.endpoints["getItem"]["path"] == "/items/{itemId}"

    def test_build_url_with_path_params(self, monkeypatch, mock_spec):
        """Test that the client builds URLs with path parameters."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        # Act
        url = client._build_url("/items/{itemId}", {"itemId": "123"})

        # Assert
        assert url == "https://test.example.com/api/v1/items/123"

    @mock.patch("requests.request")
    def test_make_request(self, mock_request, monkeypatch, mock_spec):
        """Test that the client makes HTTP requests correctly."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response

        # Act
        result = client._make_request("get", "/test", query_params={"id": "123"})

        # Assert
        assert result == {"data": "test"}
        mock_request.assert_called_once_with(
            method="get",
            url="https://test.example.com/api/v1/test",
            params={"id": "123"},
            json=None,
            headers={"Content-Type": "application/json", "User-Agent": "ecosyste_ms_cli (1.0.0)"},
            timeout=20,
        )

    @mock.patch("requests.request")
    def test_call_operation(self, mock_request, monkeypatch, mock_spec):
        """Test that the client calls operations by ID."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response

        # Act
        result = client.call("getItem", path_params={"itemId": "123"})

        # Assert
        assert result == {"data": "test"}
        mock_request.assert_called_once_with(
            method="get",
            url="https://test.example.com/api/v1/items/123",
            params={},
            json=None,
            headers={"Content-Type": "application/json", "User-Agent": "ecosyste_ms_cli (1.0.0)"},
            timeout=20,
        )

    def test_call_invalid_operation(self, monkeypatch, mock_spec):
        """Test that the client raises an error for invalid operations."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        # Act & Assert
        from ecosystems_cli.exceptions import InvalidOperationError

        with pytest.raises(InvalidOperationError, match="Invalid operation: invalidOp"):
            client.call("invalidOp")

    def test_get_required_params(self, monkeypatch, mock_spec):
        """Test that _get_required_params returns only required parameters."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        # Act
        required_params = client._get_required_params(mock_spec["paths"]["/test"]["get"])

        # Assert
        assert "id" in required_params
        assert required_params["id"]["required"] is True
        # Should not include non-required params (if any were present)
        # Add a non-required param and test
        details = mock_spec["paths"]["/test"]["get"].copy()
        details["parameters"] = details["parameters"] + [
            {
                "name": "optional_param",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            }
        ]
        required_params2 = client._get_required_params(details)
        assert "optional_param" not in required_params2

    @mock.patch("requests.request")
    def test_server_error_with_message(self, mock_request, monkeypatch, mock_spec):
        """Test that server errors include the error message from response."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "internal server error"}
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIServerError) as exc_info:
            client._make_request("get", "/test")

        assert "Server error at" in str(exc_info.value)
        assert "internal server error" in str(exc_info.value)
        assert exc_info.value.status_code == 500

    @mock.patch("requests.request")
    def test_server_error_without_message(self, mock_request, monkeypatch, mock_spec):
        """Test that server errors work even without error message in response."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 503
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIServerError) as exc_info:
            client._make_request("get", "/test")

        assert "Server error at" in str(exc_info.value)
        assert exc_info.value.status_code == 503

    @mock.patch("requests.request")
    def test_authentication_error(self, mock_request, monkeypatch, mock_spec):
        """Test that 401 errors are handled properly."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid API key"}
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIAuthenticationError) as exc_info:
            client._make_request("get", "/test")

        assert "Invalid API key" in str(exc_info.value)
        assert exc_info.value.status_code == 401

    @mock.patch("requests.request")
    def test_not_found_error(self, mock_request, monkeypatch, mock_spec):
        """Test that 404 errors are handled properly."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Resource not found"}
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APINotFoundError) as exc_info:
            client._make_request("get", "/test")

        assert "Resource not found" in str(exc_info.value)
        assert exc_info.value.status_code == 404

    @mock.patch("requests.request")
    def test_other_http_error(self, mock_request, monkeypatch, mock_spec):
        """Test that other HTTP errors are handled properly."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad request"}
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIHTTPError) as exc_info:
            client._make_request("get", "/test")

        assert "Bad request" in str(exc_info.value)
        assert exc_info.value.status_code == 400

    @mock.patch("requests.request")
    def test_rate_limit_error_with_all_headers(self, mock_request, monkeypatch, mock_spec):
        """Test that 429 errors are handled properly with all rate limit headers."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Too Many Requests"}
        mock_response.headers = {
            "X-RateLimit-Limit": "1000",
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1735128000",  # 2024-12-25 12:00:00 UTC
            "Retry-After": "3600",
        }
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIRateLimitError) as exc_info:
            client._make_request("get", "/test")

        error = exc_info.value
        assert error.status_code == 429
        assert error.limit == 1000
        assert error.remaining == 0
        assert error.retry_after == 3600
        assert "2024-12-25 12:00:00 UTC" in error.reset_time
        assert "Rate limit exceeded" in str(error)
        assert "1000 requests per window" in str(error)
        assert "0 requests" in str(error)
        assert "3600 seconds" in str(error)

    @mock.patch("requests.request")
    def test_rate_limit_error_with_minimal_headers(self, mock_request, monkeypatch, mock_spec):
        """Test that 429 errors work with minimal headers."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Too Many Requests"}
        mock_response.headers = {}  # No rate limit headers
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIRateLimitError) as exc_info:
            client._make_request("get", "/test")

        error = exc_info.value
        assert error.status_code == 429
        assert error.limit is None
        assert error.remaining is None
        assert error.retry_after is None
        assert error.reset_time is None
        assert "Rate limit exceeded" in str(error)
        assert "Please wait before retrying" in str(error)

    @mock.patch("requests.request")
    def test_rate_limit_error_with_invalid_headers(self, mock_request, monkeypatch, mock_spec):
        """Test that 429 errors handle invalid header values gracefully."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = pytest.importorskip("requests").exceptions.HTTPError()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Too Many Requests"}
        mock_response.headers = {
            "X-RateLimit-Limit": "invalid",  # Invalid integer
            "X-RateLimit-Remaining": "also-invalid",  # Invalid integer
            "X-RateLimit-Reset": "not-a-timestamp",  # Invalid timestamp
            "Retry-After": "not-a-number",  # Invalid integer
        }
        mock_request.return_value = mock_response

        # Act & Assert
        with pytest.raises(APIRateLimitError) as exc_info:
            client._make_request("get", "/test")

        error = exc_info.value
        assert error.status_code == 429
        assert error.limit is None  # Should be None due to invalid value
        assert error.remaining is None  # Should be None due to invalid value
        assert error.retry_after is None  # Should be None due to invalid value
        assert error.reset_time is None  # Should be None due to invalid value
        assert "Rate limit exceeded" in str(error)

    def test_parse_rate_limit_headers_valid(self, monkeypatch, mock_spec):
        """Test parsing valid rate limit headers."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.headers = {
            "X-RateLimit-Limit": "1000",
            "X-RateLimit-Remaining": "500",
            "X-RateLimit-Reset": "1735128000",  # 2024-12-25 12:00:00 UTC
            "Retry-After": "3600",
        }

        # Act
        result = client._parse_rate_limit_headers(mock_response)

        # Assert
        assert result["limit"] == 1000
        assert result["remaining"] == 500
        assert "2024-12-25 12:00:00 UTC" in result["reset_time"]
        assert result["retry_after"] == 3600

    def test_parse_rate_limit_headers_empty(self, monkeypatch, mock_spec):
        """Test parsing when no rate limit headers are present."""
        # Arrange
        mock_open = mock.mock_open(read_data=yaml.dump(mock_spec))
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr(Path, "exists", lambda self: True)
        client = APIClient("test")

        mock_response = mock.Mock()
        mock_response.headers = {}

        # Act
        result = client._parse_rate_limit_headers(mock_response)

        # Assert
        assert result == {}


def test_get_client():
    """Test the get_client function."""
    # Arrange
    with mock.patch.object(APIClient, "__init__", return_value=None) as mock_init:
        # Act
        get_client("test", "https://custom.example.com")

        # Assert
        mock_init.assert_called_once_with(api_name="test", base_url="https://custom.example.com", timeout=20)
