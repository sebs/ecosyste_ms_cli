"""
Error handling utilities for Ecosyste.ms CLI.
"""
from typing import Any, Callable, Dict, Optional
import sys
import typer


class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(Exception):
    """Exception for input validation errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def handle_api_error(func: Callable) -> Callable:
    """Decorator to handle API exceptions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            typer.echo(f"Error: {e.message}", err=True)
            if e.status_code:
                typer.echo(f"Status code: {e.status_code}", err=True)
            sys.exit(1)
        except ValidationError as e:
            typer.echo(f"Validation Error: {e.message}", err=True)
            sys.exit(1)
        except Exception as e:
            typer.echo(f"Unexpected error: {str(e)}", err=True)
            sys.exit(1)
    return wrapper
