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

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_lookup_package(self, mock_print_output, mock_api_factory):
        """Test looking up a package by name and ecosystem."""
        mock_api_factory.call.return_value = [
            {
                "ecosystem": "npm",
                "name": "react",
                "latest_version": "18.2.0",
                "description": "React is a JavaScript library for building user interfaces.",
            }
        ]

        result = self.runner.invoke(
            self.packages_group,
            ["lookup_package", "--ecosystem", "npm", "--name", "react"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "packages",
            "lookupPackage",
            path_params={},
            query_params={
                "ecosystem": "npm",
                "name": "react",
            },
            timeout=mock.ANY,
            mailto=mock.ANY,
            base_url=mock.ANY,
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_lookup_package_by_purl(self, mock_print_output, mock_api_factory):
        """Test looking up a package by purl."""
        mock_api_factory.call.return_value = [
            {
                "ecosystem": "pypi",
                "name": "django",
                "latest_version": "4.2.0",
                "repository_url": "https://github.com/django/django",
            }
        ]

        result = self.runner.invoke(
            self.packages_group,
            ["lookup_package", "--purl", "pkg:pypi/django"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "packages",
            "lookupPackage",
            path_params={},
            query_params={
                "purl": "pkg:pypi/django",
            },
            timeout=mock.ANY,
            mailto=mock.ANY,
            base_url=mock.ANY,
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_keywords(self, mock_print_output, mock_api_factory):
        """Test getting keywords."""
        mock_api_factory.call.return_value = [
            {"name": "javascript", "packages_count": 1000},
            {"name": "react", "packages_count": 500},
        ]

        result = self.runner.invoke(
            self.packages_group,
            ["get_keywords", "--page", "1", "--per-page", "20"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "packages",
            "getKeywords",
            path_params={},
            query_params={
                "page": 1,
                "per_page": 20,
            },
            timeout=mock.ANY,
            mailto=mock.ANY,
            base_url=mock.ANY,
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_keyword(self, mock_print_output, mock_api_factory):
        """Test getting a specific keyword."""
        mock_api_factory.call.return_value = {
            "name": "typescript",
            "packages_count": 300,
            "packages": [
                {"ecosystem": "npm", "name": "@types/node"},
                {"ecosystem": "npm", "name": "@types/react"},
            ],
        }

        result = self.runner.invoke(
            self.packages_group,
            ["get_keyword", "typescript"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "packages",
            "getKeyword",
            path_params={"keywordName": "typescript"},
            query_params={},
            timeout=mock.ANY,
            mailto=mock.ANY,
            base_url=mock.ANY,
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_registries(self, mock_print_output, mock_api_factory):
        """Test getting registries."""
        mock_api_factory.call.return_value = [
            {"name": "npmjs.org", "ecosystem": "npm", "packages_count": 2000000},
            {"name": "pypi.org", "ecosystem": "pypi", "packages_count": 400000},
        ]

        result = self.runner.invoke(
            self.packages_group,
            ["get_registries"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "packages",
            "getRegistries",
            path_params={},
            query_params={},
            timeout=mock.ANY,
            mailto=mock.ANY,
            base_url=mock.ANY,
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_error")
    def test_lookup_package_error(self, mock_print_error, mock_api_factory):
        """Test error handling when looking up a package."""
        mock_api_factory.call.side_effect = Exception("Package not found")

        result = self.runner.invoke(
            self.packages_group,
            ["lookup_package", "--ecosystem", "npm", "--name", "nonexistent"],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Package not found", console=mock.ANY)
