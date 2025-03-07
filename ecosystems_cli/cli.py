"""Command line interface for ecosystems CLI."""

import json
from typing import Dict, List, Optional

import click
from ecosystems_cli.api_client import get_client


@click.group()
def main():
    """Ecosystems CLI for interacting with ecosyste.ms APIs."""
    pass


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
def list_packages_operations():
    """List available operations for packages API."""
    client = get_client("packages")
    _print_operations(client.list_operations())


@repos.command("list")
def list_repos_operations():
    """List available operations for repos API."""
    client = get_client("repos")
    _print_operations(client.list_operations())


@summary.command("list")
def list_summary_operations():
    """List available operations for summary API."""
    client = get_client("summary")
    _print_operations(client.list_operations())


# Convenience commands for common operations

# Repos API commands

@repos.command("topics")
def get_topics():
    """Get all topics.
    
    Example:
        ecosystems repos topics
    """
    client = get_client("repos")
    result = client.get_topics()
    click.echo(json.dumps(result, indent=2))


@repos.command("topic")
@click.argument("name")
def get_topic(name: str):
    """Get a specific topic by name.
    
    Example:
        ecosystems repos topic javascript
    """
    client = get_client("repos")
    try:
        result = client.get_topic(name)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@repos.command("hosts")
def get_hosts():
    """Get all repository hosts.
    
    Example:
        ecosystems repos hosts
    """
    client = get_client("repos")
    result = client.get_hosts()
    click.echo(json.dumps(result, indent=2))


@repos.command("host")
@click.argument("name")
def get_host(name: str):
    """Get a specific repository host by name.
    
    Example:
        ecosystems repos host GitHub
    """
    client = get_client("repos")
    try:
        result = client.get_host(name)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@repos.command("repository")
@click.argument("host")
@click.argument("owner")
@click.argument("repo")
def get_repository(host: str, owner: str, repo: str):
    """Get a specific repository.
    
    Example:
        ecosystems repos repository GitHub facebook react
    """
    client = get_client("repos")
    try:
        result = client.get_repository(host, owner, repo)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


# Packages API commands

@packages.command("registries")
def get_registries():
    """Get all package registries.
    
    Example:
        ecosystems packages registries
    """
    client = get_client("packages")
    result = client.get_registries()
    click.echo(json.dumps(result, indent=2))


@packages.command("registry")
@click.argument("name")
def get_registry(name: str):
    """Get a specific registry by name.
    
    Example:
        ecosystems packages registry npm
    """
    client = get_client("packages")
    try:
        result = client.get_registry(name)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@packages.command("package")
@click.argument("registry")
@click.argument("package")
def get_package(registry: str, package: str):
    """Get a specific package from a registry.
    
    Example:
        ecosystems packages package npm express
    """
    client = get_client("packages")
    try:
        result = client.get_package(registry, package)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@packages.command("version")
@click.argument("registry")
@click.argument("package")
@click.argument("version")
def get_package_version(registry: str, package: str, version: str):
    """Get a specific package version.
    
    Example:
        ecosystems packages version npm express 4.17.1
    """
    client = get_client("packages")
    try:
        result = client.get_package_version(registry, package, version)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


# Summary API commands

@summary.command("repo")
@click.argument("url")
def get_repo_summary(url: str):
    """Get summary for a repository by URL.
    
    Example:
        ecosystems summary repo https://github.com/facebook/react
    """
    client = get_client("summary")
    try:
        result = client.get_repo_summary(url)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@summary.command("package")
@click.argument("url")
def get_package_summary(url: str):
    """Get summary for a package by URL.
    
    Example:
        ecosystems summary package https://www.npmjs.com/package/express
    """
    client = get_client("summary")
    try:
        result = client.get_package_summary(url)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@packages.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
def call_packages_operation(operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the packages API.
    
    Example:
        ecosystems packages call getRegistry --path-params '{"name": "npm"}'
    """
    _call_operation("packages", operation, path_params, query_params, body)


@repos.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
def call_repos_operation(operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the repos API.
    
    Example:
        ecosystems repos call topic --path-params '{"topic": "javascript"}'
    """
    _call_operation("repos", operation, path_params, query_params, body)


@summary.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
def call_summary_operation(operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the summary API.
    
    Example:
        ecosystems summary call getRepositorySummary --query-params '{"url": "https://github.com/facebook/react"}'
    """
    _call_operation("summary", operation, path_params, query_params, body)


def _parse_json_param(param: Optional[str]) -> Optional[Dict]:
    """Parse JSON parameter if provided."""
    if not param:
        return None
    try:
        return json.loads(param)
    except json.JSONDecodeError:
        raise click.BadParameter(f"Invalid JSON: {param}")


def _call_operation(api: str, operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the specified API."""
    client = get_client(api)
    
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
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


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
            click.echo(json.dumps(result, indent=2))
        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)
    
    # Set the docstring
    dynamic_command.__doc__ = summary
    if required_params:
        param_docs = [f"\n  {name}: {details.get('description', 'No description')}" 
                     for name, details in required_params.items()]
        dynamic_command.__doc__ += "\n\nParameters:" + "".join(param_docs)
    
    # Create a proper Click command
    return click.command(name=operation_id)(dynamic_command)


def _print_operations(operations: List[Dict]):
    """Print operations in a formatted table."""
    if not operations:
        click.echo("No operations available.")
        return
    
    # Find the maximum width for each column
    id_width = max(len(op["id"]) for op in operations)
    method_width = max(len(op["method"]) for op in operations)
    path_width = max(len(op["path"]) for op in operations)
    
    # Print header
    click.echo(f"{'OPERATION'.ljust(id_width)} | {'METHOD'.ljust(method_width)} | {'PATH'.ljust(path_width)} | DESCRIPTION")
    click.echo("-" * (id_width + method_width + path_width + 40))
    
    # Print operations
    for op in sorted(operations, key=lambda x: x["id"]):
        summary = op.get("summary", "")[:50] + ("..." if len(op.get("summary", "")) > 50 else "")
        click.echo(f"{op['id'].ljust(id_width)} | {op['method'].ljust(method_width)} | {op['path'].ljust(path_width)} | {summary}")


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
