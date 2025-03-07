# Phase 5: Topics Command Implementation

## Architecture Overview

### Command Structure
- `commands/repos.py` - Implementation of topics commands within the repositories module
- Integration with existing command framework from Phase 3
- Utilization of utility modules from Phase 4

### Key Components
- Topics listing functionality
- Topic-specific repository filtering
- Output formatting with multiple formats
- Sorting and pagination options

## Implementation Details

### 1. Topics List Command
```python
# commands/repos.py - add topics commands

@app.command("topics")
@handle_api_error
@common_parameters
def list_topics(
    list: bool = typer.Option(False, "--list", "-l", help="List all topics"),
    topic: Optional[str] = typer.Option(None, "--topic", "-t", help="Filter by specific topic"),
    sort_by: Optional[str] = typer.Option(None, "--sort-by", "-s", 
                                         help="Sort results by field"),
    order: str = typer.Option("desc", "--order", "-o", 
                             help="Sort order (asc or desc)"),
    min_repos: Optional[int] = typer.Option(None, "--min-repos", 
                                           help="Minimum number of repositories"),
    format: OutputFormat = OutputFormat.JSON,
    page: int = 1,
    per_page: int = 30,
    max_items: Optional[int] = None,
    verbose: bool = False,
    no_cache: bool = False
):
    """
    List or search repository topics
    """
    logger = get_logger(verbose=verbose)
    cache = get_cache()
    
    # Handle list topics case
    if list and not topic:
        logger.info("Fetching topics list")
        
        # Define a function to be used with pagination
        def fetch_topics(page, per_page):
            logger.debug(f"Fetching page {page} with {per_page} items per page")
            # Call the appropriate API endpoint with pagination
            with Repositories() as api:
                # Get topics list with pagination
                response = api.get_topics(page=page, per_page=per_page)
                return response
                
        # Use pagination utility from Phase 4
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
        output = format_output(items, format)
        typer.echo(output)
        return

    # Handle specific topic search case
    if topic:
        logger.info(f"Fetching repositories for topic: {topic}")
        
        # Define function for pagination
        def fetch_topic_repos(page, per_page):
            logger.debug(f"Fetching page {page} with {per_page} items per page")
            # Call API to get repositories for specific topic
            with Repositories() as api:
                response = api.get_repositories_by_topic(
                    topic=topic,
                    page=page,
                    per_page=per_page
                )
                return response
                
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
        output = format_output(items, format)
        typer.echo(output)
        return
        
    # If neither list nor topic is provided, show help
    typer.echo("Error: Please specify --list to see all topics or --topic to search for a specific topic")
    raise typer.Exit(1)
```

### 2. Sorting Functionality
```python
# utils/data.py - add sorting utility
from typing import List, Dict, Any, Optional

def sort_items(
    items: List[Dict[str, Any]], 
    sort_by: str, 
    order: str = "desc"
) -> List[Dict[str, Any]]:
    """
    Sort a list of dictionaries by the specified field.
    
    Args:
        items: List of dictionaries to sort
        sort_by: Key to sort by
        order: "asc" for ascending, "desc" for descending
    
    Returns:
        Sorted list of dictionaries
    """
    reverse = order.lower() == "desc"
    
    # Helper function to extract the sort key, handling nested paths
    def get_sort_key(item):
        if "." in sort_by:
            # Handle nested keys like "stats.stars"
            parts = sort_by.split(".")
            value = item
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return None
            return value
        return item.get(sort_by)
    
    # Sort the items
    return sorted(items, key=get_sort_key, reverse=reverse)
```

### 3. Enhanced Error Handling for Topics
```python
# utils/errors.py - add topic-specific error handling
class TopicNotFoundError(APIError):
    """Exception for when a topic cannot be found"""
    def __init__(self, topic: str):
        super().__init__(f"Topic '{topic}' not found", status_code=404)

# In commands/repos.py, enhance error handling
def fetch_topic_repos(page, per_page):
    try:
        with Repositories() as api:
            response = api.get_repositories_by_topic(
                topic=topic,
                page=page,
                per_page=per_page
            )
            return response
    except Exception as e:
        if "404" in str(e):
            raise TopicNotFoundError(topic)
        raise e
```

