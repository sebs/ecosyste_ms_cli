def parse_parameters(details: dict) -> dict:
    """
    Parse parameters from endpoint details.

    Args:
        details (dict): The endpoint details, typically from an OpenAPI spec.

    Returns:
        dict: A dictionary mapping parameter names to their metadata, including location, requirement, schema, and description.
    """
    params = {}
    for param in details.get("parameters", []):
        param_name = param.get("name")
        if param_name:
            params[param_name] = {
                "in": param.get("in"),
                "required": param.get("required", False),
                "schema": param.get("schema", {}),
                "description": param.get("description", ""),
            }
    return params
