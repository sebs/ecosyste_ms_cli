"""Commands for the advisories API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class AdvisoriesCommands(BaseCommand):
    """Commands for the advisories API."""

    def __init__(self):
        super().__init__("advisories", "Commands for the advisories API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the advisories API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("packages", "get_advisories_packages", "List packages that have advisories.")

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "search",
            "get_advisories",
            "Search advisories with optional filters.",
            click.option("--ecosystem", help="Ecosystem to filter by"),
            click.option("--package-name", help="Package to filter by"),
            click.option("--severity", help="Severity to filter by"),
            click.option("--repository-url", help="Repository URL to filter by"),
            click.option("--page", type=int, help="Pagination page number"),
            click.option("--per-page", type=int, help="Number of records to return"),
            click.option("--created-after", help="Filter by created_at after given time"),
            click.option("--updated-after", help="Filter by updated_at after given time"),
            click.option("--sort", help="Field to order results by"),
            click.option("--order", help="Direction to order results by"),
        )
        def list_advisories(
            ecosystem=None,
            package_name=None,
            severity=None,
            repository_url=None,
            page=None,
            per_page=None,
            created_after=None,
            updated_after=None,
            sort=None,
            order=None,
        ):
            pass

        @self.create_command_with_error_handling(
            "get", "get_advisory", "Get an advisory by UUID.", click.argument("advisory_uuid")
        )
        def get_advisory(advisory_uuid: str):
            pass

        # Register call operation command
        self.call_operation()


# Create the command group
advisories_base = AdvisoriesCommands()

# Export the properly named group
advisories = advisories_base.group
advisories.name = "advisories"
