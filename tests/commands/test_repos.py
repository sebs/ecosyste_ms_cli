"""Tests for the repos commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestReposCommands:
    """Test cases for repos commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.repos import ReposCommands

        self.repos_commands = ReposCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_repos_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for repos API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "get_repo", "method": "GET", "path": "/repos/{id}"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.repos_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_topics(self, mock_print_output, mock_get_client):
        """Test getting all topics."""
        mock_client = mock.MagicMock()
        mock_client.get_topics.return_value = {"topics": ["python", "javascript"]}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.repos_commands.group, ["topics"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", timeout=20)
        mock_client.get_topics.assert_called_once()
        mock_print_output.assert_called_once_with({"topics": ["python", "javascript"]}, "table", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_topic(self, mock_print_output, mock_get_client):
        """Test getting a specific topic."""
        mock_client = mock.MagicMock()
        mock_client.get_topic.return_value = {"name": "python", "count": 1000}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.repos_commands.group, ["topic", "python"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", timeout=20)
        mock_client.get_topic.assert_called_once_with(name="python")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_topic_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a topic."""
        mock_client = mock.MagicMock()
        mock_client.get_topic.side_effect = Exception("Topic not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.repos_commands.group, ["topic", "nonexistent"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Topic not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_hosts(self, mock_print_output, mock_get_client):
        """Test getting all hosts."""
        mock_client = mock.MagicMock()
        mock_client.get_hosts.return_value = {"hosts": ["github.com", "gitlab.com"]}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.repos_commands.group, ["hosts"], obj={"timeout": 20, "format": "tsv"})

        assert result.exit_code == 0
        mock_client.get_hosts.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_host(self, mock_print_output, mock_get_client):
        """Test getting a specific host."""
        mock_client = mock.MagicMock()
        mock_client.get_host.return_value = {"name": "github.com", "repos": 1000000}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.repos_commands.group, ["host", "github.com"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.get_host.assert_called_once_with(name="github.com")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_repository(self, mock_print_output, mock_get_client):
        """Test getting a specific repository."""
        mock_client = mock.MagicMock()
        mock_client.get_repository.return_value = {"full_name": "owner/repo", "stars": 100}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.repos_commands.group, ["repository", "github.com", "owner", "repo"], obj={"timeout": 20, "format": "jsonl"}
        )

        assert result.exit_code == 0
        mock_client.get_repository.assert_called_once_with(host="github.com", owner="owner", repo="repo")

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_repos_operation(self, mock_call_operation):
        """Test calling a generic operation on repos API."""
        result = self.runner.invoke(
            self.repos_commands.group,
            [
                "call",
                "get_repo",
                "--path-params",
                json.dumps({"id": 123}),
                "--query-params",
                json.dumps({"include": "meta"}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "repos"
        assert args[1] == "get_repo"
        assert args[2] == json.dumps({"id": 123})
        assert args[3] == json.dumps({"include": "meta"})
