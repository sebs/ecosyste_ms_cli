from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_api_spec(api_name: str, base_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load OpenAPI specification from file."""
    if base_path is None:
        base_path = Path(__file__).parent.parent.parent / "apis"
    api_file = base_path / f"{api_name}.openapi.yaml"
    if not api_file.exists():
        raise ValueError(f"API specification for '{api_name}' not found")
    with open(api_file, "r") as f:
        return yaml.safe_load(f)
