"""Tests for the packages commands."""

import json
from unittest import mock

import pytest
from click.testing import CliRunner

from ecosystems_cli.commands.packages import (
    call_packages_operation,
    get_package,
    get_package_version,
    get_registries,
    get_registry,
    list_packages_operations,
    packages,
)


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def mock_client():
    """Create a mock API client for packages API."""
    with mock.patch("ecosystems_cli.commands.packages.get_client") as mock_get_client:
        client_instance = mock.MagicMock()
        mock_get_client.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_print_operations():
    """Mock the print_operations function."""
    with mock.patch("ecosystems_cli.commands.packages.print_operations") as mock_print:
        yield mock_print


@pytest.fixture
def mock_print_output():
    """Mock the print_output function."""
    with mock.patch("ecosystems_cli.commands.packages.print_output") as mock_print:
        yield mock_print


@pytest.fixture
def mock_print_error():
    """Mock the print_error function."""
    with mock.patch("ecosystems_cli.commands.packages.print_error") as mock_print:
        yield mock_print


@pytest.fixture
def ctx():
    """Create a mock context object."""
    context = mock.MagicMock()
    context.obj = {"timeout": 30, "format": "table"}
    return context


class TestPackagesGroup:
    """Test the packages group command."""

    def test_packages_group(self, runner):
        """Test that the packages group is properly defined."""
        result = runner.invoke(packages, ["--help"])
        assert result.exit_code == 0
        assert "Commands for the packages API" in result.output


