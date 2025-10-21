"""Integration tests for CLI domain configuration."""

from unittest.mock import patch

from click.testing import CliRunner

from ecosystems_cli.cli import main


class TestCLIDomainConfiguration:
    """Test domain configuration in CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("ecosystems_cli.commands.execution.api_factory")
    def test_domain_parameter_in_main_command(self, mock_api_factory):
        """Test --domain parameter at main command level."""
        mock_api_factory.call.return_value = {"advisories": []}

        self.runner.invoke(main, ["--domain", "custom.api.com", "advisories", "get_advisories"])

        # Check that the custom domain was used in the URL
        mock_api_factory.call.assert_called()
        call_args = mock_api_factory.call.call_args
        assert call_args.kwargs["base_url"] == "https://custom.api.com/api/v1"

    @patch("ecosystems_cli.commands.execution.api_factory")
    def test_domain_parameter_in_subcommand(self, mock_api_factory):
        """Test --domain parameter at subcommand level."""
        mock_api_factory.call.return_value = {"advisories": []}

        self.runner.invoke(main, ["advisories", "--domain", "sub.api.com", "get_advisories"])

        # Check that the custom domain was used in the URL
        mock_api_factory.call.assert_called()
        call_args = mock_api_factory.call.call_args
        assert call_args.kwargs["base_url"] == "https://sub.api.com/api/v1"

    @patch("ecosystems_cli.commands.execution.api_factory")
    def test_domain_env_var_general(self, mock_api_factory, monkeypatch):
        """Test general ECOSYSTEMS_DOMAIN environment variable."""
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "env.api.com")

        mock_api_factory.call.return_value = {"advisories": []}

        self.runner.invoke(main, ["advisories", "get_advisories"])

        # Check that the env domain was used in the URL
        mock_api_factory.call.assert_called()
        call_args = mock_api_factory.call.call_args
        assert call_args.kwargs["base_url"] == "https://env.api.com/api/v1"

    @patch("ecosystems_cli.commands.execution.api_factory")
    def test_domain_env_var_api_specific(self, mock_api_factory, monkeypatch):
        """Test API-specific environment variable."""
        monkeypatch.setenv("ECOSYSTEMS_ADVISORIES_DOMAIN", "advisories.api.com")

        mock_api_factory.call.return_value = {"advisories": []}

        self.runner.invoke(main, ["advisories", "get_advisories"])

        # Check that the API-specific env domain was used
        mock_api_factory.call.assert_called()
        call_args = mock_api_factory.call.call_args
        assert call_args.kwargs["base_url"] == "https://advisories.api.com/api/v1"

    @patch("ecosystems_cli.commands.execution.api_factory")
    def test_domain_precedence_param_over_env(self, mock_api_factory, monkeypatch):
        """Test that command parameter takes precedence over env var."""
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "env.api.com")

        mock_api_factory.call.return_value = {"advisories": []}

        self.runner.invoke(main, ["--domain", "param.api.com", "advisories", "get_advisories"])

        # Check that the parameter domain was used (not env)
        mock_api_factory.call.assert_called()
        call_args = mock_api_factory.call.call_args
        assert call_args.kwargs["base_url"] == "https://param.api.com/api/v1"

    @patch("ecosystems_cli.commands.execution.api_factory")
    def test_domain_precedence_api_env_over_general(self, mock_api_factory, monkeypatch):
        """Test that API-specific env var takes precedence over general env var."""
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "general.api.com")
        monkeypatch.setenv("ECOSYSTEMS_ADVISORIES_DOMAIN", "advisories.api.com")

        mock_api_factory.call.return_value = {"advisories": []}

        self.runner.invoke(main, ["advisories", "get_advisories"])

        # Check that the API-specific domain was used
        mock_api_factory.call.assert_called()
        call_args = mock_api_factory.call.call_args
        assert call_args.kwargs["base_url"] == "https://advisories.api.com/api/v1"

    @patch("ecosystems_cli.commands.execution.api_factory")
    def test_domain_inherited_from_parent_context(self, mock_api_factory):
        """Test domain is properly inherited from parent context."""
        mock_api_factory.call.return_value = {"advisories": []}

        # Pass domain at main level
        self.runner.invoke(main, ["--domain", "main.api.com", "advisories", "get_advisories"])

        # Verify api_factory.call was called with the correct base_url
        mock_api_factory.call.assert_called_once()
        call_args = mock_api_factory.call.call_args
        assert call_args.kwargs["base_url"] == "https://main.api.com/api/v1"
