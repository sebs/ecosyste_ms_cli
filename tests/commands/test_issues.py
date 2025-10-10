"""Tests for the issues commands."""

from unittest import mock

from click.testing import CliRunner


class TestIssuesCommands:
    """Test cases for issues commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the issues group to ensure commands are registered
        from ecosystems_cli.commands.issues import issues

        self.issues_group = issues

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_repositories_lookup(self, mock_print_output, mock_api_factory):
        """Test repository lookup."""
        mock_api_factory.call.return_value = {
            "full_name": "octocat/hello-world",
            "html_url": "https://github.com/octocat/hello-world",
            "open_issues_count": 42,
        }

        result = self.runner.invoke(
            self.issues_group,
            ["repositories_lookup", "--url", "https://github.com/octocat/hello-world"],
            obj={"timeout": 20, "format": "table", "domain": None},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "issues",
            "repositoriesLookup",
            path_params={},
            query_params={
                "url": "https://github.com/octocat/hello-world",
            },
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
            {"name": "github", "url": "https://github.com"},
            {"name": "gitlab", "url": "https://gitlab.com"},
        ]

        result = self.runner.invoke(
            self.issues_group,
            ["get_registries", "--page", "1", "--per-page", "10"],
            obj={"timeout": 20, "format": "table", "domain": None},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "issues",
            "getRegistries",
            path_params={},
            query_params={
                "page": 1,
                "per_page": 10,
            },
            timeout=mock.ANY,
            mailto=mock.ANY,
            base_url=mock.ANY,
        )
        mock_print_output.assert_called_once()
