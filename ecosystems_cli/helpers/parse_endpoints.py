from typing import Any, Dict

from ecosystems_cli.helpers.parse_parameters import parse_parameters


def parse_endpoints(spec: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Parse endpoints from OpenAPI specification."""
    endpoints = {}
    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method, details in methods.items():
            if method in ["get", "post", "put", "delete", "patch"]:
                operation_id = details.get("operationId")
                if operation_id:
                    endpoints[operation_id] = {
                        "path": path,
                        "method": method,
                        "params": parse_parameters(details),
                        "description": details.get("description", ""),
                        "summary": details.get("summary", ""),
                        "required_params": {k: v for k, v in parse_parameters(details).items() if v.get("required", False)},
                    }
    return endpoints
