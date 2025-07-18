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
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_advisories_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for advisories API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [
            {"operation_id": "get_advisory", "method": "GET", "path": "/advisories/{id}"}
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.advisories_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("advisories", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_advisories_packages(self, mock_print_output, mock_get_client):
        """Test getting packages that have advisories."""
        mock_client = mock.MagicMock()
        mock_client.get_advisories_packages.return_value = [
            {"ecosystem": "npm", "package_name": "lodash"},
            {"ecosystem": "pypi", "package_name": "django"},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.advisories_commands.group, ["packages"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("advisories", base_url=None, timeout=20)
        mock_client.get_advisories_packages.assert_called_once()
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_search_advisories(self, mock_print_output, mock_get_client):
        """Test searching advisories with filters."""
        mock_client = mock.MagicMock()
        mock_client.get_advisories.return_value = [{"uuid": "123", "title": "Test Advisory", "severity": "high"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.advisories_commands.group,
            ["search", "--ecosystem", "npm", "--severity", "high", "--page", "1", "--per-page", "10"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("advisories", base_url=None, timeout=20)
        mock_client.get_advisories.assert_called_once_with(
            ecosystem="npm",
            severity="high",
            page=1,
            per_page=10,
            package_name=None,
            repository_url=None,
            created_after=None,
            updated_after=None,
            sort=None,
            order=None,
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_advisory(self, mock_print_output, mock_get_client):
        """Test getting a specific advisory by UUID."""
        mock_client = mock.MagicMock()
        mock_client.get_advisory.return_value = {
            "uuid": "test-uuid-123",
            "title": "Security Advisory",
            "severity": "critical",
            "cvss_score": 9.8,
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.advisories_commands.group, ["get", "test-uuid-123"], obj={"timeout": 20, "format": "json"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("advisories", base_url=None, timeout=20)
        mock_client.get_advisory.assert_called_once_with(advisory_uuid="test-uuid-123")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_advisory_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting an advisory."""
        mock_client = mock.MagicMock()
        mock_client.get_advisory.side_effect = Exception("Advisory not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.advisories_commands.group, ["get", "nonexistent-uuid"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Advisory not found", console=mock.ANY)
