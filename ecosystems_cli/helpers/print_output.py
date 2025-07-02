from typing import Any

from rich.console import Console
from rich.syntax import Syntax

from ecosystems_cli.constants import (
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_TABLE_TITLE,
    JSON_SYNTAX,
    JSON_THEME,
    MAX_SELECTED_FIELDS,
    PRIORITY_FIELDS,
    TABLE_HEADER_STYLE,
)
from ecosystems_cli.helpers.format_value import format_value
from ecosystems_cli.helpers.parse_endpoints import flatten_dict


def _format_json(data: Any, console: Console) -> None:
    """Format and print data as JSON."""
    import json

    json_str = json.dumps(data, indent=2)
    syntax = Syntax(json_str, JSON_SYNTAX, theme=JSON_THEME, line_numbers=False)
    console.print(syntax)


def _format_tsv(data: Any, console: Console) -> None:
    """Format and print data as TSV (Tab-Separated Values)."""
    if isinstance(data, list) and len(data) > 0:
        headers = list(data[0].keys())
        console.print("\t".join(headers))
        for item in data:
            console.print("\t".join(str(format_value(item.get(h, ""))) for h in headers))
    else:
        flat_data = flatten_dict(data) if isinstance(data, dict) else {"value": str(data)}
        console.print("\t".join(flat_data.keys()))
        console.print("\t".join(str(v) for v in flat_data.values()))


def _format_jsonl(data: Any, console: Console) -> None:
    """Format and print data as JSONL (JSON Lines)."""
    import json

    if isinstance(data, list):
        for item in data:
            console.print(json.dumps(item))
    else:
        console.print(json.dumps(data))


def _select_table_fields(headers: list[str]) -> list[str]:
    """Select which fields to display in the table based on priority."""
    from typing import List

    priority_fields = PRIORITY_FIELDS.copy()
    priority_fields["common"] = ["id", "name", "title"]

    # Determine API type based on available headers
    api_type = "common"
    for api_name, fields in priority_fields.items():
        if api_name != "common" and any(field in headers for field in fields):
            api_type = api_name
            break

    # Select fields based on priority
    selected_fields: List[str] = []

    # First, add priority fields for the detected API type
    for field in priority_fields[api_type]:
        if field in headers and len(selected_fields) < MAX_SELECTED_FIELDS:
            selected_fields.append(field)

    # If we have less than 2 fields, add common fields
    if len(selected_fields) < 2:
        for field in priority_fields["common"]:
            if field in headers and field not in selected_fields and len(selected_fields) < MAX_SELECTED_FIELDS:
                selected_fields.append(field)

    # If still less than 2 fields, add any remaining headers
    if len(selected_fields) < 2:
        for field in headers:
            if field not in selected_fields and len(selected_fields) < MAX_SELECTED_FIELDS:
                selected_fields.append(field)

    # Ensure we have at least 2 fields if possible
    if len(selected_fields) == 1 and len(headers) > 0:
        for field in headers:
            if field not in selected_fields:
                selected_fields.append(field)
                break

    return selected_fields


def _format_table(data: Any, console: Console) -> None:
    """Format and print data as a rich table."""
    from rich.table import Table

    if isinstance(data, list) and len(data) > 0:
        # Select fields to display
        headers = list(data[0].keys())
        selected_headers = _select_table_fields(headers)

        # Create and populate table
        table = Table(title=DEFAULT_TABLE_TITLE, show_header=True, header_style=TABLE_HEADER_STYLE)
        for header in selected_headers:
            table.add_column(header.capitalize())

        for item in data:
            table.add_row(*[format_value(item.get(h, "")) for h in selected_headers])

        console.print(table)
    elif isinstance(data, dict):
        # Create a key-value table for dict data
        table = Table(title=DEFAULT_TABLE_TITLE, show_header=True, header_style=TABLE_HEADER_STYLE)
        table.add_column("Field")
        table.add_column("Value")

        for key, value in data.items():
            table.add_row(key, format_value(value))

        console.print(table)
    else:
        # Fall back to JSON for other data types
        _format_json(data, console)


# Formatter registry
_FORMATTERS = {
    "json": _format_json,
    "tsv": _format_tsv,
    "jsonl": _format_jsonl,
    "table": _format_table,
}


def print_output(data: Any, format_type: str = DEFAULT_OUTPUT_FORMAT, console: Console = None):
    """Print data in the specified format.

    Args:
        data: The data to print
        format_type: One of 'table', 'json', 'tsv', or 'jsonl'
        console: Optional rich Console instance
    """
    if console is None:
        from rich.console import Console

        console = Console()

    # Get the formatter function from the registry
    formatter = _FORMATTERS.get(format_type, _format_table)
    formatter(data, console)
