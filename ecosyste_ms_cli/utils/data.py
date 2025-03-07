"""
Data processing utilities for Ecosyste.ms CLI.
"""
from typing import Any, Dict, List, Callable, Optional, Union, TypeVar, cast

T = TypeVar('T')


def filter_dict(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Filter dictionary to include only specified keys.
    
    Args:
        data: Dictionary to filter
        keys: List of keys to include
        
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if k in keys}


def extract_value(data: Dict[str, Any], path: str) -> Any:
    """
    Extract a value from nested dictionaries using dot notation.
    
    Example:
        extract_value({"user": {"profile": {"name": "John"}}}, "user.profile.name")
        # Returns "John"
        
    Args:
        data: Dictionary to extract from
        path: Path to value using dot notation
        
    Returns:
        Extracted value or None if not found
    """
    parts = path.split('.')
    current = data
    
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
            
    return current


def filter_list(items: List[T], matcher: Callable[[T], bool]) -> List[T]:
    """
    Filter a list using a matcher function.
    
    Args:
        items: List to filter
        matcher: Function that returns True for items to keep
        
    Returns:
        Filtered list
    """
    return [item for item in items if matcher(item)]


def search_dict(data: Dict[str, Any], term: str) -> bool:
    """
    Search recursively for a term in a dictionary's string values.
    
    Args:
        data: Dictionary to search
        term: Term to search for
        
    Returns:
        True if term is found in any string value
    """
    for key, value in data.items():
        if isinstance(value, str) and term.lower() in value.lower():
            return True
        elif isinstance(value, dict) and search_dict(value, term):
            return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and search_dict(item, term):
                    return True
                elif isinstance(item, str) and term.lower() in item.lower():
                    return True
                    
    return False


def flatten_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a single-level dictionary with dot notation keys.
    
    Example:
        flatten_dict({"user": {"name": "John", "age": 30}})
        # Returns {"user.name": "John", "user.age": 30}
        
    Args:
        data: Dictionary to flatten
        prefix: Prefix for keys (used in recursion)
        
    Returns:
        Flattened dictionary
    """
    result = {}
    
    for key, value in data.items():
        new_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            result.update(flatten_dict(value, new_key))
        else:
            result[new_key] = value
            
    return result


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
                    # Return a default value based on the expected type
                    # For descending order, use minimum value so missing values appear last
                    # For ascending order, use maximum value so missing values appear last
                    return float('-inf') if reverse else float('inf')
            return value
        return item.get(sort_by, float('-inf') if reverse else float('inf'))
    
    # Sort the items
    return sorted(items, key=get_sort_key, reverse=reverse)
