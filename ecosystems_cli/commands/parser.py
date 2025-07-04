from typing import Dict

import click

from ecosystems_cli.commands.base import BaseCommand


class ParserCommands(BaseCommand):
    def __init__(self) -> None:
        super().__init__("parser", "Parse dependency metadata from manifest files")
        self._register_commands()

    def _register_commands(self) -> None:
        self.list_operations()

        self.create_simple_command(
            "formats",
            "call",
            "List supported file formats and ecosystems",
            operation_id="jobFormats",
        )

        @self.create_command_with_operation(
            "submit",
            "createJob",
            "Submit a dependency parsing job",
            click.argument("url"),
        )
        def submit_job(url: str) -> Dict[str, str]:
            return {"url": url}

        @self.create_command_with_operation(
            "status",
            "getJob",
            "Get status of a parsing job",
            click.argument("job_id"),
        )
        def get_job_status(job_id: str) -> Dict[str, str]:
            return {"jobID": job_id}

        self.call_operation()


# Create the command group
parser_base = ParserCommands()

# Export the properly named group
parser_commands = parser_base
parser = parser_base.group
parser.name = "parser"
