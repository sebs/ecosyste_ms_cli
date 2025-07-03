"""Commands for the timeline API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class TimelineCommands(BaseCommand):
    """Commands for the timeline API."""

    def __init__(self):
        super().__init__("timeline", "Commands for the timeline API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the timeline API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("events", "get_events", "List all events.")

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "event", "get_event", "Get events for a specific repository.", click.argument("repo_name")
        )
        def get_event(repo_name: str):
            pass

        # Register call operation command
        self.call_operation()


# Create the command group
timeline_base = TimelineCommands()

# Export the properly named group
timeline = timeline_base.group
timeline.name = "timeline"
