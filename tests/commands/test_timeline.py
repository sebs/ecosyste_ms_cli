"""Tests for the timeline commands."""

from unittest import mock

from click.testing import CliRunner


class TestTimelineCommands:
    """Test cases for timeline commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the timeline group to ensure commands are registered
        from ecosystems_cli.commands.timeline import timeline

        self.timeline_group = timeline

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_events(self, mock_print_output, mock_api_factory):
        """Test getting all events."""
        mock_api_factory.call.return_value = [
            {"actor": "user1", "event_type": "push", "repository": "repo1"},
            {"actor": "user2", "event_type": "pull_request", "repository": "repo2"},
        ]

        result = self.runner.invoke(
            self.timeline_group,
            ["get_events", "--page", "1", "--per-page", "10"],
            obj={"timeout": 20, "format": "table", "domain": None},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "timeline",
            "getEvents",
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

    @mock.patch("ecosystems_cli.commands.execution.api_factory")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_get_event_for_repository(self, mock_print_output, mock_api_factory):
        """Test getting events for a specific repository."""
        mock_api_factory.call.return_value = {
            "actor": "user1",
            "event_type": "push",
            "repository": "ecosyste-ms/timeline",
            "payload": {},
        }

        result = self.runner.invoke(
            self.timeline_group,
            ["get_event", "ecosyste-ms/timeline", "--page", "1"],
            obj={"timeout": 20, "format": "json", "domain": None},
        )

        assert result.exit_code == 0
        mock_api_factory.call.assert_called_once_with(
            "timeline",
            "getEvent",
            path_params={"repoName": "ecosyste-ms/timeline"},
            query_params={
                "page": 1,
            },
            timeout=mock.ANY,
            mailto=mock.ANY,
            base_url=mock.ANY,
        )
        mock_print_output.assert_called_once()

    def test_timeline_name_attribute(self):
        """Test that timeline command has the correct name attribute."""
        from ecosystems_cli.commands.timeline import timeline

        assert hasattr(timeline, "name")
        assert timeline.name == "timeline"

    def test_timeline_help(self):
        """Test that timeline help text is correct."""
        result = self.runner.invoke(self.timeline_group, ["--help"])
        assert result.exit_code == 0
        assert "Commands for the timeline API" in result.output
