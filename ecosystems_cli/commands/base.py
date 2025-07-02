"""Base command class for ecosystems CLI commands."""

from functools import wraps
from typing import Callable

import click
from rich.console import Console

from ecosystems_cli.api_client import get_client
from ecosystems_cli.helpers.print_error import print_error
from ecosystems_cli.helpers.print_operations import print_operations
from ecosystems_cli.helpers.print_output import print_output


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
        @click.group()
        def group():
            pass

        group.__doc__ = description
        self.group = group

    def list_operations(self) -> Callable:
        """Create a command to list available operations."""

        @click.pass_context
        def list_operations_impl(ctx):
            """List available operations for the API."""
            client = get_client(self.api_name, timeout=ctx.obj.get("timeout", 20))
            print_operations(client.list_operations(), console=self.console)

        # Set the function name and docstring dynamically
        list_operations_impl.__name__ = f"list_{self.api_name}_operations"
        list_operations_impl.__doc__ = f"List available operations for {self.api_name} API."

        return self.group.command("list")(list_operations_impl)

    def create_simple_command(self, name: str, method_name: str, description: str) -> Callable:
        """Create a simple command that calls an API method without parameters.

        Args:
            name: Command name
            method_name: API client method name
            description: Command description
        """

        @click.pass_context
        def command_impl(ctx):
            client = get_client(self.api_name, timeout=ctx.obj.get("timeout", 20))
            result = getattr(client, method_name)()
            print_output(result, ctx.obj.get("format", "table"), console=self.console)

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
            @click.pass_context
            @wraps(func)
            def wrapper(ctx, *args, **kwargs):
                client = get_client(self.api_name, timeout=ctx.obj.get("timeout", 20))
                try:
                    result = getattr(client, method_name)(*args, **kwargs)
                    print_output(result, ctx.obj.get("format", "table"), console=self.console)
                except Exception as e:
                    print_error(str(e), console=self.console)

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
        @click.pass_context
        def call_operation_impl(ctx, operation: str, path_params: str, query_params: str, body: str):
            """Call an operation on the API."""
            from ecosystems_cli.cli import _call_operation

            _call_operation(self.api_name, operation, path_params, query_params, body, ctx)

        call_operation_impl.__doc__ = f"Call an operation on the {self.api_name} API."
        return self.group.command("call")(call_operation_impl)