class TestListPackagesOperations:
    """Test the list packages operations command."""

    def test_list_operations_success(self, runner, ctx, mock_client, mock_print_operations):
        """Test successful listing of operations."""
        # Arrange
        operations = [
            {"id": "get_registries", "method": "GET", "path": "/registries"},
            {"id": "get_package", "method": "GET", "path": "/registries/{registry}/packages/{package}"},
        ]
        mock_client.list_operations.return_value = operations

        # Act
        result = runner.invoke(list_packages_operations, obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once_with(operations, console=mock.ANY)

    def test_list_operations_with_custom_timeout(self, runner, mock_client, mock_print_operations):
        """Test listing operations with custom timeout."""
        # Arrange
        ctx_with_timeout = mock.MagicMock()
        ctx_with_timeout.obj = {"timeout": 60}

        # Act
        with mock.patch("ecosystems_cli.commands.packages.get_client") as mock_get_client:
            mock_get_client.return_value = mock_client
            result = runner.invoke(list_packages_operations, obj=ctx_with_timeout.obj)

        # Assert
        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", timeout=60)


class TestGetRegistries:
    """Test the get registries command."""

    def test_get_registries_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of registries."""
        # Arrange
        registries = [
            {"name": "npm", "url": "https://registry.npmjs.org"},
            {"name": "pypi", "url": "https://pypi.org"},
        ]
        mock_client.get_registries.return_value = registries

        # Act
        result = runner.invoke(get_registries, obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_registries.assert_called_once()
        mock_print_output.assert_called_once_with(registries, "table", console=mock.ANY)

    def test_get_registries_with_json_format(self, runner, mock_client, mock_print_output):
        """Test getting registries with JSON output format."""
        # Arrange
        ctx_json = mock.MagicMock()
        ctx_json.obj = {"timeout": 20, "format": "json"}
        registries = [{"name": "npm"}]
        mock_client.get_registries.return_value = registries

        # Act
        result = runner.invoke(get_registries, obj=ctx_json.obj)

        # Assert
        assert result.exit_code == 0
        mock_print_output.assert_called_once_with(registries, "json", console=mock.ANY)


class TestGetRegistry:
    """Test the get registry command."""

    def test_get_registry_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of a specific registry."""
        # Arrange
        registry = {"name": "npm", "url": "https://registry.npmjs.org", "packages_count": 1000000}
        mock_client.get_registry.return_value = registry

        # Act
        result = runner.invoke(get_registry, ["npm"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_registry.assert_called_once_with("npm")
        mock_print_output.assert_called_once_with(registry, "table", console=mock.ANY)

    def test_get_registry_not_found(self, runner, ctx, mock_client, mock_print_error):
        """Test handling of registry not found error."""
        # Arrange
        mock_client.get_registry.side_effect = Exception("Registry not found")

        # Act
        result = runner.invoke(get_registry, ["nonexistent"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0  # Click doesn't set exit code for handled exceptions
        mock_client.get_registry.assert_called_once_with("nonexistent")
        mock_print_error.assert_called_once_with("Registry not found", console=mock.ANY)


class TestGetPackage:
    """Test the get package command."""

    def test_get_package_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of a package."""
        # Arrange
        package = {
            "name": "express",
            "registry": "npm",
            "description": "Fast web framework",
            "latest_version": "4.18.2",
        }
        mock_client.get_package.return_value = package

        # Act
        result = runner.invoke(get_package, ["npm", "express"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_package.assert_called_once_with("npm", "express")
        mock_print_output.assert_called_once_with(package, "table", console=mock.ANY)

    def test_get_package_with_special_characters(self, runner, ctx, mock_client, mock_print_output):
        """Test getting a package with special characters in name."""
        # Arrange
        package = {"name": "@angular/core", "registry": "npm"}
        mock_client.get_package.return_value = package

        # Act
        result = runner.invoke(get_package, ["npm", "@angular/core"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_package.assert_called_once_with("npm", "@angular/core")

    def test_get_package_error(self, runner, ctx, mock_client, mock_print_error):
        """Test handling of package retrieval error."""
        # Arrange
        mock_client.get_package.side_effect = Exception("Package not found")

        # Act
        result = runner.invoke(get_package, ["npm", "nonexistent"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Package not found", console=mock.ANY)


class TestGetPackageVersion:
    """Test the get package version command."""

    def test_get_package_version_success(self, runner, ctx, mock_client, mock_print_output):
        """Test successful retrieval of a package version."""
        # Arrange
        version_info = {
            "name": "express",
            "version": "4.18.2",
            "published_at": "2022-10-08T00:00:00Z",
            "dependencies": {"accepts": "~1.3.8", "array-flatten": "1.1.1"},
        }
        mock_client.get_package_version.return_value = version_info

        # Act
        result = runner.invoke(get_package_version, ["npm", "express", "4.18.2"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_package_version.assert_called_once_with("npm", "express", "4.18.2")
        mock_print_output.assert_called_once_with(version_info, "table", console=mock.ANY)

    def test_get_package_version_with_prerelease(self, runner, ctx, mock_client, mock_print_output):
        """Test getting a prerelease version."""
        # Arrange
        version_info = {"name": "vue", "version": "3.0.0-beta.1"}
        mock_client.get_package_version.return_value = version_info

        # Act
        result = runner.invoke(get_package_version, ["npm", "vue", "3.0.0-beta.1"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_client.get_package_version.assert_called_once_with("npm", "vue", "3.0.0-beta.1")

    def test_get_package_version_error(self, runner, ctx, mock_client, mock_print_error):
        """Test handling of version retrieval error."""
        # Arrange
        mock_client.get_package_version.side_effect = Exception("Version not found")

        # Act
        result = runner.invoke(get_package_version, ["npm", "express", "99.99.99"], obj=ctx.obj)

        # Assert
        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Version not found", console=mock.ANY)


class TestCallPackagesOperation:
    """Test the call packages operation command."""

    def test_call_operation_success(self, runner, ctx):
        """Test successful operation call."""
        # Arrange
        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_packages_operation,
                ["get_registries"],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with("packages", "get_registries", None, None, None, mock.ANY)

    def test_call_operation_with_path_params(self, runner, ctx):
        """Test operation call with path parameters."""
        # Arrange
        path_params = {"registry": "npm", "package": "express"}
        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_packages_operation,
                ["get_package", "--path-params", json.dumps(path_params)],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with(
                "packages",
                "get_package",
                json.dumps(path_params),
                None,
                None,
                mock.ANY,
            )

    def test_call_operation_with_query_params(self, runner, ctx):
        """Test operation call with query parameters."""
        # Arrange
        query_params = {"limit": 10, "offset": 0}
        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_packages_operation,
                ["search_packages", "--query-params", json.dumps(query_params)],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with(
                "packages",
                "search_packages",
                None,
                json.dumps(query_params),
                None,
                mock.ANY,
            )

    def test_call_operation_with_all_params(self, runner, ctx):
        """Test operation call with all parameter types."""
        # Arrange
        path_params = {"registry": "npm"}
        query_params = {"q": "express"}
        body = {"filter": "production"}

        with mock.patch("ecosystems_cli.cli._call_operation") as mock_call:
            # Act
            result = runner.invoke(
                call_packages_operation,
                [
                    "search_registry_packages",
                    "--path-params",
                    json.dumps(path_params),
                    "--query-params",
                    json.dumps(query_params),
                    "--body",
                    json.dumps(body),
                ],
                obj=ctx.obj,
            )

            # Assert
            assert result.exit_code == 0
            mock_call.assert_called_once_with(
                "packages",
                "search_registry_packages",
                json.dumps(path_params),
                json.dumps(query_params),
                json.dumps(body),
                mock.ANY,
            )
