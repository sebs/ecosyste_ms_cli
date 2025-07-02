from typing import Dict, List

from rich.panel import Panel

from ecosystems_cli.constants import (
    AVAILABLE_OPERATIONS_STYLE,
    AVAILABLE_OPERATIONS_TITLE,
    DIVIDER_WIDTH_OFFSET,
    OPERATION_HEADERS,
    OPERATIONS_PANEL_STYLE,
    OPERATIONS_PANEL_TITLE,
    STYLE_BOLD_CYAN,
    STYLE_BOLD_GREEN,
    STYLE_BOLD_MAGENTA,
    STYLE_BOLD_YELLOW,
    STYLE_CYAN,
    STYLE_GREEN,
    STYLE_MAGENTA,
    STYLE_YELLOW,
    SUMMARY_TRUNCATE_LENGTH,
)


def print_operations(operations: List[Dict], console=None):
    """Print operations in a formatted table."""
    if not operations:
        if console:
            console.print(Panel("No operations available.", title=OPERATIONS_PANEL_TITLE, border_style=OPERATIONS_PANEL_STYLE))
        else:
            print("No operations available.")
        return

    # Find the maximum width for each column
    id_width = max(len(op["id"]) for op in operations)
    method_width = max(len(op["method"]) for op in operations)
    path_width = max(len(op["path"]) for op in operations)

    # Create table header
    header = (
        f"[{STYLE_BOLD_CYAN}]{OPERATION_HEADERS['operation'].ljust(id_width)}[/{STYLE_BOLD_CYAN}] | "
        f"[{STYLE_BOLD_GREEN}]{OPERATION_HEADERS['method'].ljust(method_width)}[/{STYLE_BOLD_GREEN}] | "
        f"[{STYLE_BOLD_YELLOW}]{OPERATION_HEADERS['path'].ljust(path_width)}[/{STYLE_BOLD_YELLOW}] | "
        f"[{STYLE_BOLD_MAGENTA}]{OPERATION_HEADERS['description']}[/{STYLE_BOLD_MAGENTA}]"
    )
    divider = "─" * (id_width + method_width + path_width + DIVIDER_WIDTH_OFFSET)

    # Create table rows
    rows = []
    for op in sorted(operations, key=lambda x: x["id"]):
        summary_text = op.get("summary", "")
        if len(summary_text) > SUMMARY_TRUNCATE_LENGTH:
            summary = summary_text[:SUMMARY_TRUNCATE_LENGTH] + "..."
        else:
            summary = summary_text
        row = (
            f"[{STYLE_CYAN}]{op['id'].ljust(id_width)}[/{STYLE_CYAN}] | "
            f"[{STYLE_GREEN}]{op['method'].ljust(method_width)}[/{STYLE_GREEN}] | "
            f"[{STYLE_YELLOW}]{op['path'].ljust(path_width)}[/{STYLE_YELLOW}] | "
            f"[{STYLE_MAGENTA}]{summary}[/{STYLE_MAGENTA}]"
        )
        rows.append(row)

    # Print table
    if console:
        console.print(
            Panel(
                "\n".join([header, divider] + rows),
                title=AVAILABLE_OPERATIONS_TITLE,
                border_style=AVAILABLE_OPERATIONS_STYLE,
            )
        )
    else:
        print("\n".join([header, divider] + rows))
