"""Commands for the commits API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class CommitsCommands(BaseCommand):
    """Commands for the commits API."""

    def __init__(self):
        super().__init__("commits", "Commands for the commits API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the commits API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("hosts", "getRegistries", "List all repository hosts.")

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "lookup", "repositoriesLookup", "Lookup repository metadata by URL.", click.argument("url")
        )
        def lookup(url: str):
            pass

        @self.create_command_with_error_handling("host", "getHost", "Get a specific host by name.", click.argument("host_name"))
        def get_host(host_name: str):
            pass

        @self.create_command_with_error_handling(
            "host-repositories", "getHostRepositories", "Get repositories from a specific host.", click.argument("host_name")
        )
        def get_host_repositories(host_name: str):
            pass

        @self.create_command_with_error_handling(
            "repository",
            "getHostRepository",
            "Get a specific repository from a host.",
            click.argument("host_name"),
            click.argument("repo_name"),
        )
        def get_repository(host_name: str, repo_name: str):
            pass

        @self.create_command_with_error_handling(
            "commits",
            "getRepositoryCommits",
            "Get commits from a repository.",
            click.argument("host_name"),
            click.argument("repo_name"),
        )
        def get_commits(host_name: str, repo_name: str):
            pass  # Create the command group


commits_base = CommitsCommands()

# Export the properly named group
commits = commits_base.group
commits.name = "commits"
