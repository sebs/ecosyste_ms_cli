import click

from ecosystems_cli.commands.base import BaseCommand


class LicensesCommands(BaseCommand):
    def __init__(self):
        super().__init__("licenses", "Parse license metadata from open source software ecosystems")
        self._register_commands()

    def _register_commands(self):
        self.list_operations()

        @self.create_command_with_operation(
            "submit",
            "createJob",
            "Submit a license parsing job",
            click.argument("url"),
        )
        def submit_job(url: str):
            return {"url": url}

        @self.create_command_with_operation(
            "status",
            "getJob",
            "Get status of a license parsing job",
            click.argument("job_id"),
        )
        def get_job_status(job_id: str):
            return {"jobID": job_id}

        self.call_operation()


# Create the command group
licenses_base = LicensesCommands()

# Export the properly named group
licenses_commands = licenses_base
licenses = licenses_base.group
licenses.name = "licenses"
