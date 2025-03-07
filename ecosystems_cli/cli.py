"""Command line interface for ecosystems CLI."""

import json
import sys
from typing import Dict, List, Optional, Any

import click
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from ecosystems_cli.api_client import get_client

console = Console()


@click.group()
@click.option("--timeout", default=20, help="Timeout in seconds for API requests. Default is 20 seconds.")
@click.pass_context
def main(ctx, timeout):
    """Ecosystems CLI for interacting with ecosyste.ms APIs."""
    ctx.ensure_object(dict)
    ctx.obj["timeout"] = timeout


@main.group()
def packages():
    """Commands for the packages API."""
    pass


@main.group()
def repos():
    """Commands for the repos API."""
    pass


@main.group()
def summary():
    """Commands for the summary API."""
    pass


@main.group()
def op():
    """Direct access to API operations with parameters as arguments."""
    pass


@packages.command("list")
@click.pass_context
def list_packages_operations(ctx):
    """List available operations for packages API."""
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    _print_operations(client.list_operations())


@repos.command("list")
@click.pass_context
def list_repos_operations(ctx):
    """List available operations for repos API."""
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    _print_operations(client.list_operations())


@summary.command("list")
@click.pass_context
def list_summary_operations(ctx):
    """List available operations for summary API."""
    client = get_client("summary", timeout=ctx.obj.get("timeout", 20))
    _print_operations(client.list_operations())


# Convenience commands for common operations

# Repos API commands

@repos.command("topics")
@click.pass_context
def get_topics(ctx):
    """Get all topics.

    Example:
        ecosystems repos topics
    """
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    result = client.get_topics()
    _print_json(result)


@repos.command("topic")
@click.argument("name")
@click.pass_context
def get_topic(ctx, name: str):
    """Get a specific topic by name.

    Example:
        ecosystems repos topic javascript
    """
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_topic(name)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


@repos.command("hosts")
@click.pass_context
def get_hosts(ctx):
    """Get all repository hosts.

    Example:
        ecosystems repos hosts
    """
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    result = client.get_hosts()
    _print_json(result)


@repos.command("host")
@click.argument("name")
@click.pass_context
def get_host(ctx, name: str):
    """Get a specific repository host by name.

    Example:
        ecosystems repos host GitHub
    """
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_host(name)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


@repos.command("repository")
@click.argument("host")
@click.argument("owner")
@click.argument("repo")
@click.pass_context
def get_repository(ctx, host: str, owner: str, repo: str):
    """Get a specific repository.

    Example:
        ecosystems repos repository GitHub facebook react
    """
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_repository(host, owner, repo)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


# Packages API commands

@packages.command("registries")
@click.pass_context
def get_registries(ctx):
    """Get all package registries.

    Example:
        ecosystems packages registries
    """
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    result = client.get_registries()
    _print_json(result)


@packages.command("registry")
@click.argument("name")
@click.pass_context
def get_registry(ctx, name: str):
    """Get a specific registry by name.

    Example:
        ecosystems packages registry npm
    """
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_registry(name)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


@packages.command("package")
@click.argument("registry")
@click.argument("package")
@click.pass_context
def get_package(ctx, registry: str, package: str):
    """Get a specific package from a registry.

    Example:
        ecosystems packages package npm express
    """
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_package(registry, package)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


@packages.command("version")
@click.argument("registry")
@click.argument("package")
@click.argument("version")
@click.pass_context
def get_package_version(ctx, registry: str, package: str, version: str):
    """Get a specific package version.

    Example:
        ecosystems packages version npm express 4.17.1
    """
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_package_version(registry, package, version)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


# Summary API commands

