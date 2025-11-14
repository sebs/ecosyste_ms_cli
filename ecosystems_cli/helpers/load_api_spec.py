import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from ecosystems_cli.constants import OPENAPI_FILE_EXTENSION

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files


def load_api_spec(api_name: str, base_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load OpenAPI specification from file."""
    if base_path is None:
        # Use importlib.resources for reliable resource access
        try:
            api_file_name = f"{api_name}{OPENAPI_FILE_EXTENSION}"
            spec_content = files("ecosystems_cli.apis").joinpath(api_file_name).read_text()
            return yaml.safe_load(spec_content)
        except (FileNotFoundError, ModuleNotFoundError):
            raise ValueError(f"API specification for '{api_name}' not found")
    else:
        # Fallback for custom base_path (mainly for testing)
        api_file = base_path / f"{api_name}{OPENAPI_FILE_EXTENSION}"
        if not api_file.exists():
            raise ValueError(f"API specification for '{api_name}' not found")
        with open(api_file, "r") as f:
            return yaml.safe_load(f)
