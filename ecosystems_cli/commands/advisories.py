"""Commands for the advisories API."""

import re

import click

from ecosystems_cli.commands.decorators import api_command, common_options, resolve_context_value
from ecosystems_cli.constants import DEFAULT_OUTPUT_FORMAT, DEFAULT_TIMEOUT
from ecosystems_cli.helpers.load_api_spec import load_api_spec


def _operation_id_to_command_name(operation_id: str) -> str:
    """Convert operationId to command name.

    Examples:
    - getAdvisories -> get_advisories
    - getAdvisoriesPackages -> get_advisories_packages
    - getAdvisory -> get_advisory
    """
    # Convert camelCase to snake_case
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", operation_id)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


@click.group(help="Commands for the advisories API.")
@common_options
@click.pass_context
def advisories(ctx, timeout, format, domain):
    """Commands for the advisories API."""
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
    """Register all commands for the advisories API dynamically from OpenAPI spec."""
    # Load the OpenAPI spec
    spec = load_api_spec("advisories")

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
                    @advisories.command(name=command_name, help=description)
                    @api_command("advisories", operation_id=operation_id)
                    def command_impl():
                        pass

                else:
                    # Build click options and arguments
                    click_decorators = []
                    for param in parameters:
                        param_name = param.get("name")
                        param_in = param.get("in")
                        param_description = param.get("description", "")
                        param_required = param.get("required", False)
                        param_schema = param.get("schema", {})
                        param_type = param_schema.get("type", "string")

                        # Convert parameter name to Python-friendly format
                        python_param_name = param_name.replace("_", "-")

                        if param_in == "path":
                            # Path parameters become arguments
                            click_decorators.append(click.argument(param_name))
                        elif param_in == "query":
                            # Query parameters become options
                            click_type = None
                            if param_type == "integer":
                                click_type = int
                            elif param_type == "boolean":
                                click_type = bool

                            option_decorator = click.option(
                                f"--{python_param_name}",
                                param_name.replace("-", "_"),  # Use underscore for Python variable
                                type=click_type,
                                help=param_description,
                                required=param_required,
                            )
                            click_decorators.append(option_decorator)

                    # Create the command with parameters
                    # We need to create a closure to capture the operation_id
                    def make_command(op_id):
                        @advisories.command(
                            name=_operation_id_to_command_name(op_id), help=operation.get("summary", f"Execute {op_id}")
                        )
                        @common_options
                        @click.pass_context
                        def command_impl(ctx, timeout, format, domain, *args, **kwargs):
                            from ecosystems_cli.commands.execution import (
                                execute_api_call,
                                update_context,
                            )

                            update_context(ctx, timeout, format, domain)
                            execute_api_call(ctx, "advisories", operation_id=op_id, call_args=args, call_kwargs=kwargs)

                        # Apply click decorators in reverse order
                        for decorator in reversed(click_decorators):
                            command_impl = decorator(command_impl)

                        return command_impl

                    make_command(operation_id)


# Register commands when the module is imported
_register_commands()

# Set the name attribute for consistency
advisories.name = "advisories"
