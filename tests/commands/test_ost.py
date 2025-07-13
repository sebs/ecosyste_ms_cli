"""Tests for the OST commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestOSTCommands:
    """Test cases for OST commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.ost import OSTCommands

        self.ost_commands = OSTCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_ost_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for OST API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "get_project", "method": "GET", "path": "/projects/{id}"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ost_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ost", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_projects(self, mock_print_output, mock_get_client):
        """Test getting all projects."""
        mock_client = mock.MagicMock()
        mock_client.get_projects.return_value = [{"id": 1, "url": "https://github.com/example/project"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ost_commands.group, ["projects"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ost", base_url=None, timeout=20)
        mock_client.get_projects.assert_called_once()
        mock_print_output.assert_called_once_with(
            [{"id": 1, "url": "https://github.com/example/project"}], "table", console=mock.ANY
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_project(self, mock_print_output, mock_get_client):
        """Test getting a specific project."""
        mock_client = mock.MagicMock()
        mock_client.get_project.return_value = {"id": 1, "url": "https://github.com/example/project", "category": "climate"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ost_commands.group, ["project", "1"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ost", base_url=None, timeout=20)
        mock_client.get_project.assert_called_once_with(id=1)
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_project_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a project."""
        mock_client = mock.MagicMock()
        mock_client.get_project.side_effect = Exception("Project not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ost_commands.group, ["project", "999"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Project not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_lookup_project(self, mock_print_output, mock_get_client):
        """Test looking up project by URL."""
        mock_client = mock.MagicMock()
        mock_client.lookup_project.return_value = {"id": 1, "url": "https://github.com/example/project"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.ost_commands.group, ["lookup-project", "https://github.com/example/project"], obj={"timeout": 20}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ost", base_url=None, timeout=20)
        mock_client.lookup_project.assert_called_once_with(url="https://github.com/example/project")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_issues(self, mock_print_output, mock_get_client):
        """Test getting all issues."""
        mock_client = mock.MagicMock()
        mock_client.get_issues.return_value = [{"uuid": 1, "title": "Issue 1", "state": "open"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ost_commands.group, ["issues"], obj={"timeout": 20, "format": "jsonl"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ost", base_url=None, timeout=20)
        mock_client.get_issues.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_openclimateaction_issues(self, mock_print_output, mock_get_client):
        """Test getting OpenClimateAction issues."""
        mock_client = mock.MagicMock()
        mock_client.get_open_climate_action_issues.return_value = [{"uuid": 2, "title": "Climate Issue", "state": "open"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ost_commands.group, ["openclimateaction-issues"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ost", base_url=None, timeout=20)
        mock_client.get_open_climate_action_issues.assert_called_once()

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_ost_operation(self, mock_call_operation):
        """Test calling a generic operation on OST API."""
        result = self.runner.invoke(
            self.ost_commands.group,
            [
                "call",
                "get_project",
                "--path-params",
                json.dumps({"id": 1}),
                "--query-params",
                json.dumps({"include": "details"}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "ost"
        assert args[1] == "get_project"
        assert args[2] == json.dumps({"id": 1})
        assert args[3] == json.dumps({"include": "details"})
