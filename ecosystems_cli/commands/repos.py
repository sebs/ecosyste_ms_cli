"""Commands for the repos API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class ReposCommands(BaseCommand):
    """Commands for the repos API."""

    def __init__(self):
        super().__init__("repos", "Commands for the repos API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the repos API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("topics", "get_topics", "Get all topics.")
        self.create_simple_command("hosts", "get_hosts", "Get all repository hosts.")

        # Register commands with error handling
        @self.create_command_with_error_handling("topic", "get_topic", "Get a specific topic by name.", click.argument("name"))
        def get_topic(name: str):
            pass

        @self.create_command_with_error_handling(
            "host", "get_host", "Get a specific repository host by name.", click.argument("name")
        )
        def get_host(name: str):
            pass

        @self.create_command_with_error_handling(
            "repository",
            "get_repository",
            "Get a specific repository.",
            click.argument("host"),
            click.argument("owner"),
            click.argument("repo"),
        )
        def get_repository(host: str, owner: str, repo: str):
            pass

        # Register call operation command
        self.call_operation()


# Create the command group
repos_base = ReposCommands()

# Export the properly named group
repos = repos_base.group
repos.name = "repos"
