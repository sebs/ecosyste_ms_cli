"""Tests for the ruby commands."""

from unittest import mock

from click.testing import CliRunner


class TestRubyCommands:
    """Test cases for ruby commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.ruby import RubyCommands

        self.ruby_commands = RubyCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_ruby_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for ruby API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "getProject", "method": "GET", "path": "/projects/{id}"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ruby_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ruby", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_projects(self, mock_print_output, mock_get_client):
        """Test getting all projects."""
        mock_client = mock.MagicMock()
        mock_client.getProjects.return_value = [{"id": 1, "url": "https://github.com/rails/rails"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ruby_commands.group, ["projects"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ruby", base_url=None, timeout=20)
        mock_client.getProjects.assert_called_once()
        mock_print_output.assert_called_once_with(
            [{"id": 1, "url": "https://github.com/rails/rails"}], "table", console=mock.ANY
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_project(self, mock_print_output, mock_get_client):
        """Test getting a specific project."""
        mock_client = mock.MagicMock()
        mock_client.getProject.return_value = {"id": 1, "url": "https://github.com/rails/rails", "language": "Ruby"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ruby_commands.group, ["project", "1"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("ruby", base_url=None, timeout=20)
        mock_client.getProject.assert_called_once_with(project_id=1)
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_project_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a project."""
        mock_client = mock.MagicMock()
        mock_client.getProject.side_effect = Exception("Project not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ruby_commands.group, ["project", "99999"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Project not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_lookup_project(self, mock_print_output, mock_get_client):
        """Test looking up a project by URL."""
        mock_client = mock.MagicMock()
        mock_client.lookupProject.return_value = {"id": 1, "url": "https://github.com/rails/rails"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.ruby_commands.group, ["lookup-project", "https://github.com/rails/rails"], obj={"timeout": 20}
        )

        assert result.exit_code == 0
        mock_client.lookupProject.assert_called_once_with(url="https://github.com/rails/rails")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_project_packages(self, mock_print_output, mock_get_client):
        """Test getting projects with packages."""
        mock_client = mock.MagicMock()
        mock_client.getProjectPackages.return_value = [{"id": 1, "packages": [{"name": "rails"}]}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ruby_commands.group, ["project-packages"], obj={"timeout": 20, "format": "tsv"})

        assert result.exit_code == 0
        mock_client.getProjectPackages.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_issues(self, mock_print_output, mock_get_client):
        """Test getting all issues."""
        mock_client = mock.MagicMock()
        mock_client.getIssues.return_value = [{"uuid": 123, "title": "Test issue", "state": "open"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.ruby_commands.group, ["issues"], obj={"timeout": 20, "format": "jsonl"})

        assert result.exit_code == 0
        mock_client.getIssues.assert_called_once()
