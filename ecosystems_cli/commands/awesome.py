"""Awesome API commands."""

import click

from ecosystems_cli.commands.base import BaseCommand


class AwesomeCommands(BaseCommand):
    """Commands for the Awesome API."""

    def __init__(self):
        super().__init__("awesome", "Commands for the Awesome API.")
        self._register_commands()

    def _register_commands(self):
        """Register all awesome-specific commands."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("projects", "call", "Get all projects.", operation_id="getProjects")
        self.create_simple_command("lists", "call", "Get all lists.", operation_id="getLists")
        self.create_simple_command("topics", "call", "Get all topics.", operation_id="getTopics")

        # Get specific project command
        @self.create_command_with_operation("project", "getProject", "Get a specific project by ID.", click.argument("id"))
        def get_project(id: str):
            pass

        # Get specific list command
        @self.create_command_with_operation("list", "getList", "Get a specific list by ID.", click.argument("id"))
        def get_list(id: str):
            pass

        # Get projects in a list command
        @self.create_command_with_operation(
            "list-projects", "getListProjects", "Get projects in a specific list.", click.argument("id")
        )
        def get_list_projects(id: str):
            pass

        # Get specific topic command
        @self.create_command_with_operation("topic", "getTopic", "Get a specific topic by slug.", click.argument("slug"))
        def get_topic(slug: str):
            pass  # Create the command group


awesome_base = AwesomeCommands()

# Export the properly named group
awesome = awesome_base.group
awesome.name = "awesome"
