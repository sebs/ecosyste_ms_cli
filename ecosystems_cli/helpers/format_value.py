from ecosystems_cli.constants import (
    DICT_TRUNCATE_FORMAT,
    EMPTY_DICT_DISPLAY,
    EMPTY_LIST_DISPLAY,
    LIST_TRUNCATE_FORMAT,
    MAX_INLINE_ITEMS,
)


def format_value(value):
    """Format a value for display in a table or TSV."""
    if isinstance(value, (dict, list)):
        # For complex objects, show a simplified representation
        if isinstance(value, dict):
            if len(value) == 0:
                return EMPTY_DICT_DISPLAY
            elif len(value) <= MAX_INLINE_ITEMS:
                return ", ".join(f"{k}: {format_value(v)}" for k, v in value.items())
            else:
                return DICT_TRUNCATE_FORMAT.format(count=len(value))
        elif isinstance(value, list):
            if len(value) == 0:
                return EMPTY_LIST_DISPLAY
            elif len(value) <= MAX_INLINE_ITEMS:
                return ", ".join(format_value(v) for v in value)
            else:
                return LIST_TRUNCATE_FORMAT.format(count=len(value))
    return str(value)
