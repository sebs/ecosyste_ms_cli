from typing import Dict, List

from rich.panel import Panel


def print_operations(operations: List[Dict], console=None):
    """Print operations in a formatted table."""
    if not operations:
        if console:
            console.print(Panel("No operations available.", title="Operations", border_style="yellow"))
        else:
            print("No operations available.")
        return

    # Find the maximum width for each column
    id_width = max(len(op["id"]) for op in operations)
    method_width = max(len(op["method"]) for op in operations)
    path_width = max(len(op["path"]) for op in operations)

    # Create table header
    header = (
        f"[bold cyan]{'OPERATION'.ljust(id_width)}[/bold cyan] | "
        f"[bold green]{'METHOD'.ljust(method_width)}[/bold green] | "
        f"[bold yellow]{'PATH'.ljust(path_width)}[/bold yellow] | "
        f"[bold magenta]DESCRIPTION[/bold magenta]"
    )
    divider = "─" * (id_width + method_width + path_width + 40)

    # Create table rows
    rows = []
    for op in sorted(operations, key=lambda x: x["id"]):
        summary = op.get("summary", "")[:50] + ("..." if len(op.get("summary", "")) > 50 else "")
        row = (
            f"[cyan]{op['id'].ljust(id_width)}[/cyan] | "
            f"[green]{op['method'].ljust(method_width)}[/green] | "
            f"[yellow]{op['path'].ljust(path_width)}[/yellow] | "
            f"[magenta]{summary}[/magenta]"
        )
        rows.append(row)

    # Print table
    if console:
        console.print(Panel("\n".join([header, divider] + rows), title="Available Operations", border_style="blue"))
    else:
        print("\n".join([header, divider] + rows))
