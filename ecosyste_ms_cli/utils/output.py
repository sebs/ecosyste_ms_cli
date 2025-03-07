"""
Output formatting utilities for Ecosyste.ms CLI.
"""
import json
import csv
import io
from typing import Any, Dict, List, Union, Optional

import tabulate
from ..commands.common import OutputFormat


def format_output(data: Union[Dict[str, Any], List[Dict[str, Any]]], 
                 output_format: OutputFormat) -> str:
    """
    Format data according to specified output format.
    
    Args:
        data: Data to format (dict or list of dicts)
        output_format: Desired output format (JSON, CSV, TSV)
        
    Returns:
        Formatted string representation of data
    """
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


def format_table(data: List[Dict[str, Any]], headers: Union[List[str], str] = "keys") -> str:
    """
    Format data as a table for terminal display.
    
    Args:
        data: List of dictionaries to format
        headers: Column headers ("keys" for dict keys, list for custom headers)
        
    Returns:
        Formatted table string
    """
    return tabulate.tabulate(data, headers=headers, tablefmt="grid")


def truncate_string(s: str, max_length: int = 50) -> str:
    """Truncate a string to max_length with ellipsis if needed."""
    if len(s) <= max_length:
        return s
    return s[:max_length-3] + "..."
