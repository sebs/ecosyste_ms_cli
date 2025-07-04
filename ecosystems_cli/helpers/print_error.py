from typing import Optional

from rich.console import Console
from rich.panel import Panel

from ecosystems_cli.constants import ERROR_PANEL_STYLE, ERROR_PREFIX


def print_error(error_msg: str, console: Optional[Console] = None) -> None:
    """Print an error message in a formatted panel."""
    if console is None:
        from rich.console import Console

        console = Console()
    console.print(Panel(f"{ERROR_PREFIX} {error_msg}", border_style=ERROR_PANEL_STYLE))
