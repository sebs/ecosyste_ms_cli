import click
from rich.console import Console
from rich.panel import Panel

from ecosystems_cli.api_client import get_client
from ecosystems_cli.helpers.print_operations import print_operations
from ecosystems_cli.helpers.print_output import print_output

console = Console()


def _print_output(data, format_type):
    print_output(data, format_type, console=console)


def _print_error(error_msg):
    console.print(Panel(f"[bold red]Error:[/bold red] {error_msg}", border_style="red"))


def _print_operations(operations):
    print_operations(operations, console=console)


@click.group()
def repos():
    """Commands for the repos API."""
    pass


@repos.command("list")
@click.pass_context
def list_repos_operations(ctx):
    """List available operations for repos API."""
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    _print_operations(client.list_operations())


@repos.command("topics")
@click.pass_context
def get_topics(ctx):
    """Get all topics."""
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    result = client.get_topics()
    _print_output(result, ctx.obj.get("format", "table"))


@repos.command("topic")
@click.argument("name")
@click.pass_context
def get_topic(ctx, name: str):
    """Get a specific topic by name."""
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_topic(name)
        _print_output(result, ctx.obj.get("format", "table"))
    except Exception as e:
        _print_error(str(e))


@repos.command("hosts")
@click.pass_context
def get_hosts(ctx):
    """Get all repository hosts."""
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    result = client.get_hosts()
    _print_output(result, ctx.obj.get("format", "table"))


@repos.command("host")
@click.argument("name")
@click.pass_context
def get_host(ctx, name: str):
    """Get a specific repository host by name."""
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
    """Get a specific repository."""
    client = get_client("repos", timeout=ctx.obj.get("timeout", 20))
    try:
        result = client.get_repository(host, owner, repo)
        _print_output(result, ctx.obj.get("format", "table"))
    except Exception as e:
        _print_error(str(e))


@repos.command("call")
@click.argument("operation")
@click.option("--path-params", help="Path parameters as JSON")
@click.option("--query-params", help="Query parameters as JSON")
@click.option("--body", help="Request body as JSON")
@click.pass_context
def call_repos_operation(ctx, operation: str, path_params: str, query_params: str, body: str):
    """Call an operation on the repos API."""
    from ecosystems_cli.cli import _call_operation

    _call_operation("repos", operation, path_params, query_params, body, ctx)
