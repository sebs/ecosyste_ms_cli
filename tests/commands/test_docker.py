"""Tests for the docker commands."""

from unittest import mock

from click.testing import CliRunner


class TestDockerCommands:
    """Test cases for docker commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.docker import DockerCommands

        self.docker_commands = DockerCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_docker_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for docker API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [
            {"operation_id": "get_package", "method": "GET", "path": "/packages/{packageName}"}
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_packages(self, mock_print_output, mock_get_client):
        """Test getting all packages."""
        mock_client = mock.MagicMock()
        mock_client.get_packages.return_value = [{"name": "nginx", "versions_count": 100}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["packages"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.get_packages.assert_called_once()
        mock_print_output.assert_called_once_with([{"name": "nginx", "versions_count": 100}], "table", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package(self, mock_print_output, mock_get_client):
        """Test getting a specific package."""
        mock_client = mock.MagicMock()
        mock_client.get_package.return_value = {"name": "nginx", "description": "Web server", "versions_count": 100}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["package", "nginx"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.get_package.assert_called_once_with(package_name="nginx")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_package_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a package."""
        mock_client = mock.MagicMock()
        mock_client.get_package.side_effect = Exception("Package not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["package", "nonexistent"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Package not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package_versions(self, mock_print_output, mock_get_client):
        """Test getting versions for a package."""
        mock_client = mock.MagicMock()
        mock_client.get_package_versions.return_value = [{"number": "latest", "published_at": "2023-01-01"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["versions", "nginx"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.get_package_versions.assert_called_once_with(package_name="nginx")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package_version(self, mock_print_output, mock_get_client):
        """Test getting a specific package version."""
        mock_client = mock.MagicMock()
        mock_client.get_package_version.return_value = {"number": "1.21.0", "published_at": "2021-05-25"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.docker_commands.group, ["version", "nginx", "1.21.0"], obj={"timeout": 20, "format": "jsonl"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.get_package_version.assert_called_once_with(package_name="nginx", version_number="1.21.0")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_usage(self, mock_print_output, mock_get_client):
        """Test getting usage ecosystems."""
        mock_client = mock.MagicMock()
        mock_client.usage.return_value = [{"name": "npm", "packages_count": 1000}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["usage"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.usage.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_usage_ecosystem(self, mock_print_output, mock_get_client):
        """Test getting usage for an ecosystem."""
        mock_client = mock.MagicMock()
        mock_client.usage_ecosystem.return_value = [{"name": "express", "dependents_count": 5000}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["usage-ecosystem", "npm"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.usage_ecosystem.assert_called_once_with(ecosystem="npm")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_usage_package(self, mock_print_output, mock_get_client):
        """Test getting usage for a specific package."""
        mock_client = mock.MagicMock()
        mock_client.usage_package.return_value = {"ecosystem": "npm", "name": "express", "dependents_count": 5000}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["usage-package", "npm", "express"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.usage_package.assert_called_once_with(ecosystem="npm", package="express")
