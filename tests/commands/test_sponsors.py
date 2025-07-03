"""Tests for the sponsors commands."""

import json
from unittest import mock

from click.testing import CliRunner


class TestSponsorsCommands:
    """Test cases for sponsors commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.sponsors import SponsorsCommands

        self.sponsors_commands = SponsorsCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_sponsors_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for sponsors API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [
            {"operation_id": "get_account", "method": "GET", "path": "/accounts/{login}"}
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.sponsors_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("sponsors", timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_list_accounts(self, mock_print_output, mock_get_client):
        """Test listing all maintainer accounts."""
        mock_client = mock.MagicMock()
        mock_client.list_accounts.return_value = [
            {"id": 1, "login": "user1", "has_sponsors_listing": True},
            {"id": 2, "login": "user2", "has_sponsors_listing": False},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.sponsors_commands.group, ["accounts"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("sponsors", timeout=20)
        mock_client.list_accounts.assert_called_once()
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_list_sponsors(self, mock_print_output, mock_get_client):
        """Test listing all sponsors."""
        mock_client = mock.MagicMock()
        mock_client.list_sponsors.return_value = [
            {"id": 1, "login": "sponsor1", "sponsors_count": 10},
            {"id": 2, "login": "sponsor2", "sponsors_count": 5},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.sponsors_commands.group, ["sponsors"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("sponsors", timeout=20)
        mock_client.list_sponsors.assert_called_once()
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_account(self, mock_print_output, mock_get_client):
        """Test getting a specific account."""
        mock_client = mock.MagicMock()
        mock_client.get_account.return_value = {
            "id": 1,
            "login": "testuser",
            "has_sponsors_listing": True,
            "sponsors_count": 25,
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.sponsors_commands.group, ["account", "testuser"], obj={"timeout": 20, "format": "table"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("sponsors", timeout=20)
        mock_client.get_account.assert_called_once_with(login="testuser")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_account_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting an account."""
        mock_client = mock.MagicMock()
        mock_client.get_account.side_effect = Exception("Account not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.sponsors_commands.group, ["account", "nonexistent"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Account not found", console=mock.ANY)

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_list_account_sponsors(self, mock_print_output, mock_get_client):
        """Test listing sponsors for an account."""
        mock_client = mock.MagicMock()
        mock_client.list_account_sponsors.return_value = [
            {"id": 1, "status": "active", "funder": {"login": "sponsor1"}},
            {"id": 2, "status": "active", "funder": {"login": "sponsor2"}},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.sponsors_commands.group, ["account-sponsors", "testuser"], obj={"timeout": 20, "format": "tsv"}
        )

        assert result.exit_code == 0
        mock_client.list_account_sponsors.assert_called_once_with(login="testuser")

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_list_account_sponsorships(self, mock_print_output, mock_get_client):
        """Test listing sponsorships for an account."""
        mock_client = mock.MagicMock()
        mock_client.list_account_sponsorships.return_value = [
            {"id": 1, "status": "active", "maintainer": {"login": "maintainer1"}},
            {"id": 2, "status": "inactive", "maintainer": {"login": "maintainer2"}},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.sponsors_commands.group, ["account-sponsorships", "testuser"], obj={"timeout": 20, "format": "jsonl"}
        )

        assert result.exit_code == 0
        mock_client.list_account_sponsorships.assert_called_once_with(login="testuser")

    @mock.patch("ecosystems_cli.cli._call_operation")
    def test_call_sponsors_operation(self, mock_call_operation):
        """Test calling a generic operation on sponsors API."""
        result = self.runner.invoke(
            self.sponsors_commands.group,
            [
                "call",
                "getAccount",
                "--path-params",
                json.dumps({"login": "testuser"}),
                "--query-params",
                json.dumps({"include": "sponsors"}),
            ],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "sponsors"
        assert args[1] == "getAccount"
        assert args[2] == json.dumps({"login": "testuser"})
        assert args[3] == json.dumps({"include": "sponsors"})
