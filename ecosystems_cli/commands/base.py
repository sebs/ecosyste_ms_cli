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
from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence
from ecosystems_cli.helpers.print_error import print_error
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
    f = click.option(
        "--domain",
        default=None,
        help="Override the API domain. Example: api.example.com",
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
        def group(ctx, timeout, format, domain):
            # Ensure context object exists
            ctx.ensure_object(dict)

            # Resolve context values using helper function
            timeout = self._resolve_context_value(ctx, "timeout", timeout, DEFAULT_TIMEOUT)
            format = self._resolve_context_value(ctx, "format", format, DEFAULT_OUTPUT_FORMAT)
            domain = self._resolve_context_value(ctx, "domain", domain, None)

            # Set the final values
            ctx.obj["timeout"] = timeout
            ctx.obj["format"] = format
            ctx.obj["domain"] = domain

        self.group = group

    def _resolve_context_value(self, ctx, key, current_value, default_value):
        """Helper to resolve context values with inheritance.

        Args:
            ctx: Click context
            key: Context key to resolve
            current_value: Current value from command options
            default_value: Default value for comparison

        Returns:
            Resolved value considering context inheritance
        """
        # If current value is not default, use it
        if current_value != default_value:
            return current_value

        # Check current context for existing value
        if key in ctx.obj:
            return ctx.obj[key]

        # Check parent context
        if ctx.parent and ctx.parent.obj:
            parent_value = ctx.parent.obj.get(key, default_value)
            if parent_value != default_value:
                return parent_value

        # Return current value (which is the default)
        return current_value

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
        def command_impl(ctx, timeout, format, domain):
            # Update context with command-level options
            ctx.ensure_object(dict)
            if timeout != DEFAULT_TIMEOUT:
                ctx.obj["timeout"] = timeout
            if format != DEFAULT_OUTPUT_FORMAT:
                ctx.obj["format"] = format
            if domain is not None:
                ctx.obj["domain"] = domain

            # Get domain with proper precedence
            domain = get_domain_with_precedence(self.api_name, ctx.obj.get("domain"))
            base_url = build_base_url(domain, self.api_name)

            client = get_client(self.api_name, base_url=base_url, timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT))
            try:
                if operation_id and method_name == "call":
                    result = client.call(operation_id, path_params={}, query_params={})
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
            def wrapper(ctx, timeout, format, domain, **kwargs):
                # Update context with command-level options
                ctx.ensure_object(dict)
                if timeout != DEFAULT_TIMEOUT:
                    ctx.obj["timeout"] = timeout
                if format != DEFAULT_OUTPUT_FORMAT:
                    ctx.obj["format"] = format
                if domain is not None:
                    ctx.obj["domain"] = domain

                # Get domain with proper precedence
                domain = get_domain_with_precedence(self.api_name, ctx.obj.get("domain"))
                base_url = build_base_url(domain, self.api_name)

                client = get_client(self.api_name, base_url=base_url, timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT))
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
            def wrapper(ctx, timeout, format, domain, *args, **kwargs):
                # Update context with command-level options
                ctx.ensure_object(dict)
                if timeout != DEFAULT_TIMEOUT:
                    ctx.obj["timeout"] = timeout
                if format != DEFAULT_OUTPUT_FORMAT:
                    ctx.obj["format"] = format
                if domain is not None:
                    ctx.obj["domain"] = domain

                # Get domain with proper precedence
                domain = get_domain_with_precedence(self.api_name, ctx.obj.get("domain"))
                base_url = build_base_url(domain, self.api_name)

                client = get_client(self.api_name, base_url=base_url, timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT))
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
