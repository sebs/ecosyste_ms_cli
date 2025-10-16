"""Commands for the parser API."""

import time
from typing import Optional

import click
from rich.console import Console

from ecosystems_cli.commands.decorators import common_options
from ecosystems_cli.commands.execution import update_context
from ecosystems_cli.commands.generator import APICommandGenerator
from ecosystems_cli.constants import DEFAULT_OUTPUT_FORMAT, DEFAULT_TIMEOUT
from ecosystems_cli.exceptions import EcosystemsCLIError
from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence
from ecosystems_cli.helpers.print_error import print_error
from ecosystems_cli.helpers.print_output import print_output
from ecosystems_cli.openapi_client import _factory as api_factory

console = Console()

parser = APICommandGenerator.create_api_group("parser")


# Remove auto-generated create_job command to replace with custom implementation
if "create_job" in parser.commands:
    del parser.commands["create_job"]


@parser.command(name="create_job", help="Submit a dependency parsing job")
@click.argument("url", required=True)
@click.option(
    "--polling-interval",
    type=float,
    default=None,
    help="Polling interval in seconds. If set, the command will poll the job status until completion.",
)
@common_options
@click.pass_context
def create_job(
    ctx, timeout: int, format: str, domain: Optional[str], mailto: Optional[str], url: str, polling_interval: Optional[float]
):
    """Submit a dependency parsing job.

    Args:
        ctx: Click context
        timeout: Request timeout
        format: Output format
        domain: API domain
        mailto: Email for polite pool access
        url: URL of file or zip/tar archive
        polling_interval: Optional polling interval in seconds
    """
    update_context(ctx, timeout, format, domain, mailto)

    # Get domain with proper precedence
    api_domain = get_domain_with_precedence("parser", ctx.obj.get("domain"))
    base_url = build_base_url(api_domain, "parser")

    try:
        # Create the job
        from ecosystems_cli.commands.handlers import OperationHandlerFactory

        handler = OperationHandlerFactory.get_handler("parser")
        path_params, query_params = handler.build_params("createJob", (), {"url": url})

        result = api_factory.call(
            "parser",
            "createJob",
            path_params=path_params,
            query_params=query_params,
            timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT),
            mailto=ctx.obj.get("mailto"),
            base_url=base_url,
        )

        # If polling is enabled, poll for job completion
        if polling_interval is not None:
            # Try to get job ID from direct response or from location URL
            job_id = result.get("id")

            if not job_id:
                # Try to extract job ID from location URL
                location = result.get("location", "")
                if location:
                    # Extract job ID from URL like: https://parser.ecosyste.ms/api/v1/jobs/{job_id}
                    parts = location.rstrip("/").split("/")
                    if len(parts) > 0:
                        job_id = parts[-1]

            if not job_id:
                print_error("No job ID in response, cannot poll for completion", console=console)
                print_output(result, ctx.obj.get("format", DEFAULT_OUTPUT_FORMAT), console=console)
                return

            # Only show progress messages in interactive mode (table format)
            output_format = ctx.obj.get("format", DEFAULT_OUTPUT_FORMAT)
            is_interactive = output_format == "table"

            if is_interactive:
                console.print(f"[yellow]Job created with ID: {job_id}[/yellow]")
                console.print(f"[yellow]Polling every {polling_interval} seconds...[/yellow]")

            while True:
                time.sleep(polling_interval)

                # Get job status
                handler_get = OperationHandlerFactory.get_handler("parser")
                path_params_get, query_params_get = handler_get.build_params("getJob", (), {"job_id": job_id})

                job_status = api_factory.call(
                    "parser",
                    "getJob",
                    path_params=path_params_get,
                    query_params=query_params_get,
                    timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT),
                    mailto=ctx.obj.get("mailto"),
                    base_url=base_url,
                )

                status = job_status.get("status", "unknown")
                if is_interactive:
                    console.print(f"[cyan]Job status: {status}[/cyan]")

                # Check if job is complete
                if status in ["completed", "complete", "success", "failed", "error"]:
                    print_output(job_status, output_format, console=console)
                    break
        else:
            # No polling, just print the result
            print_output(result, ctx.obj.get("format", DEFAULT_OUTPUT_FORMAT), console=console)

    except EcosystemsCLIError as e:
        print_error(str(e), console=console)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}", console=console)
