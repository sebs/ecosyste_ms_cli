"""Commands for the docker API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class DockerCommands(BaseCommand):
    """Commands for the docker API."""

    def __init__(self):
        super().__init__("docker", "Commands for the docker API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the docker API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("packages", "call", "Get a list of packages.", "getPackages")
        self.create_simple_command("usage", "call", "Get package usage ecosystems.", "usage")

        # Register commands with operation IDs
        @self.create_command_with_operation("package", "getPackage", "Get a package by name.", click.argument("package_name"))
        def get_package(package_name: str):
            pass

        @self.create_command_with_operation(
            "versions",
            "getPackageVersions",
            "Get a list of versions for a package.",
            click.argument("package_name"),
        )
        def get_package_versions(package_name: str):
            pass

        @self.create_command_with_operation(
            "version",
            "getPackageVersion",
            "Get a version of a package.",
            click.argument("package_name"),
            click.argument("version_number"),
        )
        def get_package_version(package_name: str, version_number: str):
            pass

        @self.create_command_with_operation(
            "usage-ecosystem",
            "usageEcosystem",
            "Get package usage for an ecosystem.",
            click.argument("ecosystem"),
        )
        def usage_ecosystem(ecosystem: str):
            pass

        @self.create_command_with_operation(
            "usage-package",
            "usagePackage",
            "Get package usage for a package.",
            click.argument("ecosystem"),
            click.argument("package"),
        )
        def usage_package(ecosystem: str, package: str):
            pass  # Create the command group


docker_base = DockerCommands()

# Export the properly named group
docker = docker_base.group
docker.name = "docker"