### 4. Integration with Main CLI
```python
# main.py - ensure topics command is registered
from ecosyste_ms_cli.commands.repos import app as repos_app

app = typer.Typer()
app.add_typer(repos_app, name="repos")

# Make sure the help text is updated to show topics functionality
repos_app.help = "Repository API commands including topics functionality"
```

## Testing Approach

### Unit Tests for Topics Commands
```python
# tests/commands/test_repos.py
import pytest
from typer.testing import CliRunner
from ecosyste_ms_cli.main import app
from unittest.mock import patch, MagicMock

runner = CliRunner()

class TestTopicsCommands:
    @patch("ecosyste_ms_cli.commands.repos.Repositories")
    def test_list_topics(self, mock_api):
        # Mock API response
        mock_instance = MagicMock()
        mock_api.return_value.__enter__.return_value = mock_instance
        mock_instance.get_topics.return_value = [
            {"name": "python", "repositories_count": 5000},
            {"name": "javascript", "repositories_count": 8000},
        ]
        
        # Run command
        result = runner.invoke(app, ["repos", "topics", "--list"])
        
        # Check output
        assert result.exit_code == 0
        assert "python" in result.stdout
        assert "javascript" in result.stdout
        
    @patch("ecosyste_ms_cli.commands.repos.Repositories")
    def test_topic_search(self, mock_api):
        # Mock API response
        mock_instance = MagicMock()
        mock_api.return_value.__enter__.return_value = mock_instance
        mock_instance.get_repositories_by_topic.return_value = [
            {"name": "repo1", "url": "https://github.com/user/repo1"},
            {"name": "repo2", "url": "https://github.com/user/repo2"},
        ]
        
        # Run command
        result = runner.invoke(app, ["repos", "topics", "--topic", "python"])
        
        # Check output
        assert result.exit_code == 0
        assert "repo1" in result.stdout
        assert "repo2" in result.stdout
        
    @patch("ecosyste_ms_cli.commands.repos.Repositories")
    def test_topic_not_found(self, mock_api):
        # Mock API error response
        mock_instance = MagicMock()
        mock_api.return_value.__enter__.return_value = mock_instance
        mock_instance.get_repositories_by_topic.side_effect = Exception("404 Not Found")
        
        # Run command
        result = runner.invoke(app, ["repos", "topics", "--topic", "nonexistent"])
        
        # Check output
        assert result.exit_code == 1
        assert "not found" in result.stdout
```

### Testing Sorting and Filtering
```python
# tests/utils/test_data.py - add tests for sort_items
def test_sort_items_basic():
    # Arrange
    items = [
        {"name": "B", "count": 5},
        {"name": "A", "count": 10},
        {"name": "C", "count": 2}
    ]
    
    # Act - sort by name ascending
    result = sort_items(items, "name", "asc")
    
    # Assert
    assert result[0]["name"] == "A"
    assert result[1]["name"] == "B"
    assert result[2]["name"] == "C"

def test_sort_items_nested_key():
    # Arrange
    items = [
        {"name": "B", "stats": {"stars": 50}},
        {"name": "A", "stats": {"stars": 100}},
        {"name": "C", "stats": {"stars": 20}}
    ]
    
    # Act - sort by stats.stars descending
    result = sort_items(items, "stats.stars", "desc")
    
    # Assert
    assert result[0]["name"] == "A"  # 100 stars
    assert result[1]["name"] == "B"  # 50 stars
    assert result[2]["name"] == "C"  # 20 stars
```

## Completion Criteria
- Topics listing command implemented and functioning
- Topic-specific repository filtering working correctly
- Sorting and filtering options operational
- All unit tests passing for new functionality
- Integration with existing CLI framework verified
- Documentation updated with usage examples
