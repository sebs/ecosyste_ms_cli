"""Tests for the repos commands."""

import json
from unittest import mock

import pytest
from click.testing import CliRunner

from ecosystems_cli.commands.repos import (
    call_repos_operation,
    get_host,
    get_hosts,
    get_repository,
    get_topic,
    get_topics,
    list_repos_operations,
    repos,
)


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def mock_client():
    """Create a mock API client for repos API."""
    with mock.patch("ecosystems_cli.commands.repos.get_client") as mock_get_client:
        client_instance = mock.MagicMock()
        mock_get_client.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_print_operations():
    """Mock the print_operations function."""
    with mock.patch("ecosystems_cli.commands.repos.print_operations") as mock_print:
        yield mock_print


@pytest.fixture
def mock_print_output():
    """Mock the print_output function."""
    with mock.patch("ecosystems_cli.commands.repos.print_output") as mock_print:
        yield mock_print


@pytest.fixture
def mock_print_error():
    """Mock the print_error function."""
    with mock.patch("ecosystems_cli.commands.repos.print_error") as mock_print:
        yield mock_print


@pytest.fixture
def ctx():
    """Create a mock context object."""
    context = mock.MagicMock()
    context.obj = {"timeout": 30, "format": "table"}
    return context


class TestReposGroup:
    """Test the repos group command."""

    def test_repos_group(self, runner):
        """Test that the repos group is properly defined."""
        result = runner.invoke(repos, ["--help"])
        assert result.exit_code == 0
        assert "Commands for the repos API" in result.output


