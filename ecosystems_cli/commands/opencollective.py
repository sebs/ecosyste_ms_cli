"""Commands for the opencollective API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class OpenCollectiveCommands(BaseCommand):
    """Commands for the opencollective API."""

    def __init__(self):
        super().__init__("opencollective", "Commands for the opencollective API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the opencollective API."""
        # Register list operations command
        self.list_operations()

        # Projects commands
        self.create_simple_command("projects", "call", "Get all projects.", operation_id="getProjects")

        @self.create_command_with_operation(
            "project", "getProject", "Get a specific project by ID.", click.argument("id", type=int)
        )
        def get_project(id: int):
            pass

        @self.create_command_with_operation("lookup-project", "lookupProject", "Lookup project by URL.", click.argument("url"))
        def lookup_project(url: str):
            pass

        self.create_simple_command(
            "projects-packages", "call", "Get projects with packages.", operation_id="getProjectPackages"
        )

        # Collectives commands
        self.create_simple_command("collectives", "call", "Get all collectives.", operation_id="getCollectives")

        @self.create_command_with_operation(
            "collective", "getCollective", "Get a specific collective by ID.", click.argument("id", type=int)
        )
        def get_collective(id: int):
            pass

        @self.create_command_with_operation(
            "collective-projects",
            "getCollectiveProjects",
            "Get projects for a collective by slug.",
            click.argument("slug"),
        )
        def get_collective_projects(slug: str):
            pass  # Create the command group


opencollective_base = OpenCollectiveCommands()

# Export the properly named group
opencollective = opencollective_base.group
opencollective.name = "opencollective"
