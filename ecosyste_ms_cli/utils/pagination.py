"""
Pagination utilities for Ecosyste.ms CLI.
"""
from typing import Callable, List, Dict, Any, Optional, Generator, TypeVar, Generic, Union
import typer

T = TypeVar('T')


def paginate(
    fetch_func: Callable[[int, int], List[Dict[str, Any]]],
    page: int = 1,
    per_page: int = 30,
    max_items: Optional[int] = None,
    verbose: bool = False
) -> Generator[Dict[str, Any], None, None]:
    """
    Paginate through API results using the provided fetch function.
    
    Args:
        fetch_func: Function that accepts page and per_page arguments
        page: Starting page number
        per_page: Number of items per page
        max_items: Maximum number of items to return (None for all)
        verbose: Whether to show progress
        
    Yields:
        Individual items from the paginated results
    """
    items_processed = 0
    current_page = page
    
    while True:
        if verbose:
            typer.echo(f"Fetching page {current_page}...", err=True)
            
        results = fetch_func(current_page, per_page)
        
        if not results:
            break
            
        for item in results:
            yield item
            items_processed += 1
            
            if max_items is not None and items_processed >= max_items:
                return
                
        current_page += 1


def collect_pages(
    fetch_func: Callable[[int, int], List[T]],
    page: int = 1,
    per_page: int = 30,
    max_pages: Optional[int] = None,
    verbose: bool = False
) -> List[T]:
    """
    Collect all items from paginated API results into a single list.
    
    Args:
        fetch_func: Function that accepts page and per_page arguments
        page: Starting page number
        per_page: Number of items per page
        max_pages: Maximum number of pages to fetch (None for all)
        verbose: Whether to show progress
        
    Returns:
        List of all items from all pages
    """
    all_items = []
    current_page = page
    pages_fetched = 0
    
    while True:
        if verbose:
            typer.echo(f"Fetching page {current_page}...", err=True)
        
        results = fetch_func(current_page, per_page)
        
        if not results:
            break
        
        all_items.extend(results)
        pages_fetched += 1
        
        if max_pages is not None and pages_fetched >= max_pages:
            break
        
        current_page += 1
    
    return all_items
