"""Summary API commands."""

import click

from ecosystems_cli.commands.base import BaseCommand


class SummaryCommands(BaseCommand):
    """Commands for the Summary API."""

    def __init__(self):
        super().__init__("summary", "Commands for the Summary API.")
        self._register_commands()

    def _register_commands(self):
        """Register all summary-specific commands."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("projects", "call", "Get all projects.", operation_id="getProjects")
        self.create_simple_command("collections", "call", "Get all collections.", operation_id="getCollections")

        # Get specific project command
        @self.create_command_with_operation("project", "getProject", "Get a specific project by ID.", click.argument("id"))
        def get_project(id: str):
            pass

        # Lookup project command
        @self.create_command_with_operation("lookup", "lookupProject", "Lookup project by URL.", click.argument("url"))
        def lookup_project(url: str):
            pass

        # Get specific collection command
        @self.create_command_with_operation(
            "collection", "getCollection", "Get a specific collection by ID.", click.argument("id")
        )
        def get_collection(id: str):
            pass

        # Get collection projects command
        @self.create_command_with_operation(
            "collection-projects", "getCollectionProjects", "Get projects in a collection.", click.argument("id")
        )
        def get_collection_projects(id: str):
            pass  # Create the command group


summary_base = SummaryCommands()

# Export the properly named group
summary = summary_base.group
summary.name = "summary"
