"""Tests for the commits commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestCommitsCommands:
    """Test cases for commits commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.commits import CommitsCommands

        self.commits_commands = CommitsCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_commits_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for commits API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [
            {"operation_id": "repositoriesLookup", "method": "GET", "path": "/repositories/lookup"}
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.commits_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("commits", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_hosts(self, mock_print_output, mock_get_client):
        """Test getting all hosts."""
        mock_client = mock.MagicMock()
        mock_client.getRegistries.return_value = {"hosts": ["github.com", "gitlab.com"]}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.commits_commands.group, ["hosts"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("commits", base_url=None, timeout=20)
        mock_client.getRegistries.assert_called_once()
        mock_print_output.assert_called_once_with({"hosts": ["github.com", "gitlab.com"]}, "table", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_lookup_repository(self, mock_print_output, mock_get_client):
        """Test looking up a repository by URL."""
        mock_client = mock.MagicMock()
        mock_client.repositoriesLookup.return_value = {"full_name": "owner/repo", "host": "github.com", "stars": 100}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.commits_commands.group, ["lookup", "https://github.com/owner/repo"], obj={"timeout": 20, "format": "json"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("commits", base_url=None, timeout=20)
        mock_client.repositoriesLookup.assert_called_once_with(url="https://github.com/owner/repo")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_lookup_repository_error(self, mock_print_error, mock_get_client):
        """Test error handling when looking up a repository."""
        mock_client = mock.MagicMock()
        mock_client.repositoriesLookup.side_effect = Exception("Repository not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.commits_commands.group, ["lookup", "https://invalid.com/repo"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Repository not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_host(self, mock_print_output, mock_get_client):
        """Test getting a specific host."""
        mock_client = mock.MagicMock()
        mock_client.getHost.return_value = {"name": "github.com", "repositories_count": 1000000}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.commits_commands.group, ["host", "github.com"], obj={"timeout": 20, "format": "tsv"})

        assert result.exit_code == 0
        mock_client.getHost.assert_called_once_with(host_name="github.com")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_host_repositories(self, mock_print_output, mock_get_client):
        """Test getting repositories from a specific host."""
        mock_client = mock.MagicMock()
        mock_client.getHostRepositories.return_value = {
            "repositories": [{"full_name": "owner1/repo1", "stars": 100}, {"full_name": "owner2/repo2", "stars": 200}]
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.commits_commands.group, ["host-repositories", "github.com"], obj={"timeout": 20, "format": "jsonl"}
        )

        assert result.exit_code == 0
        mock_client.getHostRepositories.assert_called_once_with(host_name="github.com")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_repository(self, mock_print_output, mock_get_client):
        """Test getting a specific repository from a host."""
        mock_client = mock.MagicMock()
        mock_client.getHostRepository.return_value = {
            "full_name": "owner/repo",
            "host": "github.com",
            "stars": 150,
            "forks": 25,
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.commits_commands.group, ["repository", "github.com", "owner/repo"], obj={"timeout": 20, "format": "json"}
        )

        assert result.exit_code == 0
        mock_client.getHostRepository.assert_called_once_with(host_name="github.com", repo_name="owner/repo")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_commits(self, mock_print_output, mock_get_client):
        """Test getting commits from a repository."""
        mock_client = mock.MagicMock()
        mock_client.getRepositoryCommits.return_value = {
            "commits": [
                {"sha": "abc123", "message": "Initial commit", "author": "user1"},
                {"sha": "def456", "message": "Add feature", "author": "user2"},
            ]
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.commits_commands.group, ["commits", "github.com", "owner/repo"], obj={"timeout": 20, "format": "table"}
        )

        assert result.exit_code == 0
        mock_client.getRepositoryCommits.assert_called_once_with(host_name="github.com", repo_name="owner/repo")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_commits_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting commits."""
        mock_client = mock.MagicMock()
        mock_client.getRepositoryCommits.side_effect = Exception("Repository not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.commits_commands.group, ["commits", "github.com", "nonexistent/repo"], obj={"timeout": 20}
        )

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Repository not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_commits_operation(self, mock_call_operation):
        """Test calling a generic operation on commits API."""
        result = self.runner.invoke(
            self.commits_commands.group,
            [
                "call",
                "repositoriesLookup",
                "--query-params",
                json.dumps({"url": "https://github.com/owner/repo"}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "commits"
        assert args[1] == "repositoriesLookup"
        assert args[3] == json.dumps({"url": "https://github.com/owner/repo"})

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_commits_operation_with_path_params(self, mock_call_operation):
        """Test calling a generic operation with path parameters."""
        result = self.runner.invoke(
            self.commits_commands.group,
            [
                "call",
                "getHostRepository",
                "--path-params",
                json.dumps({"host": "github.com", "name": "owner/repo"}),
                "--query-params",
                json.dumps({"include": "commits"}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "commits"
        assert args[1] == "getHostRepository"
        assert args[2] == json.dumps({"host": "github.com", "name": "owner/repo"})
        assert args[3] == json.dumps({"include": "commits"})
