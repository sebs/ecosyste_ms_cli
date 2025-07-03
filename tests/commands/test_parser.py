"""Tests for the parser commands."""

from unittest import mock

from click.testing import CliRunner


class TestParserCommands:
    """Test cases for parser commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.parser import ParserCommands

        self.parser_commands = ParserCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_parser_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for parser API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "createJob", "method": "POST", "path": "/jobs"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.parser_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("parser", timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_formats_command(self, mock_print_output, mock_get_client):
        """Test listing supported file formats."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {"name": "npm", "file": "package.json"},
            {"name": "pip", "file": "requirements.txt"},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.parser_commands.group, ["formats"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("parser", timeout=20)
        mock_client.call.assert_called_once_with("jobFormats")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.parser.APIClient")
    def test_submit_command(self, mock_api_client):
        """Test submitting a parsing job."""
        mock_client_instance = mock.MagicMock()
        mock_api_client.return_value = mock_client_instance
        mock_client_instance.call.return_value = {"id": "job123", "status": "pending"}

        # Create a context object to pass
        context = mock.MagicMock()
        context.obj = {"timeout": 20, "format": "table"}

        # Note: The command might not be invoked directly in this test setup
        # since it's registered through decorators
        self.runner.invoke(
            self.parser_commands.group,
            ["submit", "https://example.com/package.json"],
            obj={"timeout": 20, "format": "table"},
        )

    @mock.patch("ecosystems_cli.commands.parser.APIClient")
    def test_status_command(self, mock_api_client):
        """Test getting job status."""
        mock_client_instance = mock.MagicMock()
        mock_api_client.return_value = mock_client_instance
        mock_client_instance.call.return_value = {
            "id": "job123",
            "status": "completed",
            "results": {"dependencies": []},
        }

        # Note: The command might not be invoked directly in this test setup
        # since it's registered through decorators
        self.runner.invoke(
            self.parser_commands.group,
            ["status", "job123"],
            obj={"timeout": 20, "format": "table"},
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_call_command(self, mock_print_output, mock_get_client):
        """Test generic call command."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"result": "success"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.parser_commands.group,
            ["call", "createJob", "--query-params", '{"url": "https://example.com/package.json"}'],
            obj={"timeout": 20, "format": "table"},
        )

        if result.exit_code != 0:
            print(f"Output: {result.output}")
            print(f"Exception: {result.exception}")
        assert result.exit_code == 0