class TestListReposOperations:
    """Test the list repos operations command."""

    def test_list_operations_success(self, runner, ctx, mock_client, mock_print_operations):
        """Test successful listing of operations."""
        # Arrange
        operations = [
            {"id": "get_topics", "method": "GET", "path": "/topics"},
            {"id": "get_repository", "method": "GET", "path": "/hosts/{host}/owners/{owner}/repos/{repo}"},
        ]
        mock_client.list_operations.return_value = operations

        # Act
        result = runner.invoke(list_repos_operations, obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.list_operations.assert_called_once()
        # Note: print_operations is called with console as positional arg in repos.py
        mock_print_operations.assert_called_once_with(operations, mock.ANY)

    def test_list_operations_with_custom_timeout(self, runner, mock_client, mock_print_operations):
        """Test listing operations with custom timeout."""
        # Arrange
        ctx_with_timeout = mock.MagicMock()
        ctx_with_timeout.obj = {"timeout": 60}

        # Act
        with mock.patch("ecosystems_cli.commands.repos.get_client") as mock_get_client:
            mock_get_client.return_value = mock_client
            result = runner.invoke(list_repos_operations, obj=ctx_with_timeout.obj)

        # Assert
        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", timeout=60)


class TestGetTopics:
    """Test the get topics command."""

    def test_get_topics_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of topics."""
        # Arrange
        topics = [
            {"name": "javascript", "repositories_count": 1000000},
            {"name": "python", "repositories_count": 500000},
        ]
        mock_client.get_topics.return_value = topics

        # Act
        result = runner.invoke(get_topics, obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_topics.assert_called_once()
        mock_print_output.assert_called_once_with(topics, "table", console=mock.ANY)

    def test_get_topics_with_json_format(self, runner, mock_client, mock_print_output):
        """Test getting topics with JSON output format."""
        # Arrange
        ctx_json = mock.MagicMock()
        ctx_json.obj = {"timeout": 20, "format": "json"}
        topics = [{"name": "rust"}]
        mock_client.get_topics.return_value = topics

        # Act
        result = runner.invoke(get_topics, obj=ctx_json.obj)

        # Assert
        assert result.exit_code == 0
        mock_print_output.assert_called_once_with(topics, "json", console=mock.ANY)


class TestGetTopic:
    """Test the get topic command."""

    def test_get_topic_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of a specific topic."""
        # Arrange
        topic = {
            "name": "javascript",
            "repositories_count": 1000000,
            "description": "JavaScript programming language",
        }
        mock_client.get_topic.return_value = topic

        # Act
        result = runner.invoke(get_topic, ["javascript"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_topic.assert_called_once_with("javascript")
        mock_print_output.assert_called_once_with(topic, "table", console=mock.ANY)

    def test_get_topic_not_found(self, runner, ctx, mock_client, mock_print_error):
        """Test handling of topic not found error."""
        # Arrange
        mock_client.get_topic.side_effect = Exception("Topic not found")

        # Act
        result = runner.invoke(get_topic, ["nonexistent"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0  # Click doesn't set exit code for handled exceptions
        mock_client.get_topic.assert_called_once_with("nonexistent")
        mock_print_error.assert_called_once_with("Topic not found", console=mock.ANY)

    def test_get_topic_with_special_characters(self, runner, ctx, mock_client, mock_print_output):
        """Test getting a topic with special characters."""
        # Arrange
        topic = {"name": "c++", "repositories_count": 100000}
        mock_client.get_topic.return_value = topic

        # Act
        result = runner.invoke(get_topic, ["c++"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_topic.assert_called_once_with("c++")


class TestGetHosts:
    """Test the get hosts command."""

    def test_get_hosts_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of hosts."""
        # Arrange
        hosts = [
            {"name": "GitHub", "url": "https://github.com", "repositories_count": 100000000},
            {"name": "GitLab", "url": "https://gitlab.com", "repositories_count": 10000000},
        ]
        mock_client.get_hosts.return_value = hosts

        # Act
        result = runner.invoke(get_hosts, obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_hosts.assert_called_once()
        mock_print_output.assert_called_once_with(hosts, "table", console=mock.ANY)

    def test_get_hosts_empty_result(self, runner, ctx, mock_client, mock_print_output):
        """Test getting hosts when no hosts are available."""
        # Arrange
        mock_client.get_hosts.return_value = []

        # Act
        result = runner.invoke(get_hosts, obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_print_output.assert_called_once_with([], "table", console=mock.ANY)


class TestGetHost:
    """Test the get host command."""

    def test_get_host_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of a specific host."""
        # Arrange
        host = {
            "name": "GitHub",
            "url": "https://github.com",
            "repositories_count": 100000000,
            "api_url": "https://api.github.com",
        }
        mock_client.get_host.return_value = host

        # Act
        result = runner.invoke(get_host, ["GitHub"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_host.assert_called_once_with("GitHub")
        mock_print_output.assert_called_once_with(host, "table", console=mock.ANY)

    def test_get_host_case_sensitive(self, runner, ctx, mock_client, mock_print_output):
        """Test that host names are case sensitive."""
        # Arrange
        host = {"name": "GitHub"}
        mock_client.get_host.return_value = host

        # Act
        result = runner.invoke(get_host, ["github"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_host.assert_called_once_with("github")

    def test_get_host_error(self, runner, ctx, mock_client, mock_print_error):
        """Test handling of host retrieval error."""
        # Arrange
        mock_client.get_host.side_effect = Exception("Host not found")

        # Act
        result = runner.invoke(get_host, ["NonExistentHost"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Host not found", console=mock.ANY)


class TestGetRepository:
    """Test the get repository command."""

    def test_get_repository_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of a repository."""
        # Arrange
        repository = {
            "full_name": "microsoft/vscode",
            "host": "GitHub",
            "owner": "microsoft",
            "name": "vscode",
            "description": "Visual Studio Code",
            "stars": 150000,
            "forks": 25000,
        }
        mock_client.get_repository.return_value = repository

        # Act
        result = runner.invoke(get_repository, ["GitHub", "microsoft", "vscode"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_repository.assert_called_once_with("GitHub", "microsoft", "vscode")
        mock_print_output.assert_called_once_with(repository, "table", console=mock.ANY)

    def test_get_repository_with_special_chars(self, runner, ctx, mock_client, mock_print_output):
        """Test getting a repository with special characters in name."""
        # Arrange
        repository = {"full_name": "user/my-repo.js"}
        mock_client.get_repository.return_value = repository

        # Act
        result = runner.invoke(get_repository, ["GitHub", "user", "my-repo.js"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_repository.assert_called_once_with("GitHub", "user", "my-repo.js")

    def test_get_repository_error(self, runner, ctx, mock_client, mock_print_error):
        """Test handling of repository retrieval error."""
        # Arrange
        mock_client.get_repository.side_effect = Exception("Repository not found")

        # Act
        result = runner.invoke(get_repository, ["GitHub", "nonexistent", "repo"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Repository not found", console=mock.ANY)

    def test_get_repository_with_org(self, runner, ctx, mock_client, mock_print_output):
        """Test getting a repository owned by an organization."""
        # Arrange
        repository = {
            "full_name": "facebook/react",
            "host": "GitHub",
            "owner": "facebook",
            "name": "react",
            "organization": True,
        }
        mock_client.get_repository.return_value = repository

        # Act
        result = runner.invoke(get_repository, ["GitHub", "facebook", "react"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_repository.assert_called_once_with("GitHub", "facebook", "react")


class TestCallReposOperation:
    """Test the call repos operation command."""

    def test_call_operation_success(self, runner, ctx):
        """Test successful operation call."""
        # Arrange
        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_repos_operation,
                ["get_topics"],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with("repos", "get_topics", None, None, None, mock.ANY)

    def test_call_operation_with_path_params(self, runner, ctx):
        """Test operation call with path parameters."""
        # Arrange
        path_params = {"host": "GitHub", "owner": "microsoft", "repo": "vscode"}
        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_repos_operation,
                ["get_repository", "--path-params", json.dumps(path_params)],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with(
                "repos",
                "get_repository",
                json.dumps(path_params),
                None,
                None,
                mock.ANY,
            )

    def test_call_operation_with_query_params(self, runner, ctx):
        """Test operation call with query parameters."""
        # Arrange
        query_params = {"page": 1, "per_page": 100}
        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_repos_operation,
                ["list_repositories", "--query-params", json.dumps(query_params)],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with(
                "repos",
                "list_repositories",
                None,
                json.dumps(query_params),
                None,
                mock.ANY,
            )

    def test_call_operation_with_all_params(self, runner, ctx):
        """Test operation call with all parameter types."""
        # Arrange
        path_params = {"host": "GitHub"}
        query_params = {"q": "language:python", "sort": "stars"}
        body = {"filters": {"min_stars": 100}}

        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_repos_operation,
                [
                    "search_host_repositories",
                    "--path-params",
                    json.dumps(path_params),
                    "--query-params",
                    json.dumps(query_params),
                    "--body",
                    json.dumps(body),
                ],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with(
                "repos",
                "search_host_repositories",
                json.dumps(path_params),
                json.dumps(query_params),
                json.dumps(body),
                mock.ANY,
            )
