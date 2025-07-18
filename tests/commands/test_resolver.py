"""Tests for the resolver commands."""

from unittest import mock

from click.testing import CliRunner


class TestResolverCommands:
    """Test cases for resolver commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.resolver import ResolverCommands

        self.resolver_commands = ResolverCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_resolver_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for resolver API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [
            {"operation_id": "createJob", "method": "POST", "path": "/jobs"},
            {"operation_id": "getJob", "method": "GET", "path": "/jobs/{jobID}"},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.resolver_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("resolver", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.api_client.get_client")
    @mock.patch("ecosystems_cli.helpers.print_output.print_output")
    def test_create_job(self, mock_print_output, mock_get_client):
        """Test creating a resolve job."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"id": "job123", "status": "pending"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.resolver_commands.group,
            ["create-job", "numpy", "pypi"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("resolver", timeout=20)
        mock_client.call.assert_called_once_with(
            "createJob",
            path_params={},
            query_params={"package_name": "numpy", "registry": "pypi"},
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.api_client.get_client")
    @mock.patch("ecosystems_cli.helpers.print_output.print_output")
    def test_create_job_with_options(self, mock_print_output, mock_get_client):
        """Test creating a resolve job with optional parameters."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"id": "job456", "status": "pending"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.resolver_commands.group,
            ["create-job", "numpy", "pypi", "--before", "2023-01-01T00:00:00Z", "--version", ">=1.20.0"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("resolver", timeout=20)
        mock_client.call.assert_called_once_with(
            "createJob",
            path_params={},
            query_params={
                "package_name": "numpy",
                "registry": "pypi",
                "before": "2023-01-01T00:00:00Z",
                "version": ">=1.20.0",
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.api_client.get_client")
    @mock.patch("ecosystems_cli.helpers.print_output.print_output")
    def test_get_job(self, mock_print_output, mock_get_client):
        """Test getting a job by ID."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "id": "job123",
            "package_name": "numpy",
            "registry": "pypi",
            "status": "completed",
            "results": {"dependencies": ["scipy", "matplotlib"]},
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.resolver_commands.group,
            ["get-job", "job123"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("resolver", timeout=20)
        mock_client.call.assert_called_once_with("getJob", path_params={"jobID": "job123"}, query_params={})
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.api_client.get_client")
    @mock.patch("ecosystems_cli.helpers.print_error.print_error")
    def test_get_job_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a job."""
        mock_client = mock.MagicMock()
        mock_client.call.side_effect = Exception("Job not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.resolver_commands.group,
            ["get-job", "nonexistent"],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Job not found", console=mock.ANY)
