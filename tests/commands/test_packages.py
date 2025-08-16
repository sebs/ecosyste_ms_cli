"""Tests for the packages commands."""

from unittest import mock

from click.testing import CliRunner


class TestPackagesCommands:
    """Test cases for packages commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the packages group to ensure commands are registered
        from ecosystems_cli.commands.packages import packages

        self.packages_group = packages

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_lookup_package(self, mock_print_output, mock_get_client):
        """Test looking up a package by name and ecosystem."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {
                "ecosystem": "npm",
                "name": "react",
                "latest_version": "18.2.0",
                "description": "React is a JavaScript library for building user interfaces.",
            }
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.packages_group,
            ["lookup_package", "--ecosystem", "npm", "--name", "react"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "lookupPackage",
            path_params={},
            query_params={
                "ecosystem": "npm",
                "name": "react",
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_lookup_package_by_purl(self, mock_print_output, mock_get_client):
        """Test looking up a package by purl."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {
                "ecosystem": "pypi",
                "name": "django",
                "latest_version": "4.2.0",
                "repository_url": "https://github.com/django/django",
            }
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.packages_group,
            ["lookup_package", "--purl", "pkg:pypi/django"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "lookupPackage",
            path_params={},
            query_params={
                "purl": "pkg:pypi/django",
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_keywords(self, mock_print_output, mock_get_client):
        """Test getting keywords."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {"name": "javascript", "packages_count": 1000},
            {"name": "react", "packages_count": 500},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.packages_group,
            ["get_keywords", "--page", "1", "--per-page", "20"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "getKeywords",
            path_params={},
            query_params={
                "page": 1,
                "per_page": 20,
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_keyword(self, mock_print_output, mock_get_client):
        """Test getting a specific keyword."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "name": "typescript",
            "packages_count": 300,
            "packages": [
                {"ecosystem": "npm", "name": "@types/node"},
                {"ecosystem": "npm", "name": "@types/react"},
            ],
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.packages_group,
            ["get_keyword", "typescript"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "getKeyword",
            path_params={"keywordName": "typescript"},
            query_params={},
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_registries(self, mock_print_output, mock_get_client):
        """Test getting registries."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {"name": "npmjs.org", "ecosystem": "npm", "packages_count": 2000000},
            {"name": "pypi.org", "ecosystem": "pypi", "packages_count": 400000},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.packages_group,
            ["get_registries"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("packages", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "getRegistries",
            path_params={},
            query_params={},
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_error")
    def test_lookup_package_error(self, mock_print_error, mock_get_client):
        """Test error handling when looking up a package."""
        mock_client = mock.MagicMock()
        mock_client.call.side_effect = Exception("Package not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.packages_group,
            ["lookup_package", "--ecosystem", "npm", "--name", "nonexistent"],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Package not found", console=mock.ANY)
