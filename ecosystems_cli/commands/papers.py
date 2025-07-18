"""Commands for the papers API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class PapersCommands(BaseCommand):
    """Commands for the papers API."""

    def __init__(self):
        super().__init__("papers", "Commands for the papers API.")
        self._register_commands()

    def _register_commands(self):
        """Register all commands for the papers API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        @self.create_command_with_error_handling(
            "list-papers",
            "list_papers",
            "List all papers.",
            click.option("--page", type=int, help="Pagination page number"),
            click.option("--per-page", type=int, help="Number of records to return"),
            click.option("--sort", type=str, help="Field to order results by"),
            click.option("--order", type=str, help="Direction to order results by"),
        )
        def list_papers(page: int = None, per_page: int = None, sort: str = None, order: str = None):
            pass

        # Register commands with arguments
        @self.create_command_with_error_handling("get", "get_paper", "Get a paper by DOI.", click.argument("doi"))
        def get_paper(doi: str):
            pass

        @self.create_command_with_error_handling(
            "mentions",
            "get_paper_mentions",
            "List all mentions for a paper.",
            click.argument("doi"),
            click.option("--page", type=int, help="Pagination page number"),
            click.option("--per-page", type=int, help="Number of records to return"),
        )
        def paper_mentions(doi: str, page: int = None, per_page: int = None):
            pass  # Create the command group


papers_base = PapersCommands()

# Export the properly named group
papers = papers_base.group
papers.name = "papers"
