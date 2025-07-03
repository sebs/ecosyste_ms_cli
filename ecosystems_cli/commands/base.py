"""Base command class for ecosystems CLI commands."""

from functools import wraps
from typing import Callable

import click
from rich.console import Console

from ecosystems_cli.api_client import get_client
from ecosystems_cli.exceptions import EcosystemsCLIError
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

    def create_simple_command(self, name: str, method_name: str, description: str, operation_id: str = None) -> Callable:
        """Create a simple command that calls an API method without parameters.

        Args:
            name: Command name
            method_name: API client method name
            description: Command description
            operation_id: Optional operation ID for 'call' method
        """

        @click.pass_context
        def command_impl(ctx):
            client = get_client(self.api_name, timeout=ctx.obj.get("timeout", 20))
            if operation_id and method_name == "call":
                result = client.call(operation_id)
            else:
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
            @click.pass_context
            @wraps(func)
            def wrapper(ctx, *args, **kwargs):
                client = get_client(self.api_name, timeout=ctx.obj.get("timeout", 20))
                try:
                    # Build params based on operation requirements
                    path_params = {}
                    query_params = {}

                    # Special handling for resolver API
                    if self.api_name == "resolver":
                        if operation_id == "createJob" and len(args) >= 2:
                            # For resolver API createJob operation
                            query_params = {"package_name": args[0], "registry": args[1]}
                            # Handle optional parameters from kwargs
                            if "before" in kwargs and kwargs["before"]:
                                query_params["before"] = kwargs["before"]
                            if "version" in kwargs and kwargs["version"]:
                                query_params["version"] = kwargs["version"]
                        elif operation_id == "getJob" and len(args) == 1:
                            path_params = {"jobID": args[0]}
                    elif self.api_name == "archives":
                        # Handle archives API operations
                        # Click passes named arguments as keyword args, so check both
                        if operation_id == "list":
                            if len(args) == 1:
                                query_params = {"url": args[0]}
                            elif "url" in kwargs:
                                query_params = {"url": kwargs["url"]}
                        elif operation_id == "contents":
                            if len(args) == 2:
                                query_params = {"url": args[0], "path": args[1]}
                            elif "url" in kwargs and "path" in kwargs:
                                query_params = {"url": kwargs["url"], "path": kwargs["path"]}
                        elif operation_id in ["readme", "changelog", "repopack"]:
                            if len(args) == 1:
                                query_params = {"url": args[0]}
                            elif "url" in kwargs:
                                query_params = {"url": kwargs["url"]}
                    else:
                        # Check both args and kwargs for parameters
                        all_args = list(args) + list(kwargs.values())
                        if len(all_args) > 0:
                            # Map arguments to params based on operation ID
                            if (
                                operation_id
                                in ["getProject", "getList", "getListProjects", "getCollection", "getCollectionProjects"]
                                and len(all_args) == 1
                            ):
                                path_params = {"id": all_args[0]}
                            elif operation_id == "getTopic" and len(all_args) == 1:
                                path_params = {"slug": all_args[0]}
                            elif operation_id == "getCollective" and len(all_args) == 1:
                                path_params = {"id": all_args[0]}
                            elif operation_id == "getCollectiveProjects" and len(all_args) == 1:
                                path_params = {"slug": all_args[0]}
                            elif operation_id == "lookupProject" and len(all_args) == 1:
                                query_params = {"url": all_args[0]}
                            elif operation_id == "createJob" and len(all_args) == 1:
                                # For other APIs' createJob operation
                                query_params = {"url": all_args[0]}
                            elif operation_id == "getJob" and len(all_args) == 1:
                                path_params = {"jobID": all_args[0]}

                    result = client.call(operation_id, path_params=path_params, query_params=query_params)
                    print_output(result, ctx.obj.get("format", "table"), console=self.console)
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
        @click.pass_context
        def call_operation_impl(ctx, operation: str, path_params: str, query_params: str, body: str):
            """Call an operation on the API."""
            from ecosystems_cli.cli import _call_operation

            _call_operation(self.api_name, operation, path_params, query_params, body, ctx)

        call_operation_impl.__doc__ = f"Call an operation on the {self.api_name} API."
        return self.group.command("call")(call_operation_impl)
