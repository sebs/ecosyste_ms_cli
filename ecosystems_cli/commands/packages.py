import click
from rich.console import Console

from ecosystems_cli.api_client import get_client
from ecosystems_cli.helpers.print_error import print_error
from ecosystems_cli.helpers.print_operations import print_operations
from ecosystems_cli.helpers.print_output import print_output

console = Console()


@click.group()
def packages():
    """Commands for the packages API."""
    pass


@packages.command("list")
@click.pass_context
def list_packages_operations(ctx):
    """List available operations for packages API."""
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    print_operations(client.list_operations(), console=console)


@packages.command("registries")
@click.pass_context
def get_registries(ctx):
    """Get all package registries."""
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    result = client.get_registries()
    print_output(result, ctx.obj.get("format", "table"), console=console)


@packages.command("registry")
@click.argument("name")
@click.pass_context
def get_registry(ctx, name: str):
    """Get a specific registry by name."""
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_registry(name)
        print_output(result, ctx.obj.get("format", "table"), console=console)
    except Exception as e:
        print_error(str(e), console=console)


@packages.command("package")
@click.argument("registry")
@click.argument("package")
@click.pass_context
def get_package(ctx, registry: str, package: str):
    """Get a specific package from a registry."""
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_package(registry, package)
        print_output(result, ctx.obj.get("format", "table"), console=console)
    except Exception as e:
        print_error(str(e), console=console)


@packages.command("version")
@click.argument("registry")
@click.argument("package")
@click.argument("version")
@click.pass_context
def get_package_version(ctx, registry: str, package: str, version: str):
    """Get a specific package version."""
    client = get_client("packages", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_package_version(registry, package, version)
        print_output(result, ctx.obj.get("format", "table"), console=console)
    except Exception as e:
        print_error(str(e), console=console)


@packages.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
@click.pass_context
def call_packages_operation(ctx, operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the packages API."""
    from ecosystems_cli.cli import _call_operation

    _call_operation("packages", operation, path_params, query_params, body, ctx)
