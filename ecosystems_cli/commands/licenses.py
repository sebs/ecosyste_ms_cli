"""Commands for the licenses API."""

import re

import click

from ecosystems_cli.commands.decorators import api_command, common_options, resolve_context_value
from ecosystems_cli.constants import DEFAULT_OUTPUT_FORMAT, DEFAULT_TIMEOUT
from ecosystems_cli.helpers.load_api_spec import load_api_spec


def _operation_id_to_command_name(operation_id: str) -> str:
    """Convert operationId to command name.

    Examples:
    - createJob -> create_job
    - getJob -> get_job
    """
    # Convert camelCase to snake_case
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", operation_id)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


@click.group(help="Commands for the licenses API.")
@common_options
@click.pass_context
def licenses(ctx, timeout, format, domain):
    """Commands for the licenses API."""
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Resolve context values using helper function
    timeout = resolve_context_value(ctx, "timeout", timeout, DEFAULT_TIMEOUT)
    format = resolve_context_value(ctx, "format", format, DEFAULT_OUTPUT_FORMAT)
    domain = resolve_context_value(ctx, "domain", domain, None)

    # Set the final values
    ctx.obj["timeout"] = timeout
    ctx.obj["format"] = format
    ctx.obj["domain"] = domain


def _register_commands():
    """Register all commands for the licenses API dynamically from OpenAPI spec."""
    # Load the OpenAPI spec
    spec = load_api_spec("licenses")

    # Iterate through all paths and operations
    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method in ["get", "post", "put", "delete", "patch"]:
                operation_id = operation.get("operationId")
                if not operation_id:
                    continue

                # Convert operationId to command name
                command_name = _operation_id_to_command_name(operation_id)
                description = operation.get("summary", f"Execute {operation_id}")

                # Get parameters
                parameters = operation.get("parameters", [])

                if not parameters:
                    # Simple command without parameters
                    @licenses.command(name=command_name, help=description)
                    @api_command("licenses", operation_id=operation_id)
                    def command_impl():
                        pass

                else:
                    # Command with parameters - create dynamic function to avoid closure issues
                    def create_command(op_id, cmd_name, desc):
                        @licenses.command(name=cmd_name, help=desc)
                        @api_command("licenses", operation_id=op_id)
                        def command_impl():
                            pass

                        return command_impl

                    create_command(operation_id, command_name, description)


# Register commands
_register_commands()
