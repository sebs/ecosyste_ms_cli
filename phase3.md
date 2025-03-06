# Phase 3: CLI Framework Implementation

## Architecture Overview

### Command Structure
- Main Typer app in `main.py` (already implemented)
- Command groups in separate modules:
  - `commands/repos.py` - Repository API commands
  - `commands/packages.py` - Packages API commands
  - `commands/summary.py` - Summary API commands
  - `commands/common.py` - Shared parameters and options

### Utility Modules
- `utils/errors.py` - Error handling framework
- `utils/output.py` - Output formatting utilities

## Implementation Details

### 1. Command Group Structure
```python
# Example structure for a command module (commands/repos.py)
import typer
from typing import Optional
from enum import Enum
from ..utils.errors import handle_api_error
from ..utils.output import format_output

# Create command group
app = typer.Typer(name="repos", help="Repository API commands")

# Commands will be implemented here
```

### 2. Common CLI Options
```python
# commands/common.py
from enum import Enum
from typing import Optional
import typer

class OutputFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    TSV = "tsv"

def common_parameters(func):
    """Decorator for common CLI parameters"""
    func = typer.Option(
        OutputFormat.JSON, "--format", "-f", 
        help="Output format"
    )(func)
    func = typer.Option(
        1, "--page", "-p", 
        help="Page number for paginated results"
    )(func)
    func = typer.Option(
        30, "--per-page", "-n", 
        help="Number of items per page"
    )(func)
    func = typer.Option(
        False, "--verbose", "-v", 
        help="Enable verbose output"
    )(func)
    return func
```

### 3. Error Handling Framework
```python
# utils/errors.py
from typing import Any, Dict, Optional
import typer
import sys

class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def handle_api_error(func):
    """Decorator to handle API exceptions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            typer.echo(f"Error: {e.message}", err=True)
            if e.status_code:
                typer.echo(f"Status code: {e.status_code}", err=True)
            sys.exit(1)
        except Exception as e:
            typer.echo(f"Unexpected error: {str(e)}", err=True)
            sys.exit(1)
    return wrapper
```

### 4. Output Formatting
```python
# utils/output.py
import json
import csv
import io
from typing import Any, Dict, List, Union
from ..commands.common import OutputFormat

def format_output(data: Union[Dict[str, Any], List[Dict[str, Any]]], 
                  output_format: OutputFormat) -> str:
    """Format data according to specified output format"""
    if output_format == OutputFormat.JSON:
        return json.dumps(data, indent=2)
    elif output_format in (OutputFormat.CSV, OutputFormat.TSV):
        delimiter = "," if output_format == OutputFormat.CSV else "\t"
        # Handle both single item and list of items
        items = data if isinstance(data, list) else [data]
        if not items:
            return ""
        
        output = io.StringIO()
        writer = csv.DictWriter(
            output, 
            fieldnames=items[0].keys(),
            delimiter=delimiter
        )
        writer.writeheader()
        writer.writerows(items)
        return output.getvalue()
    else:
        return str(data)
```

## Main App Integration
```python
# Excerpt from main.py
from ecosyste_ms_cli.commands import repos, packages, summary

# Add command groups to main app
app.add_typer(repos.app, name="repos")
app.add_typer(packages.app, name="packages")
app.add_typer(summary.app, name="summary")
```

## Next Steps
1. Implement skeleton command modules for each API
2. Connect command groups to main app
3. Test help system and parameter validation
4. Prepare for Phase 4 implementation
