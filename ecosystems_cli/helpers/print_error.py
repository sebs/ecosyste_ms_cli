from rich.console import Console
from rich.panel import Panel


def print_error(error_msg: str, console: Console = None):
    """Print an error message in a formatted panel."""
    if console is None:
        from rich.console import Console

        console = Console()
    console.print(Panel(f"[bold red]Error:[/bold red] {error_msg}", border_style="red"))
