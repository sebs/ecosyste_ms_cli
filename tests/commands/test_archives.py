"""Tests for the archives commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestArchivesCommands:
    """Test cases for archives commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.archives import ArchivesCommands

        self.archives_commands = ArchivesCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_archives_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for archives API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "list", "method": "GET", "path": "/archives/list"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.archives_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("archives", timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_list_files(self, mock_print_output, mock_get_client):
        """Test listing files in an archive."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = ["package.json", "README.md", "lib/express.js"]
        mock_get_client.return_value = mock_client

        test_url = "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
        result = self.runner.invoke(
            self.archives_commands.group, ["list-files", test_url], obj={"timeout": 20, "format": "table"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("archives", timeout=20)
        mock_client.call.assert_called_once_with("list", path_params={}, query_params={"url": test_url})
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_contents(self, mock_print_output, mock_get_client):
        """Test getting contents of a path from an archive."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "name": "package.json",
            "directory": False,
            "contents": '{"name": "express", "version": "4.18.2"}',
        }
        mock_get_client.return_value = mock_client

        test_url = "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
        test_path = "package.json"
        result = self.runner.invoke(
            self.archives_commands.group, ["contents", test_url, test_path], obj={"timeout": 20, "format": "json"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("archives", timeout=20)
        mock_client.call.assert_called_once_with("contents", path_params={}, query_params={"url": test_url, "path": test_path})
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_readme(self, mock_print_output, mock_get_client):
        """Test getting readme from an archive."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "name": "README.md",
            "raw": "# Express\n\nFast, unopinionated, minimalist web framework",
            "html": "<h1>Express</h1><p>Fast, unopinionated, minimalist web framework</p>",
            "extension": ".md",
        }
        mock_get_client.return_value = mock_client

        test_url = "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
        result = self.runner.invoke(self.archives_commands.group, ["readme", test_url], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("archives", timeout=20)
        mock_client.call.assert_called_once_with("readme", path_params={}, query_params={"url": test_url})

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_changelog(self, mock_print_output, mock_get_client):
        """Test getting changelog from an archive."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "name": "CHANGELOG.md",
            "raw": "# Changelog\n\n## 4.18.2\n- Bug fixes",
            "html": "<h1>Changelog</h1><h2>4.18.2</h2><ul><li>Bug fixes</li></ul>",
            "extension": ".md",
        }
        mock_get_client.return_value = mock_client

        test_url = "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
        result = self.runner.invoke(self.archives_commands.group, ["changelog", test_url], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("archives", timeout=20)
        mock_client.call.assert_called_once_with("changelog", path_params={}, query_params={"url": test_url})

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_repopack(self, mock_print_output, mock_get_client):
        """Test getting repopack from an archive."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"output": "Repository Pack output..."}
        mock_get_client.return_value = mock_client

        test_url = "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
        result = self.runner.invoke(self.archives_commands.group, ["repopack", test_url], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("archives", timeout=20)
        mock_client.call.assert_called_once_with("repopack", path_params={}, query_params={"url": test_url})

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_archives_error_handling(self, mock_print_error, mock_get_client):
        """Test error handling for archives commands."""
        mock_client = mock.MagicMock()
        mock_client.call.side_effect = Exception("Archive not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.archives_commands.group, ["list-files", "https://invalid.url"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Archive not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_archives_operation(self, mock_call_operation):
        """Test calling a generic operation on archives API."""
        result = self.runner.invoke(
            self.archives_commands.group,
            [
                "call",
                "list",
                "--query-params",
                json.dumps({"url": "https://registry.npmjs.org/express/-/express-4.18.2.tgz"}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "archives"
        assert args[1] == "list"
        assert args[3] == json.dumps({"url": "https://registry.npmjs.org/express/-/express-4.18.2.tgz"})
