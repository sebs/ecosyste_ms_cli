"""Tests for the diff commands."""

from unittest import mock

from click.testing import CliRunner


class TestDiffCommands:
    """Test cases for diff commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.diff import DiffCommands

        self.diff_commands = DiffCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_diff_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for diff API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [
            {"operation_id": "createJob", "method": "POST", "path": "/jobs"},
            {"operation_id": "getJob", "method": "GET", "path": "/jobs/{jobID}"},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.diff_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("diff", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_create_job(self, mock_print_output, mock_get_client):
        """Test creating a diff job."""
        mock_client = mock.MagicMock()
        # Simulate a redirect response
        mock_response = mock.MagicMock()
        mock_response.headers = {"location": "https://diff.ecosyste.ms/api/v1/jobs/123"}
        mock_response.status_code = 301
        mock_client.createJob.return_value = mock_response
        mock_get_client.return_value = mock_client

        url1 = "https://example.com/file1.zip"
        url2 = "https://example.com/file2.zip"
        result = self.runner.invoke(self.diff_commands.group, ["create-job", url1, url2], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("diff", base_url=None, timeout=20)
        mock_client.createJob.assert_called_once_with(url_1=url1, url_2=url2)
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_create_job_error(self, mock_print_error, mock_get_client):
        """Test error handling when creating a job."""
        mock_client = mock.MagicMock()
        mock_client.createJob.side_effect = Exception("Failed to create job")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.diff_commands.group, ["create-job", "url1", "url2"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Failed to create job", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_job(self, mock_print_output, mock_get_client):
        """Test getting a specific job."""
        mock_client = mock.MagicMock()
        mock_client.getJob.return_value = {
            "id": "123",
            "url_1": "https://example.com/file1.zip",
            "url_2": "https://example.com/file2.zip",
            "status": "completed",
            "results": {"files_changed": 10},
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.diff_commands.group, ["get-job", "123"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("diff", base_url=None, timeout=20)
        mock_client.getJob.assert_called_once_with(job_id="123")
        mock_print_output.assert_called_once()
