"""Commands for the packages API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class PackagesCommands(BaseCommand):
    """Commands for the packages API."""

    def __init__(self) -> None:
        super().__init__("packages", "Commands for the packages API.")
        self._register_commands()

    def _register_commands(self) -> None:
        """Register all commands for the packages API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("registries", "get_registries", "Get all package registries.")

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "registry", "get_registry", "Get a specific registry by name.", click.argument("name")
        )
        def get_registry(name: str) -> None:
            pass

        @self.create_command_with_error_handling(
            "package",
            "get_package",
            "Get a specific package from a registry.",
            click.argument("registry"),
            click.argument("package"),
        )
        def get_package(registry: str, package: str) -> None:
            pass

        @self.create_command_with_error_handling(
            "version",
            "get_package_version",
            "Get a specific package version.",
            click.argument("registry"),
            click.argument("package"),
            click.argument("version"),
        )
        def get_package_version(registry: str, package: str, version: str) -> None:
            pass  # Create the command group


packages_base = PackagesCommands()

# Export the properly named group
packages = packages_base.group
packages.name = "packages"
