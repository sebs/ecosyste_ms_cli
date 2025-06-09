"""Tests for the CLI."""

import re
from unittest import mock

import pytest
from click.testing import CliRunner

from ecosystems_cli.cli import main


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def mock_api_client():
    """Create a mock API client for all API groups."""
    with mock.patch("ecosystems_cli.cli.get_client") as mock_client:
        client_instance = mock.MagicMock()
        # Always return the test operation for list_operations
        client_instance.list_operations.return_value = [
            {"id": "test_op", "method": "GET", "path": "/test", "summary": "Test operation"}
        ]
        # Mock call method
        client_instance.call.return_value = {"result": "success"}
        # Mock convenience methods
        client_instance.get_topics.return_value = [{"name": "test_topic"}]
        client_instance.get_hosts.return_value = [{"name": "GitHub"}]
        client_instance.get_host.return_value = {"name": "GitHub", "url": "https://github.com"}
        client_instance.get_repository.return_value = {"full_name": "owner/repo"}
        client_instance.get_registries.return_value = [{"name": "npm"}]
        client_instance.get_registry.return_value = {"name": "npm", "url": "https://npmjs.com"}
        client_instance.get_package.return_value = {"name": "express"}
        client_instance.get_package_version.return_value = {"version": "4.17.1"}
        client_instance.get_repo_summary.return_value = {"url": "https://github.com/owner/repo"}
        client_instance.get_package_summary.return_value = {"url": "https://npmjs.com/package/express"}

        def get_topic(name):
            return {"name": "test_topic", "repositories": []}

        client_instance.get_topic.side_effect = get_topic
        mock_client.return_value = client_instance
        yield client_instance


class TestReposCommands:
    """Test the repos commands."""

    def test_list_repos_operations(self, runner, mock_api_client):
        """Test listing repos operations."""
        # Arrange - done via fixtures

        # Act
        result = runner.invoke(main, ["repos", "list"])

        # Assert
        assert result.exit_code == 0

        # Strip ANSI escape codes for robust matching
        def strip_ansi(text):
            ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
            return ansi_escape.sub("", text)

        clean_output = strip_ansi(result.output)
        assert "test_op" in clean_output

    def test_get_topics(self, runner, mock_api_client):
        """Test getting all topics."""
        # Act
        result = runner.invoke(main, ["repos", "topics"])

        # Assert
        assert result.exit_code == 0
        assert "test_topic" in result.output

    def test_get_topic(self, runner, mock_api_client):
        """Test getting a specific topic."""
        # Act
        result = runner.invoke(main, ["repos", "topic", "test"])

        # Assert
        assert result.exit_code == 0
        assert "test_topic" in result.output

    def test_get_hosts(self, runner, mock_api_client):
        """Test getting all hosts."""
        # Act
        result = runner.invoke(main, ["repos", "hosts"])

        # Assert
        assert result.exit_code == 0
        assert "GitHub" in result.output

    def test_get_host(self, runner, mock_api_client):
        """Test getting a specific host."""
        # Act
        result = runner.invoke(main, ["repos", "host", "GitHub"])

        # Assert
        assert result.exit_code == 0
        assert "GitHub" in result.output

    def test_get_repository(self, runner, mock_api_client):
        """Test getting a specific repository."""
        # Act
        result = runner.invoke(main, ["repos", "repository", "GitHub", "owner", "repo"])

        # Assert
        assert result.exit_code == 0
        assert "owner/repo" in result.output


class TestPackagesCommands:
    """Test the packages commands."""

    def test_list_packages_operations(self, runner, mock_api_client):
        """Test listing packages operations."""
        # Act
        result = runner.invoke(main, ["packages", "list"])

        # Assert
        assert result.exit_code == 0

        # Strip ANSI escape codes and whitespace for robust matching
        def strip_ansi(text):
            ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
            return ansi_escape.sub("", text)

        clean_output = strip_ansi(result.output).replace(" ", "")
        assert "test_op" in clean_output

    def test_get_registries(self, runner, mock_api_client):
        """Test getting all registries."""
        # Act
        result = runner.invoke(main, ["packages", "registries"])

        # Assert
        assert result.exit_code == 0
        assert "npm" in result.output

    def test_get_registry(self, runner, mock_api_client):
        """Test getting a specific registry."""
        # Act
        result = runner.invoke(main, ["packages", "registry", "npm"])

        # Assert
        assert result.exit_code == 0
        assert "npm" in result.output

    def test_get_package(self, runner, mock_api_client):
        """Test getting a specific package."""
        # Act
        result = runner.invoke(main, ["packages", "package", "npm", "express"])

        # Assert
        assert result.exit_code == 0
        assert "express" in result.output

    def test_get_package_version(self, runner, mock_api_client):
        """Test getting a specific package version."""
        # Act
        result = runner.invoke(main, ["packages", "version", "npm", "express", "4.17.1"])

        # Assert
        assert result.exit_code == 0
        assert "4.17.1" in result.output


class TestSummaryCommands:
    """Test the summary commands."""

    def test_list_summary_operations(self, runner, mock_api_client):
        """Test listing summary operations."""
        # Act
        result = runner.invoke(main, ["summary", "list"])

        # Assert
        assert result.exit_code == 0
        assert "test_op" in result.output

    def test_get_repo_summary(self, runner, mock_api_client):
        """Test getting a repo summary."""
        # Act
        result = runner.invoke(main, ["summary", "repo", "https://github.com/owner/repo"])

        # Assert
        assert result.exit_code == 0
        assert "github.com/owner/repo" in result.output

    def test_get_package_summary(self, runner, mock_api_client):
        """Test getting a package summary."""
        # Act
        result = runner.invoke(main, ["summary", "package", "https://npmjs.com/package/express"])

        # Assert
        assert result.exit_code == 0
        assert "npmjs.com/package/express" in result.output


# Note: Testing dynamic commands is complex due to how they're registered at runtime
# We'll focus on testing the core functionality instead


class TestErrorHandling:
    """Test error handling in the CLI."""

    def test_invalid_json_params(self, runner, mock_api_client):
        """Test handling invalid JSON parameters."""
        # Act
        result = runner.invoke(main, ["repos", "call", "test_op", "--path-params", "{invalid json}"])

        # Assert
        assert result.exit_code != 0
        assert "Invalid JSON" in result.output

    def test_api_error_handling(self, runner, mock_api_client):
        """Test handling API errors."""
        # Arrange
        from ecosystems_cli.cli import get_client

        get_client.return_value.get_topic.side_effect = ValueError("Topic not found")

        # Act
        result = runner.invoke(main, ["repos", "topic", "nonexistent"])

        # Assert
        def strip_ansi(text):
            ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
            return ansi_escape.sub("", text)

        clean_output = strip_ansi(result.output)
        assert "Error: Topic not found" in clean_output
