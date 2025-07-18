"""Integration tests for CLI domain configuration."""

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ecosystems_cli.cli import main


class TestCLIDomainConfiguration:
    """Test domain configuration in CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("ecosystems_cli.api_client.requests.request")
    def test_domain_parameter_in_main_command(self, mock_request):
        """Test --domain parameter at main command level."""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"topics": []}

        self.runner.invoke(main, ["--domain", "custom.api.com", "repos", "topics"])

        # Check that the custom domain was used in the URL
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["url"] == "https://custom.api.com/api/v1/topics"

    @patch("ecosystems_cli.api_client.requests.request")
    def test_domain_parameter_in_subcommand(self, mock_request):
        """Test --domain parameter at subcommand level."""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"topics": []}

        self.runner.invoke(main, ["repos", "--domain", "sub.api.com", "topics"])

        # Check that the custom domain was used in the URL
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["url"] == "https://sub.api.com/api/v1/topics"

    @patch("ecosystems_cli.api_client.requests.request")
    def test_domain_env_var_general(self, mock_request, monkeypatch):
        """Test general ECOSYSTEMS_DOMAIN environment variable."""
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "env.api.com")

        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"topics": []}

        self.runner.invoke(main, ["repos", "topics"])

        # Check that the env domain was used
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["url"] == "https://env.api.com/api/v1/topics"

    @patch("ecosystems_cli.api_client.requests.request")
    def test_domain_env_var_api_specific(self, mock_request, monkeypatch):
        """Test API-specific environment variable."""
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "general.api.com")
        monkeypatch.setenv("ECOSYSTEMS_REPOS_DOMAIN", "repos.api.com")

        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"topics": []}

        self.runner.invoke(main, ["repos", "topics"])

        # Check that the API-specific env domain was used
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["url"] == "https://repos.api.com/api/v1/topics"

    @patch("ecosystems_cli.api_client.requests.request")
    def test_domain_precedence_env_over_param(self, mock_request, monkeypatch):
        """Test that env var takes precedence over --domain parameter."""
        monkeypatch.setenv("ECOSYSTEMS_REPOS_DOMAIN", "env.api.com")

        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"topics": []}

        self.runner.invoke(main, ["repos", "--domain", "param.api.com", "topics"])

        # Check that the env domain was used (not the parameter)
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["url"] == "https://env.api.com/api/v1/topics"

    @patch("ecosystems_cli.api_client.requests.request")
    def test_domain_with_protocol(self, mock_request):
        """Test domain with full URL including protocol."""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"topics": []}

        self.runner.invoke(main, ["--domain", "http://localhost:8080", "repos", "topics"])

        # Check that the full URL was preserved
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["url"] == "http://localhost:8080/topics"

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_operations")
    def test_domain_inherited_from_parent_context(self, mock_print_operations, mock_get_client):
        """Test that domain is inherited from parent context."""
        mock_client = MagicMock()
        mock_client.list_operations.return_value = [{"id": "op1", "method": "GET", "path": "/test", "summary": "Test"}]
        mock_get_client.return_value = mock_client

        # Domain set at main level should be inherited by subcommand
        result = self.runner.invoke(main, ["--domain", "parent.api.com", "repos", "list"])

        # Verify the command executed successfully
        assert result.exit_code == 0

        # The list command should use the parent domain
        mock_get_client.assert_called_once_with("repos", base_url="https://parent.api.com/api/v1", timeout=20)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @patch("ecosystems_cli.api_client.requests.request")
    def test_no_domain_uses_default(self, mock_request):
        """Test that default domain is used when none specified."""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"topics": []}

        self.runner.invoke(main, ["repos", "topics"])

        # Check that the default domain was used
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["url"] == "https://repos.ecosyste.ms/api/v1/topics"
