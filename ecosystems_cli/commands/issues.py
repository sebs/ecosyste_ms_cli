"""Commands for the issues API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class IssuesCommands(BaseCommand):
    """Commands for the issues API."""

    def __init__(self):
        super().__init__("issues", "Commands for the issues API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the issues API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("hosts", "getRegistries", "Get all issue hosts.")

        # Register commands with error handling
        @self.create_command_with_error_handling("host", "getHost", "Get a specific host by name.", click.argument("host_name"))
        def get_host(host_name: str):
            pass

        @self.create_command_with_error_handling(
            "host-repositories", "getHostRepositories", "Get a list of repositories from a host.", click.argument("host_name")
        )
        def get_host_repositories(host_name: str):
            pass

        @self.create_command_with_error_handling(
            "repository",
            "getHostRepository",
            "Get a repository from a host.",
            click.argument("host_name"),
            click.argument("repo_name"),
        )
        def get_repository(host_name: str, repo_name: str):
            pass

        @self.create_command_with_error_handling(
            "repository-issues",
            "getHostRepositoryIssues",
            "Get a list of issues from a repository.",
            click.argument("host_name"),
            click.argument("repo_name"),
        )
        def get_repository_issues(host_name: str, repo_name: str):
            pass

        @self.create_command_with_error_handling(
            "issue",
            "getHostRepositoryIssue",
            "Get an issue from a repository.",
            click.argument("host_name"),
            click.argument("repo_name"),
            click.argument("issue_number", type=int),
        )
        def get_issue(host_name: str, repo_name: str, issue_number: int):
            pass

        @self.create_command_with_error_handling(
            "lookup", "repositoriesLookup", "Lookup repository metadata by URL.", click.argument("url")
        )
        def lookup_repository(url: str):
            pass  # Create the command group


issues_base = IssuesCommands()

# Export the properly named group
issues = issues_base.group
issues.name = "issues"
