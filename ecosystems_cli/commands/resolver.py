"""Commands for the resolver API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class ResolverCommands(BaseCommand):
    """Commands for interacting with the resolver API."""

    def __init__(self):
        """Initialize resolver commands."""
        super().__init__("resolver", "Commands for the resolver API")
        self._register_commands()

    def _register_commands(self):
        """Register all resolver commands."""
        # List operations command
        self.list_operations()

        # Create job command (convenience command for createJob operation)
        @self.group.command("create-job")
        @click.argument("package_name")
        @click.argument("registry")
        @click.option("--before", help="Resolve only with dependencies before this date (ISO format)")
        @click.option("--version", help="Resolve only with version within this range")
        @click.pass_context
        def create_job(ctx, package_name: str, registry: str, before: str = None, version: str = None):
            """Submit a resolve job."""
            from ecosystems_cli.api_client import get_client
            from ecosystems_cli.exceptions import EcosystemsCLIError
            from ecosystems_cli.helpers.print_error import print_error
            from ecosystems_cli.helpers.print_output import print_output

            client = get_client(self.api_name, timeout=ctx.obj.get("timeout", 20))
            try:
                query_params = {"package_name": package_name, "registry": registry}
                if before:
                    query_params["before"] = before
                if version:
                    query_params["version"] = version

                result = client.call("createJob", path_params={}, query_params=query_params)
                print_output(result, ctx.obj.get("format", "table"), console=self.console)
            except EcosystemsCLIError as e:
                print_error(str(e), console=self.console)
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}", console=self.console)

        # Get job command (convenience command for getJob operation)
        @self.group.command("get-job")
        @click.argument("job_id")
        @click.pass_context
        def get_job(ctx, job_id: str):
            """Fetch job by ID."""
            from ecosystems_cli.api_client import get_client
            from ecosystems_cli.exceptions import EcosystemsCLIError
            from ecosystems_cli.helpers.print_error import print_error
            from ecosystems_cli.helpers.print_output import print_output

            client = get_client(self.api_name, timeout=ctx.obj.get("timeout", 20))
            try:
                result = client.call("getJob", path_params={"jobID": job_id}, query_params={})
                print_output(result, ctx.obj.get("format", "table"), console=self.console)
            except EcosystemsCLIError as e:
                print_error(str(e), console=self.console)
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}", console=self.console)

        # Generic call command
        self.call_operation()


def get_resolver_group():
    """Get the resolver command group."""
    commands = ResolverCommands()
    return commands.group
