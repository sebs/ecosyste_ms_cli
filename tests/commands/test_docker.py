"""Tests for docker command group."""

from unittest import mock

import click
from click.testing import CliRunner

from ecosystems_cli.commands.docker import DockerCommands


class TestDockerCommands:
    """Test the docker commands."""

    def setup_method(self):
        """Setup test fixtures."""
        self.runner = CliRunner()
        self.docker_commands = DockerCommands()

    def test_docker_group_creation(self):
        """Test that docker group is created correctly."""
        assert self.docker_commands.group.name == "docker" or self.docker_commands.group.name == "group"
        assert isinstance(self.docker_commands.group, click.Group)

    def test_list_operations(self):
        """Test list operations command exists."""
        commands = self.docker_commands.group.commands
        assert "list" in commands

    def test_commands_registered(self):
        """Test that all expected commands are registered."""
        commands = self.docker_commands.group.commands
        assert "packages" in commands
        assert "package" in commands
        assert "versions" in commands
        assert "version" in commands

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_packages(self, mock_print_output, mock_get_client):
        """Test getting all packages."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"name": "nginx", "versions_count": 100}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["packages"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with("getPackages")
        mock_print_output.assert_called_once_with([{"name": "nginx", "versions_count": 100}], "table", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.handlers.factory.OperationHandlerFactory.get_handler")
    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package(self, mock_print_output, mock_get_client, mock_get_handler):
        """Test getting a specific package."""
        # Mock the handler
        mock_handler = mock.MagicMock()
        mock_handler.build_params.return_value = ({"packageName": "nginx"}, {})
        mock_get_handler.return_value = mock_handler

        # Mock the client
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"name": "nginx", "description": "Web server", "versions_count": 100}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["package", "nginx"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("docker", base_url=None, timeout=20)
        mock_handler.build_params.assert_called_once_with("getPackage", (), {"package_name": "nginx"})
        mock_client.call.assert_called_once_with("getPackage", path_params={"packageName": "nginx"}, query_params={})
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.handlers.factory.OperationHandlerFactory.get_handler")
    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_package_error(self, mock_print_error, mock_get_client, mock_get_handler):
        """Test error handling when getting a package."""
        # Mock the handler
        mock_handler = mock.MagicMock()
        mock_handler.build_params.return_value = ({"packageName": "nonexistent"}, {})
        mock_get_handler.return_value = mock_handler

        # Mock the client
        mock_client = mock.MagicMock()
        mock_client.call.side_effect = Exception("Package not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["package", "nonexistent"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Package not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.handlers.factory.OperationHandlerFactory.get_handler")
    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package_versions(self, mock_print_output, mock_get_client, mock_get_handler):
        """Test getting versions for a package."""
        # Mock the handler
        mock_handler = mock.MagicMock()
        mock_handler.build_params.return_value = ({"packageName": "nginx"}, {})
        mock_get_handler.return_value = mock_handler

        # Mock the client
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"version": "1.21.0"}, {"version": "1.20.0"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["versions", "nginx"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with("getPackageVersions", path_params={"packageName": "nginx"}, query_params={})

    @mock.patch("ecosystems_cli.commands.handlers.factory.OperationHandlerFactory.get_handler")
    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_package_version(self, mock_print_output, mock_get_client, mock_get_handler):
        """Test getting a specific version of a package."""
        # Mock the handler
        mock_handler = mock.MagicMock()
        mock_handler.build_params.return_value = ({"packageName": "nginx", "versionNumber": "1.21.0"}, {})
        mock_get_handler.return_value = mock_handler

        # Mock the client
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"name": "nginx", "version": "1.21.0", "published_at": "2021-05-25"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["version", "nginx", "1.21.0"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with(
            "getPackageVersion", path_params={"packageName": "nginx", "versionNumber": "1.21.0"}, query_params={}
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_usage(self, mock_print_output, mock_get_client):
        """Test getting usage ecosystems."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"ecosystem": "npm", "count": 50000}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["usage"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with("usage")

    @mock.patch("ecosystems_cli.commands.handlers.factory.OperationHandlerFactory.get_handler")
    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_usage_ecosystem(self, mock_print_output, mock_get_client, mock_get_handler):
        """Test getting usage for an ecosystem."""
        # Mock the handler
        mock_handler = mock.MagicMock()
        mock_handler.build_params.return_value = ({"ecosystem": "npm"}, {})
        mock_get_handler.return_value = mock_handler

        # Mock the client
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"name": "express", "dependents_count": 5000}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["usage-ecosystem", "npm"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with("usageEcosystem", path_params={"ecosystem": "npm"}, query_params={})

    @mock.patch("ecosystems_cli.commands.handlers.factory.OperationHandlerFactory.get_handler")
    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_usage_package(self, mock_print_output, mock_get_client, mock_get_handler):
        """Test getting usage for a specific package."""
        # Mock the handler
        mock_handler = mock.MagicMock()
        mock_handler.build_params.return_value = ({"ecosystem": "npm", "package": "express"}, {})
        mock_get_handler.return_value = mock_handler

        # Mock the client
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {"ecosystem": "npm", "name": "express", "dependents_count": 5000}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.docker_commands.group, ["usage-package", "npm", "express"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.call.assert_called_once_with(
            "usagePackage", path_params={"ecosystem": "npm", "package": "express"}, query_params={}
        )
