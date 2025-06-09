"""Command line interface for ecosystems CLI."""

import json
from typing import Any, Dict, List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from ecosystems_cli.api_client import get_client
from ecosystems_cli.helpers.format_value import format_value
from ecosystems_cli.helpers.parse_endpoints import flatten_dict
from ecosystems_cli.helpers.print_operations import print_operations

console = Console()


@click.group()
@click.option("--timeout", default=20, help="Timeout in seconds for API requests. Default is 20 seconds.")
@click.option(
    "--format", default="table", type=click.Choice(["table", "json", "tsv", "jsonl"]), help="Output format. Default is table."
)
@click.pass_context
def main(ctx, timeout, format):
    """Ecosystems CLI for interacting with ecosyste.ms APIs."""
    ctx.ensure_object(dict)
    ctx.obj["timeout"] = timeout
    ctx.obj["format"] = format


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
def awesome():
    """Commands for the awesome API."""
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
    _print_output(result, ctx.obj.get("format", "table"))


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
        _print_output(result, ctx.obj.get("format", "table"))
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
    _print_output(result, ctx.obj.get("format", "table"))


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
        _print_output(result, ctx.obj.get("format", "table"))
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
        _print_output(result, ctx.obj.get("format", "table"))
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
    _print_output(result, ctx.obj.get("format", "table"))


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
        _print_output(result, ctx.obj.get("format", "table"))
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
        _print_output(result, ctx.obj.get("format", "table"))
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
        _print_output(result, ctx.obj.get("format", "table"))
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
        _print_output(result, ctx.obj.get("format", "table"))
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
        _print_output(result, ctx.obj.get("format", "table"))
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


@awesome.command("projects")
@click.pass_context
def get_projects(ctx):
    """Get all projects.

    Example:
        ecosystems awesome projects
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    result = client.call("getProjects")
    _print_output(result, ctx.obj.get("format", "table"))


@awesome.command("project")
@click.argument("id")
@click.pass_context
def get_project(ctx, id: str):
    """Get a specific project by ID.

    Example:
        ecosystems awesome project 123
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.call("getProject", path_params={"id": id})
        _print_output(result, ctx.obj.get("format", "table"))
    except Exception as e:
        _print_error(str(e))


