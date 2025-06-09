from typing import Any

from rich.console import Console
from rich.syntax import Syntax

from ecosystems_cli.helpers.format_value import format_value
from ecosystems_cli.helpers.parse_endpoints import flatten_dict


def print_output(data: Any, format_type: str = "table", console: Console = None):
    """Print data in the specified format.

    Args:
        data: The data to print
        format_type: One of 'table', 'json', 'tsv', or 'jsonl'
        console: Optional rich Console instance
    """
    if console is None:
        from rich.console import Console

        console = Console()
    if format_type == "json":
        import json

        json_str = json.dumps(data, indent=2)
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
        console.print(syntax)
    elif format_type == "tsv":
        if isinstance(data, list) and len(data) > 0:
            headers = list(data[0].keys())
            console.print("\t".join(headers))
            for item in data:
                console.print("\t".join(str(format_value(item.get(h, ""))) for h in headers))
        else:
            flat_data = flatten_dict(data) if isinstance(data, dict) else {"value": str(data)}
            console.print("\t".join(flat_data.keys()))
            console.print("\t".join(str(v) for v in flat_data.values()))
    elif format_type == "jsonl":
        import json

        if isinstance(data, list):
            for item in data:
                console.print(json.dumps(item))
        else:
            console.print(json.dumps(data))
    else:  # Default to table
        if isinstance(data, list) and len(data) > 0:
            from rich.table import Table

            headers = list(data[0].keys())
            priority_fields = {
                "common": ["id", "name", "title"],
                "repos": ["full_name", "description", "url", "host"],
                "packages": ["name", "description", "latest_version", "registry"],
                "awesome": ["id", "name", "title", "url"],
                "summary": ["name", "description", "url"],
            }
            api_type = "common"
            for api_name, fields in priority_fields.items():
                if api_name != "common" and any(field in headers for field in fields):
                    api_type = api_name
                    break
            selected_fields = []
            for field in priority_fields[api_type]:
                if field in headers and len(selected_fields) < 2:
                    selected_fields.append(field)
            if len(selected_fields) < 2:
                for field in priority_fields["common"]:
                    if field in headers and field not in selected_fields and len(selected_fields) < 2:
                        selected_fields.append(field)
            if len(selected_fields) < 2:
                for field in headers:
                    if field not in selected_fields and len(selected_fields) < 2:
                        selected_fields.append(field)
            if len(selected_fields) == 1 and len(headers) > 0:
                for field in headers:
                    if field not in selected_fields:
                        selected_fields.append(field)
                        break
            headers = selected_fields
            table = Table(title="API Response", show_header=True, header_style="bold cyan")
            for header in headers:
                table.add_column(header.capitalize())
            for item in data:
                table.add_row(*[format_value(item.get(h, "")) for h in headers])
            console.print(table)
        else:
            if isinstance(data, dict):
                from rich.table import Table

                table = Table(title="API Response", show_header=True, header_style="bold cyan")
                table.add_column("Field")
                table.add_column("Value")
                for key, value in data.items():
                    table.add_row(key, format_value(value))
                console.print(table)
            else:
                import json

                json_str = json.dumps(data, indent=2)
                syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
                console.print(syntax)
