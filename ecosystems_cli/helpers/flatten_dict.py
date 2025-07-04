from typing import Any, Dict, List, Tuple

from ecosystems_cli.constants import DEFAULT_SEPARATOR


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = DEFAULT_SEPARATOR) -> Dict[str, Any]:
    """Flatten a nested dictionary for TSV output."""
    items: List[Tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
