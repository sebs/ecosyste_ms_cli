"""Tests for the timeline commands."""

from unittest import mock

from click.testing import CliRunner


class TestTimelineCommands:
    """Test cases for timeline commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the commands to ensure they're registered
        from ecosystems_cli.commands.timeline import TimelineCommands

        self.timeline_commands = TimelineCommands()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_operations")
    def test_list_timeline_operations(self, mock_print_operations, mock_get_client):
        """Test listing available operations for timeline API."""
        mock_client = mock.MagicMock()
        mock_client.list_operations.return_value = [{"operation_id": "get_events", "method": "GET", "path": "/events"}]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.timeline_commands.group, ["list"], obj={"timeout": 30})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("timeline", base_url=None, timeout=30)
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_events(self, mock_print_output, mock_get_client):
        """Test getting all events."""
        mock_client = mock.MagicMock()
        mock_client.get_events.return_value = [
            {"actor": "user1", "event_type": "push", "repository": "repo1"},
            {"actor": "user2", "event_type": "pull_request", "repository": "repo2"},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.timeline_commands.group, ["events"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("timeline", base_url=None, timeout=20)
        mock_client.get_events.assert_called_once()
        mock_print_output.assert_called_once_with(
            [
                {"actor": "user1", "event_type": "push", "repository": "repo1"},
                {"actor": "user2", "event_type": "pull_request", "repository": "repo2"},
            ],
            "table",
            console=mock.ANY,
        )

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_output")
    def test_get_event(self, mock_print_output, mock_get_client):
        """Test getting events for a specific repository."""
        mock_client = mock.MagicMock()
        mock_client.get_event.return_value = {"actor": "user1", "event_type": "push", "repository": "owner/repo"}
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.timeline_commands.group, ["event", "owner/repo"], obj={"timeout": 20, "format": "json"}
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("timeline", base_url=None, timeout=20)
        mock_client.get_event.assert_called_once_with(repo_name="owner/repo")
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.base.get_client")
    @mock.patch("ecosystems_cli.commands.base.print_error")
    def test_get_event_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting events for a repository."""
        mock_client = mock.MagicMock()
        mock_client.get_event.side_effect = Exception("Repository not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.timeline_commands.group, ["event", "nonexistent/repo"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Repository not found", console=mock.ANY)
