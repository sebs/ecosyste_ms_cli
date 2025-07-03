"""Commands for the OST (Open Sustainable Technology) API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class OSTCommands(BaseCommand):
    """Commands for the OST API."""

    def __init__(self):
        super().__init__("ost", "Commands for the OST (Open Sustainable Technology) API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the OST API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("projects", "get_projects", "Get all projects.")
        self.create_simple_command("projects-with-packages", "get_project_packages", "Get projects with packages.")
        self.create_simple_command("projects-with-images", "get_project_images", "Get projects with images.")
        self.create_simple_command("issues", "get_issues", "Get all issues.")
        self.create_simple_command(
            "openclimateaction-issues", "get_open_climate_action_issues", "Get issues for OpenClimateAction."
        )

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "project", "get_project", "Get a specific project by ID.", click.argument("id", type=int)
        )
        def get_project(id: int):
            pass

        @self.create_command_with_error_handling(
            "lookup-project",
            "lookup_project",
            "Lookup project by URL.",
            click.argument("url"),
        )
        def lookup_project(url: str):
            pass

        # Register call operation command
        self.call_operation()


# Create the command group
ost_base = OSTCommands()

# Export the properly named group
ost = ost_base.group
ost.name = "ost"
