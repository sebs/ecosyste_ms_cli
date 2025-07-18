"""Commands for the archives API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class ArchivesCommands(BaseCommand):
    """Commands for the archives API."""

    def __init__(self):
        super().__init__("archives", "Commands for the archives API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the archives API."""
        # Register list operations command
        self.list_operations()

        # Register commands with operation IDs
        @self.create_command_with_operation(
            "list-files",
            "list",
            "List files in an archive.",
            click.argument("url"),
        )
        def list_files(url: str):
            pass

        @self.create_command_with_operation(
            "contents",
            "contents",
            "Get contents of a path from an archive.",
            click.argument("url"),
            click.argument("path"),
        )
        def get_contents(url: str, path: str):
            pass

        @self.create_command_with_operation(
            "readme",
            "readme",
            "Get readme from an archive.",
            click.argument("url"),
        )
        def get_readme(url: str):
            pass

        @self.create_command_with_operation(
            "changelog",
            "changelog",
            "Get changelog from an archive.",
            click.argument("url"),
        )
        def get_changelog(url: str):
            pass

        @self.create_command_with_operation(
            "repopack",
            "repopack",
            "Get repopack from an archive.",
            click.argument("url"),
        )
        def get_repopack(url: str):
            pass  # Create the command group


archives_base = ArchivesCommands()

# Export the properly named group
archives = archives_base.group
archives.name = "archives"
