"""
Utility functions for Ecosyste.ms CLI.
"""
from .errors import APIError, ValidationError, handle_api_error
from .output import format_output, format_table, truncate_string
from .pagination import paginate, collect_pages
from .auth import AuthManager, get_auth_manager
from .cache import Cache, get_cache
from .data import (
    filter_dict, extract_value, filter_list,
    search_dict, flatten_dict
)
from .logging import CLILogger, get_logger
