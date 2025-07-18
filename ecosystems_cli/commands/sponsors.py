"""Commands for the sponsors API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class SponsorsCommands(BaseCommand):
    """Commands for the sponsors API."""

    def __init__(self):
        super().__init__("sponsors", "Commands for the sponsors API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the sponsors API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("accounts", "list_accounts", "List all maintainer accounts.")
        self.create_simple_command("sponsors", "list_sponsors", "List all sponsors.")

        # Register commands with error handling
        @self.create_command_with_error_handling("account", "get_account", "Get an account by login.", click.argument("login"))
        def get_account(login: str):
            pass

        @self.create_command_with_error_handling(
            "account-sponsors", "list_account_sponsors", "List all sponsors for an account.", click.argument("login")
        )
        def list_account_sponsors(login: str):
            pass

        @self.create_command_with_error_handling(
            "account-sponsorships",
            "list_account_sponsorships",
            "List all sponsorships for an account.",
            click.argument("login"),
        )
        def list_account_sponsorships(login: str):
            pass  # Create the command group


sponsors_base = SponsorsCommands()

# Export the properly named group
sponsors = sponsors_base.group
sponsors.name = "sponsors"
