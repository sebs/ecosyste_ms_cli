"""Tests for the opencollective commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestOpenCollectiveCommands:
    """Test cases for opencollective commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.opencollective import OpenCollectiveCommands

        self.opencollective_commands = OpenCollectiveCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_opencollective_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for opencollective API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "getProject", "method": "GET", "path": "/projects/{id}"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.opencollective_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("opencollective", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_projects(self, mock_print_output, mock_get_client):
        """Test getting all projects."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"id": 1, "url": "https://opencollective.com/project1"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.opencollective_commands.group, ["projects"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("opencollective", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with("getProjects")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_project(self, mock_print_output, mock_get_client):
        """Test getting a specific project."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"id": 123, "url": "https://opencollective.com/project123"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.opencollective_commands.group, ["project", "123"], obj={"timeout": 20, "format": "json"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("opencollective", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with("getProject", path_params={"id": 123}, query_params={})
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_lookup_project(self, mock_print_output, mock_get_client):
        """Test looking up a project by URL."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"id": 1, "url": "https://github.com/test/repo"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.opencollective_commands.group, ["lookup-project", "https://github.com/test/repo"], obj={"timeout": 20}
        )

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with(
            "lookupProject", path_params={}, query_params={"url": "https://github.com/test/repo"}
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_projects_packages(self, mock_print_output, mock_get_client):
        """Test getting projects with packages."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"id": 1, "packages": ["package1", "package2"]}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.opencollective_commands.group, ["projects-packages"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with("getProjectPackages")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_collectives(self, mock_print_output, mock_get_client):
        """Test getting all collectives."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"id": 1, "name": "Collective 1"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.opencollective_commands.group, ["collectives"], obj={"timeout": 20, "format": "tsv"})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with("getCollectives")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_collective(self, mock_print_output, mock_get_client):
        """Test getting a specific collective."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"id": 456, "name": "Test Collective"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.opencollective_commands.group, ["collective", "456"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with("getCollective", path_params={"id": 456}, query_params={})

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_collective_projects(self, mock_print_output, mock_get_client):
        """Test getting projects for a collective."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"id": 1, "url": "https://github.com/test/repo"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.opencollective_commands.group, ["collective-projects", "webpack"], obj={"timeout": 20, "format": "jsonl"}
        )

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with("getCollectiveProjects", path_params={"slug": "webpack"}, query_params={})

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_project_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a project."""
        mock_client = mock.MagicMock()
        mock_client.call.side_effect = Exception("Project not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.opencollective_commands.group, ["project", "999"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Project not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_opencollective_operation(self, mock_call_operation):
        """Test calling a generic operation on opencollective API."""
        result = self.runner.invoke(
            self.opencollective_commands.group,
            [
                "call",
                "getProject",
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
        assert args[0] == "opencollective"
        assert args[1] == "getProject"
        assert args[2] == json.dumps({"id": 123})
        assert args[3] == json.dumps({"include": "meta"})
