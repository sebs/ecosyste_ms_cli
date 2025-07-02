"""Tests for the base command class."""

from unittest.mock import MagicMock, patch

import click

from ecosystems_cli.commands.base import BaseCommand


class TestBaseCommand:
    """Test cases for BaseCommand class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.base_command = BaseCommand("test_api", "Test API commands")

    def test_init(self):
        """Test BaseCommand initialization."""
        assert self.base_command.api_name == "test_api"
        assert self.base_command.description == "Test API commands"
        assert self.base_command.console is not None
        assert isinstance(self.base_command.group, click.Group)

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_operations")
    def test_list_operations(self, mock_print_operations, mock_get_client):
        """Test list_operations command creation."""
        # Create mock client
        mock_client = MagicMock()
        mock_client.list_operations.return_value = ["op1", "op2"]
        mock_get_client.return_value = mock_client

        # Create the command
        list_cmd = self.base_command.list_operations()

        # Test that it's a Click command
        assert isinstance(list_cmd, click.Command)
        assert list_cmd.name == "list"

        # Test command execution using invoke
        from click.testing import CliRunner

        runner = CliRunner()
        ctx = MagicMock()
        ctx.obj = {"timeout": 30}

        with runner.isolated_filesystem():
            runner.invoke(list_cmd, obj={"timeout": 30})

        # Verify calls
        mock_get_client.assert_called_once_with("test_api", timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once_with(["op1", "op2"], console=self.base_command.console)

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    def test_create_simple_command(self, mock_print_output, mock_get_client):
        """Test create_simple_command."""
        # Create mock client
        mock_client = MagicMock()
        mock_client.test_method.return_value = {"result": "test"}
        mock_get_client.return_value = mock_client

        # Create the command
        simple_cmd = self.base_command.create_simple_command("test_cmd", "test_method", "Test command description")

        # Test that it's a Click command
        assert isinstance(simple_cmd, click.Command)
        assert simple_cmd.name == "test_cmd"
        assert simple_cmd.help == "Test command description"

        # Test command execution using invoke
        from click.testing import CliRunner

        runner = CliRunner()

        runner.invoke(simple_cmd, obj={"timeout": 20, "format": "json"})

        # Verify calls
        mock_get_client.assert_called_once_with("test_api", timeout=20)
        mock_client.test_method.assert_called_once()
        mock_print_output.assert_called_once_with({"result": "test"}, "json", console=self.base_command.console)

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    @patch("ecosystems_cli.commands.base.print_error")
    def test_create_command_with_error_handling_success(self, mock_print_error, mock_print_output, mock_get_client):
        """Test create_command_with_error_handling for successful execution."""
        # Create mock client
        mock_client = MagicMock()
        mock_client.test_method.return_value = {"result": "success"}
        mock_get_client.return_value = mock_client

        # Create the command with arguments
        @self.base_command.create_command_with_error_handling(
            "test_cmd",
            "test_method",
            "Test command with error handling",
            click.argument("arg1"),
            click.argument("arg2"),
        )
        def test_func(arg1, arg2):
            pass

        # Test command execution using invoke
        from click.testing import CliRunner

        runner = CliRunner()

        runner.invoke(test_func, ["value1", "value2"], obj={"timeout": 20, "format": "table"})

        # Verify calls
        mock_get_client.assert_called_once_with("test_api", timeout=20)
        mock_client.test_method.assert_called_once_with(arg1="value1", arg2="value2")
        mock_print_output.assert_called_once()
        mock_print_error.assert_not_called()

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_error")
    def test_create_command_with_error_handling_failure(self, mock_print_error, mock_get_client):
        """Test create_command_with_error_handling for error cases."""
        # Create mock client that raises an exception
        mock_client = MagicMock()
        mock_client.test_method.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client

        # Create the command
        @self.base_command.create_command_with_error_handling("test_cmd", "test_method", "Test command", click.argument("arg1"))
        def test_func(arg1):
            pass

        # Test command execution using invoke
        from click.testing import CliRunner

        runner = CliRunner()

        runner.invoke(test_func, ["value1"], obj={"timeout": 20})

        # Verify error handling
        mock_print_error.assert_called_once_with("API Error", console=self.base_command.console)

    @patch("ecosystems_cli.cli._call_operation")
    def test_call_operation(self, mock_call_operation):
        """Test call_operation command creation."""
        # Create the command
        call_cmd = self.base_command.call_operation()

        # Test that it's a Click command
        assert isinstance(call_cmd, click.Command)
        assert call_cmd.name == "call"
        assert len(call_cmd.params) == 4  # operation + 3 options

        # Test command execution using invoke
        from click.testing import CliRunner

        runner = CliRunner()
        runner.invoke(
            call_cmd,
            [
                "test_operation",
                "--path-params",
                '{"key": "value"}',
                "--query-params",
                '{"query": "param"}',
                "--body",
                '{"body": "data"}',
            ],
            obj={},
        )

        # Verify call
        assert mock_call_operation.called
        args = mock_call_operation.call_args[0]
        assert args[0] == "test_api"
        assert args[1] == "test_operation"
        assert args[2] == '{"key": "value"}'
        assert args[3] == '{"query": "param"}'
        assert args[4] == '{"body": "data"}'
