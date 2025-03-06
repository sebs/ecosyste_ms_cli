"""
Common parameters and options for CLI commands.
"""
from enum import Enum
from typing import Callable, Any
import typer


class OutputFormat(str, Enum):
    """Output format options for CLI commands."""
    JSON = "json"
    CSV = "csv"
    TSV = "tsv"


def common_parameters(func: Callable) -> Callable:
    """Decorator for common CLI parameters."""
    func = typer.Option(
        OutputFormat.JSON, "--format", "-f",
        help="Output format (json, csv, tsv)"
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
