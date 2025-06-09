def format_value(value):
    """Format a value for display in a table or TSV."""
    if isinstance(value, (dict, list)):
        # For complex objects, show a simplified representation
        if isinstance(value, dict):
            if len(value) == 0:
                return "{}"
            elif len(value) <= 3:
                return ", ".join(f"{k}: {format_value(v)}" for k, v in value.items())
            else:
                return f"{{...}} ({len(value)} items)"
        elif isinstance(value, list):
            if len(value) == 0:
                return "[]"
            elif len(value) <= 3:
                return ", ".join(format_value(v) for v in value)
            else:
                return f"[...] ({len(value)} items)"
    return str(value)
