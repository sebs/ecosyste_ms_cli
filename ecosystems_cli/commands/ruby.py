"""Commands for the ruby API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class RubyCommands(BaseCommand):
    """Commands for the ruby API."""

    def __init__(self):
        super().__init__("ruby", "Commands for the ruby API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the ruby API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("projects", "getProjects", "Get all projects.")
        self.create_simple_command("project-packages", "getProjectPackages", "Get projects with packages.")
        self.create_simple_command("issues", "getIssues", "Get all issues.")

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "project", "getProject", "Get a specific project by ID.", click.argument("project_id", type=int)
        )
        def get_project(project_id: int):
            pass

        @self.create_command_with_error_handling(
            "lookup-project", "lookupProject", "Lookup project by URL.", click.argument("url")
        )
        def lookup_project(url: str):
            pass  # Create the command group


ruby_base = RubyCommands()

# Export the properly named group
ruby = ruby_base.group
ruby.name = "ruby"
