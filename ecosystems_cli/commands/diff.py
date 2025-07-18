"""Commands for the diff API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class DiffCommands(BaseCommand):
    """Commands for the diff API."""

    def __init__(self):
        super().__init__("diff", "Commands for the diff API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the diff API."""
        # Register list operations command
        self.list_operations()

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "create-job",
            "createJob",
            "Submit a diff job between two URLs.",
            click.argument("url_1"),
            click.argument("url_2"),
        )
        def create_job(url_1: str, url_2: str):
            pass

        @self.create_command_with_error_handling("get-job", "getJob", "Fetch a diff job by ID.", click.argument("job_id"))
        def get_job(job_id: str):
            pass  # Create the command group


diff_base = DiffCommands()

# Export the properly named group
diff = diff_base.group
diff.name = "diff"
