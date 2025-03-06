#!/usr/bin/env python3
"""
Main CLI entry point for Ecosyste.ms CLI.
"""
import typer
from typing import Optional

# Create main Typer app instance
app = typer.Typer(
    name="ecosystems",
    help="Command line interface for Ecosyste.ms APIs",
    add_completion=True,
)

# Import commands
# These will be uncommented as we implement each command group
# from ecosyste_ms_cli.commands import topics
# from ecosyste_ms_cli.commands import repositories
# from ecosyste_ms_cli.commands import packages
# from ecosyste_ms_cli.commands import summary


@app.callback()
def callback():
    """
    Ecosyste.ms CLI - a tool for interacting with Ecosyste.ms APIs.
    """
    pass


@app.command()
def version():
    """
    Print the version of the Ecosyste.ms CLI.
    """
    import ecosyste_ms_cli
    typer.echo(f"Ecosyste.ms CLI version: {ecosyste_ms_cli.__version__}")


def main():
    """
    Main entry point for the CLI.
    """
    app()


if __name__ == "__main__":
    main()
