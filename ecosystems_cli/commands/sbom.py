"""Commands for the SBOM API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class SbomCommands(BaseCommand):
    """Commands for the SBOM API."""

    def __init__(self):
        super().__init__("sbom", "Commands for the SBOM API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the SBOM API."""
        # Register list operations command
        self.list_operations()

        # Register commands with error handling
        @self.create_command_with_error_handling(
            "submit-job",
            "createJob",
            "Submit a dependency parsing job.",
            click.option("--url", required=True, help="URL of file or zip/tar archive"),
        )
        def create_job(url: str):
            pass

        @self.create_command_with_error_handling("get-job", "getJob", "Fetch job by ID.", click.argument("job_id"))
        def get_job(job_id: str):
            pass  # Create the command group


sbom_base = SbomCommands()

# Export the properly named group
sbom = sbom_base.group
sbom.name = "sbom"
