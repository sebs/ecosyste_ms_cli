"""Command line interface for ecosystems CLI."""

import json
from typing import Any, Dict, List, Optional

import click
from rich.console import Console
from rich.panel import Panel

from ecosystems_cli.api_client import get_client
from ecosystems_cli.commands.advisories import advisories
from ecosystems_cli.commands.archives import archives
from ecosystems_cli.commands.awesome import awesome
from ecosystems_cli.commands.commits import commits
from ecosystems_cli.commands.diff import diff
from ecosystems_cli.commands.docker import docker
from ecosystems_cli.commands.issues import issues
from ecosystems_cli.commands.licenses import licenses
from ecosystems_cli.commands.opencollective import opencollective
from ecosystems_cli.commands.ost import ost
from ecosystems_cli.commands.packages import packages
from ecosystems_cli.commands.papers import papers
from ecosystems_cli.commands.parser import parser
from ecosystems_cli.commands.repos import repos
from ecosystems_cli.commands.resolver import get_resolver_group
from ecosystems_cli.commands.ruby import ruby
from ecosystems_cli.commands.sbom import sbom
from ecosystems_cli.commands.sponsors import sponsors
from ecosystems_cli.commands.summary import summary
from ecosystems_cli.commands.timeline import timeline
from ecosystems_cli.constants import (
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_TIMEOUT,
    ERROR_PANEL_STYLE,
    ERROR_PREFIX,
    OUTPUT_FORMATS,
    SUPPORTED_APIS,
)
from ecosystems_cli.exceptions import EcosystemsCLIError, JSONParseError
from ecosystems_cli.helpers.format_value import format_value
from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence
from ecosystems_cli.helpers.print_operations import print_operations
from ecosystems_cli.helpers.print_output import print_output

console = Console()


@click.group()
@click.option(
    "--timeout",
    default=DEFAULT_TIMEOUT,
    help=f"Timeout in seconds for API requests. Default is {DEFAULT_TIMEOUT} seconds.",
)
@click.option(
    "--format",
    default=DEFAULT_OUTPUT_FORMAT,
    type=click.Choice(OUTPUT_FORMATS),
    help=f"Output format. Default is {DEFAULT_OUTPUT_FORMAT}.",
)
@click.option(
    "--domain",
    default=None,
    help="Override the API domain. Example: api.example.com",
)
@click.pass_context
def main(ctx, timeout, format, domain):
    """Ecosystems CLI for interacting with ecosyste.ms APIs."""
    ctx.ensure_object(dict)
    ctx.obj["timeout"] = timeout
    ctx.obj["format"] = format
    ctx.obj["domain"] = domain


# Add command groups to main
main.add_command(advisories)
main.add_command(archives)
main.add_command(commits)
main.add_command(docker)
main.add_command(repos)
main.add_command(packages)
main.add_command(summary)
main.add_command(awesome)
main.add_command(papers)
main.add_command(ost)
main.add_command(parser)
main.add_command(get_resolver_group())
main.add_command(sbom)
main.add_command(licenses)
main.add_command(diff)
main.add_command(timeline)
main.add_command(issues)
main.add_command(sponsors)
main.add_command(opencollective)
main.add_command(ruby)


@main.group()
def op():
    """Direct access to API operations with parameters as arguments."""
    pass


# Dynamic op commands will be registered below


def _parse_json_param(param: Optional[str]) -> Optional[Dict]:
    """Parse JSON parameter if provided."""
    if not param:
        return None
    try:
        return json.loads(param)
    except json.JSONDecodeError as e:
        raise JSONParseError(f"Invalid JSON: {param}. Error: {str(e)}")


def _call_operation(api: str, operation: str, path_params: str, query_params: str, body: str, context=None):
    """Call an operation on the specified API."""
    # Get timeout, format, and domain from context if available
    if context and hasattr(context, "obj"):
        timeout = context.obj.get("timeout", DEFAULT_TIMEOUT)
        format_type = context.obj.get("format", DEFAULT_OUTPUT_FORMAT)
        domain = context.obj.get("domain")
    else:
        timeout = DEFAULT_TIMEOUT
        format_type = DEFAULT_OUTPUT_FORMAT
        domain = None

    # Get domain with proper precedence
    final_domain = get_domain_with_precedence(api, domain)
    base_url = build_base_url(final_domain, api)

    try:
        client = get_client(api, base_url=base_url, timeout=timeout)

        # Parse parameters
        path_params_dict = _parse_json_param(path_params)
        query_params_dict = _parse_json_param(query_params)
        body_dict = _parse_json_param(body)

        result = client.call(
            operation_id=operation, path_params=path_params_dict, query_params=query_params_dict, body=body_dict
        )
        _print_output(result, format_type)
    except JSONParseError as e:
        _print_error(str(e))
    except EcosystemsCLIError as e:
        _print_error(str(e))
    except Exception as e:
        _print_error(f"Unexpected error: {str(e)}")


def create_dynamic_command(api_name: str, operation_id: str, client):
    """Create a dynamic command for an operation with appropriate parameters."""
    operation_details = client.endpoints.get(operation_id, {})
    required_params = operation_details.get("required_params", {})
    summary = operation_details.get("summary", "No description available")

    # Create a function that will be the command
    @click.argument("params", nargs=-1)
    def dynamic_command(params):
        """Execute the operation with provided parameters."""
        # Process parameters
        path_params = {}
        query_params = {}

        # Map positional arguments to parameters
        param_names = list(required_params.keys())
        for i, value in enumerate(params):
            if i < len(param_names):
                param_name = param_names[i]
                param_location = required_params[param_name].get("in")

                if param_location == "path":
                    path_params[param_name] = value
                elif param_location == "query":
                    query_params[param_name] = value

        try:
            result = client.call(operation_id=operation_id, path_params=path_params, query_params=query_params)
            # Default to table format
            _print_output(result, DEFAULT_OUTPUT_FORMAT)
        except EcosystemsCLIError as e:
            _print_error(str(e))
        except Exception as e:
            _print_error(f"Unexpected error: {str(e)}")

    # Set the docstring
    dynamic_command.__doc__ = summary
    if required_params:
        param_docs = [
            f"\n  {name}: {details.get('description', 'No description')}" for name, details in required_params.items()
        ]
        dynamic_command.__doc__ += "\n\nParameters:" + "".join(param_docs)

    # Create a proper Click command
    return click.command(name=operation_id)(dynamic_command)


def _print_output(data: Any, format_type: str = "table"):
    """Print data in the specified format."""
    print_output(data, format_type, console=console)


def _format_value(value: Any) -> str:
    """Deprecated: use format_value from helpers.format_value instead."""
    return format_value(value)


def _print_json(data: Any):
    """Print JSON data in a nicely formatted way."""
    _print_output(data, "json")


def _print_error(error_msg: str):
    """Print error message in a nicely formatted way."""
    console.print(Panel(f"{ERROR_PREFIX} {error_msg}", border_style=ERROR_PANEL_STYLE))


def _print_operations(operations: List[Dict]):
    print_operations(operations, console=console)


# Register dynamic 'op' commands for each API
for api_name in SUPPORTED_APIS:
    # Create a sub-group for each API under 'op'
    api_group = click.Group(name=api_name, help=f"Operations for {api_name} API")
    op.add_command(api_group)

    # Create client to get operations
    client = get_client(api_name)

    # Register each operation as a command
    for operation in client.list_operations():
        operation_id = operation.get("id")
        if operation_id and operation_id not in ["list", "operations"]:  # Skip reserved command names
            cmd = create_dynamic_command(api_name, operation_id, client)
            api_group.add_command(cmd)
