"""
Output formatting utilities for Ecosyste.ms CLI.
"""
import json
import csv
import io
from typing import Any, Dict, List, Union

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
