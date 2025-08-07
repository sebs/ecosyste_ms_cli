"""Tests for the advisories commands."""

from unittest import mock

from click.testing import CliRunner


class TestAdvisoriesCommands:
    """Test cases for advisories commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.advisories import AdvisoriesCommands

        self.advisories_commands = AdvisoriesCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_advisories_packages(self, mock_print_output, mock_get_client):
        """Test getting packages that have advisories."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {"ecosystem": "npm", "package_name": "lodash"},
            {"ecosystem": "pypi", "package_name": "django"},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.advisories_commands.group, ["get_advisories_packages"], obj={"timeout": 20, "format": "table"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("advisories", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with("getAdvisoriesPackages", path_params={}, query_params={})
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_advisories(self, mock_print_output, mock_get_client):
        """Test searching advisories with filters."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [{"uuid": "123", "title": "Test Advisory", "severity": "high"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.advisories_commands.group,
            ["get_advisories", "--ecosystem", "npm", "--severity", "high", "--page", "1", "--per-page", "10"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("advisories", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "getAdvisories",
            path_params={},
            query_params={
                "ecosystem": "npm",
                "severity": "high",
                "page": 1,
                "per_page": 10,
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_advisory(self, mock_print_output, mock_get_client):
        """Test getting a specific advisory by UUID."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "uuid": "test-uuid-123",
            "title": "Security Advisory",
            "severity": "critical",
            "cvss_score": 9.8,
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.advisories_commands.group, ["get_advisory", "test-uuid-123"], obj={"timeout": 20, "format": "json"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("advisories", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "getAdvisory",
            path_params={"advisoryUUID": "test-uuid-123"},
            query_params={},
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_advisory_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting an advisory."""
        mock_client = mock.MagicMock()
        mock_client.call.side_effect = Exception("Advisory not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.advisories_commands.group, ["get_advisory", "nonexistent-uuid"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Advisory not found", console=mock.ANY)
