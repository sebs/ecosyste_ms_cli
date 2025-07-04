"""Base command class for ecosystems CLI commands."""

from functools import wraps
from typing import Callable

import click
from rich.console import Console

from ecosystems_cli.api_client import get_client
from ecosystems_cli.commands.handlers import OperationHandlerFactory
from ecosystems_cli.constants import (
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_TIMEOUT,
    OUTPUT_FORMATS,
)
from ecosystems_cli.exceptions import EcosystemsCLIError
from ecosystems_cli.helpers.print_error import print_error
from ecosystems_cli.helpers.print_operations import print_operations
from ecosystems_cli.helpers.print_output import print_output


def common_options(f):
    """Decorator to add common options to commands."""
    f = click.option(
        "--format",
        default=DEFAULT_OUTPUT_FORMAT,
        type=click.Choice(OUTPUT_FORMATS),
        help=f"Output format. Default is {DEFAULT_OUTPUT_FORMAT}.",
    )(f)
    f = click.option(
        "--timeout",
        default=DEFAULT_TIMEOUT,
        help=f"Timeout in seconds for API requests. Default is {DEFAULT_TIMEOUT} seconds.",
    )(f)
    return f


class BaseCommand:
    """Base class for API command groups."""

    def __init__(self, api_name: str, description: str):
        """Initialize base command.

        Args:
            api_name: Name of the API (e.g., 'repos', 'packages')
            description: Description of the command group
        """
        self.api_name = api_name
        self.description = description
        self.console = Console()

        # Create the group with proper decorator
        @click.group(help=description)
        @common_options
        @click.pass_context
        def group(ctx, timeout, format):
            # Ensure context object exists
            ctx.ensure_object(dict)

            # Check if values were already set in context (e.g., by tests)
            # Only preserve them if the provided values are defaults
            if timeout == DEFAULT_TIMEOUT and "timeout" in ctx.obj:
                timeout = ctx.obj["timeout"]
            elif ctx.parent and ctx.parent.obj and timeout == DEFAULT_TIMEOUT:
                # Use parent value if current value is default
                parent_timeout = ctx.parent.obj.get("timeout", DEFAULT_TIMEOUT)
                if parent_timeout != DEFAULT_TIMEOUT:
                    timeout = parent_timeout

            if format == DEFAULT_OUTPUT_FORMAT and "format" in ctx.obj:
                format = ctx.obj["format"]
            elif ctx.parent and ctx.parent.obj and format == DEFAULT_OUTPUT_FORMAT:
                # Use parent value if current value is default
                parent_format = ctx.parent.obj.get("format", DEFAULT_OUTPUT_FORMAT)
                if parent_format != DEFAULT_OUTPUT_FORMAT:
                    format = parent_format

            # Set the final values
            ctx.obj["timeout"] = timeout
            ctx.obj["format"] = format

        self.group = group

    def list_operations(self) -> Callable:
        """Create a command to list available operations."""

        @common_options
        @click.pass_context
        def list_operations_impl(ctx, timeout, format):
            """List available operations for the API."""
            # Update context with command-level options
            ctx.ensure_object(dict)
            if timeout != DEFAULT_TIMEOUT:
                ctx.obj["timeout"] = timeout
            if format != DEFAULT_OUTPUT_FORMAT:
                ctx.obj["format"] = format

            client = get_client(self.api_name, timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT))
            print_operations(client.list_operations(), console=self.console)

        # Set the function name and docstring dynamically
        list_operations_impl.__name__ = f"list_{self.api_name}_operations"
        list_operations_impl.__doc__ = f"List available operations for {self.api_name} API."

        return self.group.command("list")(list_operations_impl)

    def create_simple_command(self, name: str, method_name: str, description: str, operation_id: str = None) -> Callable:
        """Create a simple command that calls an API method without parameters.

        Args:
            name: Command name
            method_name: API client method name
            description: Command description
            operation_id: Optional operation ID for 'call' method
        """

        @common_options
        @click.pass_context
        def command_impl(ctx, timeout, format):
            # Update context with command-level options
            ctx.ensure_object(dict)
            if timeout != DEFAULT_TIMEOUT:
                ctx.obj["timeout"] = timeout
            if format != DEFAULT_OUTPUT_FORMAT:
                ctx.obj["format"] = format

            client = get_client(self.api_name, timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT))
            try:
                if operation_id and method_name == "call":
                    result = client.call(operation_id)
                else:
                    result = getattr(client, method_name)()
                print_output(result, ctx.obj.get("format", DEFAULT_OUTPUT_FORMAT), console=self.console)
            except EcosystemsCLIError as e:
                print_error(str(e), console=self.console)
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}", console=self.console)

        command_impl.__doc__ = description
        return self.group.command(name)(command_impl)

    def create_command_with_error_handling(self, name: str, method_name: str, description: str, *args) -> Callable:
        """Create a command with error handling.

        Args:
            name: Command name
            method_name: API client method name
            description: Command description
            *args: Click argument decorators
        """

        def decorator(func):
            @common_options
            @click.pass_context
            @wraps(func)
            def wrapper(ctx, timeout, format, **kwargs):
                # Update context with command-level options
                ctx.ensure_object(dict)
                if timeout != DEFAULT_TIMEOUT:
                    ctx.obj["timeout"] = timeout
                if format != DEFAULT_OUTPUT_FORMAT:
                    ctx.obj["format"] = format

                client = get_client(self.api_name, timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT))
                try:
                    result = getattr(client, method_name)(**kwargs)
                    print_output(result, ctx.obj.get("format", DEFAULT_OUTPUT_FORMAT), console=self.console)
                except EcosystemsCLIError as e:
                    print_error(str(e), console=self.console)
                except Exception as e:
                    print_error(f"Unexpected error: {str(e)}", console=self.console)

            # Apply click decorators in reverse order
            for arg in reversed(args):
                wrapper = arg(wrapper)

            wrapper.__doc__ = description
            return self.group.command(name)(wrapper)

        return decorator

    def create_command_with_operation(self, name: str, operation_id: str, description: str, *args) -> Callable:
        """Create a command that calls a specific operation ID.

        Args:
            name: Command name
            operation_id: Operation ID to call
            description: Command description
            *args: Click argument decorators
        """

        def decorator(func):
            @common_options
            @click.pass_context
            @wraps(func)
            def wrapper(ctx, timeout, format, *args, **kwargs):
                # Update context with command-level options
                ctx.ensure_object(dict)
                if timeout != DEFAULT_TIMEOUT:
                    ctx.obj["timeout"] = timeout
                if format != DEFAULT_OUTPUT_FORMAT:
                    ctx.obj["format"] = format

                client = get_client(self.api_name, timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT))
                try:
                    # Use operation handler to build parameters
                    handler = OperationHandlerFactory.get_handler(self.api_name)
                    path_params, query_params = handler.build_params(operation_id, args, kwargs)

                    result = client.call(operation_id, path_params=path_params, query_params=query_params)
                    print_output(result, ctx.obj.get("format", DEFAULT_OUTPUT_FORMAT), console=self.console)
                except EcosystemsCLIError as e:
                    print_error(str(e), console=self.console)
                except Exception as e:
                    print_error(f"Unexpected error: {str(e)}", console=self.console)

            # Apply click decorators in reverse order
            for arg in reversed(args):
                wrapper = arg(wrapper)

            wrapper.__doc__ = description
            return self.group.command(name)(wrapper)

        return decorator

    def call_operation(self) -> Callable:
        """Create a generic call command for the API."""

        @click.argument("operation")
        @click.option("--path-params", help="Path parameters as JSON")
        @click.option("--query-params", help="Query parameters as JSON")
        @click.option("--body", help="Request body as JSON")
        @common_options
        @click.pass_context
        def call_operation_impl(ctx, operation: str, path_params: str, query_params: str, body: str, timeout, format):
            """Call an operation on the API."""
            # Update context with command-level options
            ctx.ensure_object(dict)
            if timeout != DEFAULT_TIMEOUT:
                ctx.obj["timeout"] = timeout
            if format != DEFAULT_OUTPUT_FORMAT:
                ctx.obj["format"] = format

            from ecosystems_cli.cli import _call_operation

            _call_operation(self.api_name, operation, path_params, query_params, body, ctx)

        call_operation_impl.__doc__ = f"Call an operation on the {self.api_name} API."
        return self.group.command("call")(call_operation_impl)
