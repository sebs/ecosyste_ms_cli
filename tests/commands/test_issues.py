"""Tests for the issues commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestIssuesCommands:
    """Test cases for issues commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.issues import IssuesCommands

        self.issues_commands = IssuesCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_issues_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for issues API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "getHost", "method": "GET", "path": "/hosts/{hostName}"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.issues_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("issues", timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_hosts(self, mock_print_output, mock_get_client):
        """Test getting all hosts."""
        mock_client = mock.MagicMock()
        mock_client.getRegistries.return_value = [{"name": "github.com", "repositories_count": 1000}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.issues_commands.group, ["hosts"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("issues", timeout=20)
        mock_client.getRegistries.assert_called_once()
        mock_print_output.assert_called_once_with(
            [{"name": "github.com", "repositories_count": 1000}], "table", console=mock.ANY
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_host(self, mock_print_output, mock_get_client):
        """Test getting a specific host."""
        mock_client = mock.MagicMock()
        mock_client.getHost.return_value = {"name": "github.com", "repositories_count": 1000000}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.issues_commands.group, ["host", "github.com"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("issues", timeout=20)
        mock_client.getHost.assert_called_once_with(host_name="github.com")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_host_repositories(self, mock_print_output, mock_get_client):
        """Test getting repositories from a host."""
        mock_client = mock.MagicMock()
        mock_client.getHostRepositories.return_value = [{"full_name": "owner/repo", "issues_count": 10}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.issues_commands.group, ["host-repositories", "github.com"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.getHostRepositories.assert_called_once_with(host_name="github.com")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_repository(self, mock_print_output, mock_get_client):
        """Test getting a specific repository."""
        mock_client = mock.MagicMock()
        mock_client.getHostRepository.return_value = {"full_name": "owner/repo", "issues_count": 100}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.issues_commands.group, ["repository", "github.com", "owner/repo"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.getHostRepository.assert_called_once_with(host_name="github.com", repo_name="owner/repo")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_repository_issues(self, mock_print_output, mock_get_client):
        """Test getting issues from a repository."""
        mock_client = mock.MagicMock()
        mock_client.getHostRepositoryIssues.return_value = [{"number": 1, "title": "Test issue"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.issues_commands.group, ["repository-issues", "github.com", "owner/repo"], obj={"timeout": 20}
        )

        assert result.exit_code == 0
        mock_client.getHostRepositoryIssues.assert_called_once_with(host_name="github.com", repo_name="owner/repo")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_issue(self, mock_print_output, mock_get_client):
        """Test getting a specific issue."""
        mock_client = mock.MagicMock()
        mock_client.getHostRepositoryIssue.return_value = {"number": 123, "title": "Bug report", "state": "open"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.issues_commands.group, ["issue", "github.com", "owner/repo", "123"], obj={"timeout": 20}
        )

        assert result.exit_code == 0
        mock_client.getHostRepositoryIssue.assert_called_once_with(
            host_name="github.com", repo_name="owner/repo", issue_number=123
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_lookup_repository(self, mock_print_output, mock_get_client):
        """Test repository lookup by URL."""
        mock_client = mock.MagicMock()
        mock_client.repositoriesLookup.return_value = {"full_name": "owner/repo", "html_url": "https://github.com/owner/repo"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.issues_commands.group, ["lookup", "https://github.com/owner/repo"], obj={"timeout": 20}
        )

        assert result.exit_code == 0
        mock_client.repositoriesLookup.assert_called_once_with(url="https://github.com/owner/repo")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_host_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a host."""
        mock_client = mock.MagicMock()
        mock_client.getHost.side_effect = Exception("Host not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.issues_commands.group, ["host", "nonexistent.com"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Host not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_issues_operation(self, mock_call_operation):
        """Test calling a generic operation on issues API."""
        result = self.runner.invoke(
            self.issues_commands.group,
            [
                "call",
                "getHost",
                "--path-params",
                json.dumps({"hostName": "github.com"}),
                "--query-params",
                json.dumps({"page": 1}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "issues"
        assert args[1] == "getHost"
        assert args[2] == json.dumps({"hostName": "github.com"})
        assert args[3] == json.dumps({"page": 1})
