"""Tests for the packages commands."""

from unittest import mock

from click.testing import CliRunner


class TestPackagesCommands:
    """Test cases for packages commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.packages import PackagesCommands

        self.packages_commands = PackagesCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_packages_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for packages API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "get_package", "method": "GET", "path": "/packages/{id}"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.packages_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_registries(self, mock_print_output, mock_get_client):
        """Test getting all registries."""
        mock_client = mock.MagicMock()
        mock_client.get_registries.return_value = {"registries": ["npm", "pypi"]}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.packages_commands.group, ["registries"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.get_registries.assert_called_once()
        mock_print_output.assert_called_once_with({"registries": ["npm", "pypi"]}, "table", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_registry(self, mock_print_output, mock_get_client):
        """Test getting a specific registry."""
        mock_client = mock.MagicMock()
        mock_client.get_registry.return_value = {"name": "npm", "packages": 1000000}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.packages_commands.group, ["registry", "npm"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.get_registry.assert_called_once_with(name="npm")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_registry_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a registry."""
        mock_client = mock.MagicMock()
        mock_client.get_registry.side_effect = Exception("Registry not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.packages_commands.group, ["registry", "nonexistent"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Registry not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package(self, mock_print_output, mock_get_client):
        """Test getting a specific package."""
        mock_client = mock.MagicMock()
        mock_client.get_package.return_value = {"name": "react", "registry": "npm", "version": "18.0.0"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.packages_commands.group, ["package", "npm", "react"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.get_package.assert_called_once_with(registry="npm", package="react")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package_version(self, mock_print_output, mock_get_client):
        """Test getting a specific package version."""
        mock_client = mock.MagicMock()
        mock_client.get_package_version.return_value = {"name": "react", "version": "18.0.0", "published": "2022-03-29"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.packages_commands.group, ["version", "npm", "react", "18.0.0"], obj={"timeout": 20, "format": "jsonl"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.get_package_version.assert_called_once_with(registry="npm", package="react", version="18.0.0")
