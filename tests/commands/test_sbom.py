"""Tests for the SBOM commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestSbomCommands:
    """Test cases for SBOM commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.sbom import SbomCommands

        self.sbom_commands = SbomCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_sbom_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for SBOM API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "createJob", "method": "POST", "path": "/jobs"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.sbom_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("sbom", timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_create_job(self, mock_print_output, mock_get_client):
        """Test creating a new SBOM parsing job."""
        mock_client = mock.MagicMock()
        mock_client.createJob.return_value = {"id": "12345", "status": "pending"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.sbom_commands.group,
            ["submit-job", "--url", "https://example.com/package.json"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("sbom", timeout=20)
        mock_client.createJob.assert_called_once_with(url="https://example.com/package.json")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_job(self, mock_print_output, mock_get_client):
        """Test getting a specific job by ID."""
        mock_client = mock.MagicMock()
        mock_client.getJob.return_value = {
            "id": "12345",
            "status": "completed",
            "url": "https://example.com/package.json",
            "results": {"dependencies": 10},
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.sbom_commands.group, ["get-job", "12345"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("sbom", timeout=20)
        mock_client.getJob.assert_called_once_with(job_id="12345")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_job_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a job."""
        mock_client = mock.MagicMock()
        mock_client.getJob.side_effect = Exception("Job not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.sbom_commands.group, ["get-job", "nonexistent"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Job not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_sbom_operation(self, mock_call_operation):
        """Test calling a generic operation on SBOM API."""
        result = self.runner.invoke(
            self.sbom_commands.group,
            [
                "call",
                "createJob",
                "--query-params",
                json.dumps({"url": "https://example.com/package.json"}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "sbom"
        assert args[1] == "createJob"
        assert args[3] == json.dumps({"url": "https://example.com/package.json"})
