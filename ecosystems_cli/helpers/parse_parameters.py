from typing import Any, Dict, List


def parse_parameters(details: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Parse parameters from endpoint details.

    Args:
        details (dict): The endpoint details, typically from an OpenAPI spec.

    Returns:
        dict: A dictionary mapping parameter names to their metadata, including location, requirement, schema, and description.
    """
    params: Dict[str, Dict[str, Any]] = {}
    parameters: List[Dict[str, Any]] = details.get("parameters", [])
    for param in parameters:
        param_name = param.get("name")
        if param_name:
            params[param_name] = {
                "in": param.get("in"),
                "required": param.get("required", False),
                "schema": param.get("schema", {}),
                "description": param.get("description", ""),
            }
    return params
