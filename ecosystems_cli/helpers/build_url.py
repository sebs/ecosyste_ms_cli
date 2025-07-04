from typing import Dict, Optional


def build_url(base_url: str, path: str, path_params: Optional[Dict[str, str]] = None) -> str:
    """
    Construct a URL by combining a base URL and a path, replacing placeholders in the path with values from path_params.

    Args:
        base_url (str): The base URL (e.g., 'https://api.example.com').
        path (str): The URL path, which may contain placeholders in curly braces (e.g., '/foo/{bar}/baz/{qux}').
        path_params (dict): A dictionary mapping placeholder names to their replacement values.

    Returns:
        str: The constructed URL with placeholders replaced by their corresponding values.
            If a placeholder is not provided in path_params, it remains unchanged in the output.
    """
    url = f"{base_url}{path}"
    for param, value in (path_params or {}).items():
        url = url.replace(f"{{{param}}}", str(value))
    return url