@awesome.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
@click.pass_context
def call_awesome_operation(ctx, operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the awesome API.

    Example:
        ecosystems awesome call getProject --path-params '{"id": "123"}'
    """
    _call_operation("awesome", operation, path_params, query_params, body, ctx)


@awesome.command("lists")
@click.pass_context
def get_lists(ctx):
    """Get all lists.

    Example:
        ecosystems awesome lists
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    result = client.call("getLists")
    _print_output(result, ctx.obj.get("format", "table"))


@awesome.command("list")
@click.argument("id")
@click.pass_context
def get_list(ctx, id: str):
    """Get a specific list by ID.

    Example:
        ecosystems awesome list 123
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.call("getList", path_params={"id": id})
        _print_output(result, ctx.obj.get("format", "table"))
    except Exception as e:
        _print_error(str(e))


@awesome.command("list-projects")
@click.argument("id")
@click.pass_context
def get_list_projects(ctx, id: str):
    """Get projects in a specific list.

    Example:
        ecosystems awesome list-projects 123
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.call("getListProjects", path_params={"id": id})
        _print_output(result, ctx.obj.get("format", "table"))
    except Exception as e:
        _print_error(str(e))


@awesome.command("topics")
@click.pass_context
def get_awesome_topics(ctx):
    """Get all topics.

    Example:
        ecosystems awesome topics
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    result = client.call("getTopics")
    _print_output(result, ctx.obj.get("format", "table"))


@awesome.command("topic")
@click.argument("slug")
@click.pass_context
def get_awesome_topic(ctx, slug: str):
    """Get a specific topic by slug.

    Example:
        ecosystems awesome topic javascript
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.call("getTopic", path_params={"slug": slug})
        _print_output(result, ctx.obj.get("format", "table"))
    except Exception as e:
        _print_error(str(e))


@awesome.command("operations")
@click.pass_context
def list_awesome_operations(ctx):
    """List available operations for the awesome API.

    Example:
        ecosystems awesome operations
    """
    client = get_client("awesome", timeout=ctx.obj.get("timeout", 20))
    _print_operations(client.list_operations())


def _parse_json_param(param: Optional[str]) -> Optional[Dict]:
    """Parse JSON parameter if provided."""
    if not param:
        return None
    try:
        return json.loads(param)
    except json.JSONDecodeError:
        raise click.BadParameter(f"Invalid JSON: {param}")


def _call_operation(api: str, operation: str, path_params: str, query_params: str, body: str, context=None):
    """Call an operation on the specified API."""
    # Get timeout and format from context if available
    if context and hasattr(context, "obj"):
        timeout = context.obj.get("timeout", 20)
        format_type = context.obj.get("format", "table")
    else:
        timeout = 20
        format_type = "table"
    client = get_client(api, timeout=timeout)

    # Parse parameters
    path_params_dict = _parse_json_param(path_params)
    query_params_dict = _parse_json_param(query_params)
    body_dict = _parse_json_param(body)

    try:
        result = client.call(
            operation_id=operation, path_params=path_params_dict, query_params=query_params_dict, body=body_dict
        )
        _print_output(result, format_type)
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
            result = client.call(operation_id=operation_id, path_params=path_params, query_params=query_params)
            # Default to table format
            _print_output(result, "table")
        except Exception as e:
            _print_error(str(e))

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
    """Print data in the specified format.

    Args:
        data: The data to print
        format_type: One of 'table', 'json', 'tsv', or 'jsonl'
    """
    if format_type == "json":
        json_str = json.dumps(data, indent=2)
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
        console.print(syntax)
    elif format_type == "tsv":
        if isinstance(data, list) and len(data) > 0:
            # Get headers from first item
            headers = list(data[0].keys())
            # Print headers
            console.print("\t".join(headers))
            # Print rows
            for item in data:
                console.print("\t".join(str(_format_value(item.get(h, ""))) for h in headers))
        else:
            # For non-list data, convert to flat dictionary
            flat_data = flatten_dict(data) if isinstance(data, dict) else {"value": str(data)}
            console.print("\t".join(flat_data.keys()))
            console.print("\t".join(str(v) for v in flat_data.values()))
    elif format_type == "jsonl":
        if isinstance(data, list):
            for item in data:
                console.print(json.dumps(item))
        else:
            console.print(json.dumps(data))
    else:  # Default to table
        if isinstance(data, list) and len(data) > 0:
            from rich.table import Table

            # Get headers from first item
            headers = list(data[0].keys())

            # Show only 2 columns by default for table format
            # Choose the most important fields based on the API response

            # Define priority fields for different APIs
            priority_fields = {
                # Common priority fields across all APIs
                "common": ["id", "name", "title"],
                # Fields specific to repos API
                "repos": ["full_name", "description", "url", "host"],
                # Fields specific to packages API
                "packages": ["name", "description", "latest_version", "registry"],
                # Fields specific to awesome API
                "awesome": ["id", "name", "title", "url"],
                # Fields specific to summary API
                "summary": ["name", "description", "url"],
            }

            # Determine which API we're dealing with based on the fields
            api_type = "common"
            for api_name, fields in priority_fields.items():
                if api_name != "common" and any(field in headers for field in fields):
                    api_type = api_name
                    break

            # Always select exactly 2 columns
            selected_fields = []

            # First try the API-specific priority fields
            for field in priority_fields[api_type]:
                if field in headers and len(selected_fields) < 2:
                    selected_fields.append(field)

            # If we still need more fields, try common fields
            if len(selected_fields) < 2:
                for field in priority_fields["common"]:
                    if field in headers and field not in selected_fields and len(selected_fields) < 2:
                        selected_fields.append(field)

            # If we still need more fields, add any remaining fields
            if len(selected_fields) < 2:
                for field in headers:
                    if field not in selected_fields and len(selected_fields) < 2:
                        selected_fields.append(field)

            # Ensure we have exactly 2 fields if possible
            if len(selected_fields) == 1 and len(headers) > 0:
                # If we only have one field but more are available, add another
                for field in headers:
                    if field not in selected_fields:
                        selected_fields.append(field)
                        break

            headers = selected_fields

            table = Table(title="API Response", show_header=True, header_style="bold cyan")

            # Add columns
            for header in headers:
                table.add_column(header.capitalize())

            # Add rows
            for item in data:
                table.add_row(*[_format_value(item.get(h, "")) for h in headers])

            console.print(table)
        else:
            # For non-list data, create a table with key-value pairs
            if isinstance(data, dict):
                from rich.table import Table

                table = Table(title="API Response", show_header=True, header_style="bold cyan")
                table.add_column("Field")
                table.add_column("Value")

                # Add rows for each key-value pair
                for key, value in data.items():
                    table.add_row(key, _format_value(value))

                console.print(table)
            else:
                # Fall back to JSON format for non-dict data
                json_str = json.dumps(data, indent=2)
                syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
                console.print(syntax)


def _format_value(value: Any) -> str:
    """Deprecated: use format_value from helpers.format_value instead."""
    return format_value(value)


def _print_json(data: Any):
    """Print JSON data in a nicely formatted way."""
    _print_output(data, "json")


def _print_error(error_msg: str):
    """Print error message in a nicely formatted way."""
    console.print(Panel(f"[bold red]Error:[/bold red] {error_msg}", border_style="red"))


def _print_operations(operations: List[Dict]):
    print_operations(operations, console=console)
