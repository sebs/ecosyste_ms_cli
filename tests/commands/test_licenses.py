"""Tests for the licenses commands."""

from unittest import mock

from click.testing import CliRunner


class TestLicensesCommands:
    """Test cases for licenses commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.licenses import LicensesCommands

        self.licenses_commands = LicensesCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_licenses_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for licenses API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "createJob", "method": "POST", "path": "/jobs"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.licenses_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("licenses", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_submit_command(self, mock_print_output, mock_get_client):
        """Test submitting a license parsing job."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"id": "job123", "status": "pending"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.licenses_commands.group,
            ["submit", "https://example.com/LICENSE"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("licenses", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "createJob", path_params={}, query_params={"url": "https://example.com/LICENSE"}
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_status_command(self, mock_print_output, mock_get_client):
        """Test getting job status."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "id": "job123",
            "status": "completed",
            "results": {"license": "MIT"},
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.licenses_commands.group,
            ["status", "job123"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("licenses", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with("getJob", path_params={"jobID": "job123"}, query_params={})
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_command(self, mock_call_operation):
        """Test generic call command."""
        result = self.runner.invoke(
            self.licenses_commands.group,
            ["call", "createJob", "--query-params", '{"url": "https://example.com/LICENSE"}'],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "licenses"
        assert args[1] == "createJob"
        assert args[3] == '{"url": "https://example.com/LICENSE"}'