@summary.command("repo")
@click.argument("url")
@click.pass_context
def get_repo_summary(ctx, url: str):
    """Get summary for a repository by URL.

    Example:
        ecosystems summary repo https://github.com/facebook/react
    """
    client = get_client("summary", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_repo_summary(url)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


@summary.command("package")
@click.argument("url")
@click.pass_context
def get_package_summary(ctx, url: str):
    """Get summary for a package by URL.

    Example:
        ecosystems summary package https://www.npmjs.com/package/express
    """
    client = get_client("summary", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_package_summary(url)
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


@packages.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
@click.pass_context
def call_packages_operation(ctx, operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the packages API.

    Example:
        ecosystems packages call getRegistry --path-params '{"name": "npm"}'
    """
    _call_operation("packages", operation, path_params, query_params, body, ctx)


@repos.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
@click.pass_context
def call_repos_operation(ctx, operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the repos API.

    Example:
        ecosystems repos call topic --path-params '{"topic": "javascript"}'
    """
    _call_operation("repos", operation, path_params, query_params, body, ctx)


@summary.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
@click.pass_context
def call_summary_operation(ctx, operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the summary API.

    Example:
        ecosystems summary call getRepositorySummary --query-params '{"url": "https://github.com/facebook/react"}'
    """
    _call_operation("summary", operation, path_params, query_params, body, ctx)


def _parse_json_param(param: Optional[str]) -> Optional[Dict]:
    """Parse JSON parameter if provided."""
    if not param:
        return None
    try:
        return json.loads(param)
    except json.JSONDecodeError:
        raise click.BadParameter(f"Invalid JSON: {param}")


def _call_operation(api: str, operation: str, path_params: str, query_params: str, body: str, ctx=None):
    """Call an operation on the specified API."""
    timeout = ctx.obj.get("timeout", 20) if ctx else 20
    client = get_client(api, timeout=timeout)

    # Parse parameters
    path_params_dict = _parse_json_param(path_params)
    query_params_dict = _parse_json_param(query_params)
    body_dict = _parse_json_param(body)

    try:
        result = client.call(
            operation_id=operation,
            path_params=path_params_dict,
            query_params=query_params_dict,
            body=body_dict
        )
        _print_json(result)
    except Exception as e:
        _print_error(str(e))


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
            result = client.call(
                operation_id=operation_id,
                path_params=path_params,
                query_params=query_params
            )
            _print_json(result)
        except Exception as e:
            _print_error(str(e))

    # Set the docstring
    dynamic_command.__doc__ = summary
    if required_params:
        param_docs = [f"\n  {name}: {details.get('description', 'No description')}"
                     for name, details in required_params.items()]
        dynamic_command.__doc__ += "\n\nParameters:" + "".join(param_docs)

    # Create a proper Click command
    return click.command(name=operation_id)(dynamic_command)


def _print_json(data: Any):
    """Print JSON data in a nicely formatted way."""
    json_str = json.dumps(data, indent=2)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    console.print(syntax)

def _print_error(error_msg: str):
    """Print error message in a nicely formatted way."""
    console.print(Panel(f"[bold red]Error:[/bold red] {error_msg}", border_style="red"))

def _print_operations(operations: List[Dict]):
    """Print operations in a formatted table."""
    if not operations:
        console.print(Panel("No operations available.", title="Operations", border_style="yellow"))
        return

    # Find the maximum width for each column
    id_width = max(len(op["id"]) for op in operations)
    method_width = max(len(op["method"]) for op in operations)
    path_width = max(len(op["path"]) for op in operations)

    # Create table header
    header = f"[bold cyan]{'OPERATION'.ljust(id_width)}[/bold cyan] | [bold green]{'METHOD'.ljust(method_width)}[/bold green] | [bold yellow]{'PATH'.ljust(path_width)}[/bold yellow] | [bold magenta]DESCRIPTION[/bold magenta]"
    divider = "─" * (id_width + method_width + path_width + 40)

    # Create table rows
    rows = []
    for op in sorted(operations, key=lambda x: x["id"]):
        summary = op.get("summary", "")[:50] + ("..." if len(op.get("summary", "")) > 50 else "")
        row = f"[cyan]{op['id'].ljust(id_width)}[/cyan] | [green]{op['method'].ljust(method_width)}[/green] | [yellow]{op['path'].ljust(path_width)}[/yellow] | [magenta]{summary}[/magenta]"
        rows.append(row)

    # Print table
    console.print(Panel("\n".join([header, divider] + rows), title="Available Operations", border_style="blue"))


def register_dynamic_commands():
    """Register dynamic commands for all API operations."""
    # Create API clients
    apis = ["packages", "repos", "summary"]
    clients = {api: get_client(api) for api in apis}

    # Create subgroups for each API
    for api_name, client in clients.items():
        # Create a group for this API
        api_group = click.Group(name=api_name, help=f"Operations for {api_name} API")
        op.add_command(api_group)

        # Add commands for each operation
        for operation_id in client.endpoints:
            # Create a dynamic command for this operation
            command = create_dynamic_command(api_name, operation_id, client)
            # Add the command to the API group
            api_group.add_command(command)


# Register dynamic commands
register_dynamic_commands()


if __name__ == "__main__":
    main()
