"""
Repository API commands for Ecosyste.ms CLI.
"""
import typer
from typing import Optional

from ..utils.errors import handle_api_error, TopicNotFoundError
from ..utils.output import format_output
from ..commands.common import OutputFormat
from ..clients.repos_client.client import Repositories

# Create command group
app = typer.Typer(
    name="repos",
    help="Commands for working with the Ecosyste.ms Repositories API",
)


@app.callback()
def callback():
    """
    Work with the Ecosyste.ms Repositories API.
    
    Fetch information about code repositories across different
    forges and package managers.
    """
    pass


@app.command("lookup")
@handle_api_error
def lookup_repository(
    url: str = typer.Argument(..., help="Repository URL to look up"),
    output_format: OutputFormat = typer.Option(
        OutputFormat.JSON, "--format", "-f", help="Output format"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Look up repository information by URL.
    
    Example:
        ecosystems repos lookup https://github.com/ecosyste-ms/repos
    """
    # Implementation will be added in Phase 6
    # For now, return a placeholder message
    typer.echo("Repository lookup functionality will be implemented in Phase 6")


@app.command("topics")
@handle_api_error
def list_topics(
    list_all: bool = typer.Option(False, "--list", "-l", help="List all topics"),
    topic: Optional[str] = typer.Option(None, "--topic", "-t", help="Filter by specific topic"),
    sort_by: Optional[str] = typer.Option(None, "--sort-by", "-s", 
                                         help="Sort results by field"),
    order: str = typer.Option("desc", "--order", "-o", 
                             help="Sort order (asc or desc)"),
    min_repos: Optional[int] = typer.Option(None, "--min-repos", 
                                           help="Minimum number of repositories"),
    output_format: OutputFormat = typer.Option(
        OutputFormat.JSON, "--format", "-f", help="Output format"
    ),
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    per_page: int = typer.Option(30, "--per-page", "-n", help="Items per page"),
    max_items: Optional[int] = typer.Option(None, "--max-items", "-m", 
                                          help="Maximum number of items to return"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Bypass cache"),
):
    """
    List or search repository topics.
    
    Examples:
        # List all topics
        ecosystems repos topics --list
        
        # Get repositories for a specific topic
        ecosystems repos topics --topic python
        
        # List topics with at least 100 repositories
        ecosystems repos topics --list --min-repos 100
        
        # Sort topics by repository count
        ecosystems repos topics --list --sort-by repositories_count --order desc
    """
    from ..utils.logging import get_logger
    from ..utils.pagination import paginate
    from ..utils.cache import get_cache
    from ..utils.data import sort_items
    from ..clients.repos.api.default_api import DefaultApi
    from ..clients.repos.configuration import Configuration
    
    logger = get_logger(verbose=verbose)
    cache = get_cache()
    
    # Handle list topics case
    if list_all and not topic:
        logger.info("Fetching topics list")
        
        # Define a function to be used with pagination
        def fetch_topics(page, per_page):
            logger.debug(f"Fetching page {page} with {per_page} items per page")
            try:
                with Repositories() as client:
                    return client.get_topics(page=page, per_page=per_page)
            except Exception as e:
                logger.error(f"Error fetching topics: {str(e)}")
                return []
        
        # Use pagination utility
        items = []
        for item in paginate(
            fetch_topics, 
            page=page, 
            per_page=per_page, 
            max_items=max_items,
            verbose=verbose
        ):
            # Apply any filtering based on min_repos if provided
            if min_repos is not None and item.get("repositories_count", 0) < min_repos:
                continue
                
            items.append(item)
            
        # Sort results if requested
        if sort_by:
            items = sort_items(items, sort_by, order)
            
        # Format and output the results
        output = format_output(items, output_format)
        typer.echo(output)
        return

    # Handle specific topic search case
    if topic:
        logger.info(f"Fetching repositories for topic: {topic}")
        
        try:
            # Define function for pagination
            def fetch_topic_repos(page, per_page):
                logger.debug(f"Fetching page {page} with {per_page} items per page")
                with Repositories() as client:
                    return client.get_repositories_by_topic(topic=topic, page=page, per_page=per_page)
                    
            # Use pagination utility
            items = []
            for item in paginate(
                fetch_topic_repos,
                page=page,
                per_page=per_page,
                max_items=max_items,
                verbose=verbose
            ):
                items.append(item)
                
            # Sort if requested
            if sort_by:
                items = sort_items(items, sort_by, order)
                
            # Format and output
            output = format_output(items, output_format)
            typer.echo(output)
            return
            
        except TopicNotFoundError:
            typer.echo(f"Error: Topic '{topic}' not found")
            raise typer.Exit(1)
        
    # If neither list nor topic is provided, show help
    typer.echo("Error: Please specify --list to see all topics or --topic to search for a specific topic")
    raise typer.Exit(1)
