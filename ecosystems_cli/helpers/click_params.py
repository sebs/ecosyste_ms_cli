"""Shared utilities for building Click parameter decorators from OpenAPI parameters."""

from typing import List

import click


def build_click_decorators(parameters: List[dict]) -> List:
    """Build click decorators from OpenAPI parameters.

    This utility function converts OpenAPI parameter definitions into Click
    decorators for command-line arguments and options.

    Args:
        parameters: List of OpenAPI parameter definitions

    Returns:
        List of Click parameter decorators
    """
    click_decorators = []
    for param in parameters:
        param_name = param.get("name")
        param_in = param.get("in")
        param_description = param.get("description", "")
        param_required = param.get("required", False)
        param_schema = param.get("schema", {})
        param_type = param_schema.get("type", "string")

        python_param_name = param_name.replace("_", "-")

        if param_in == "path":
            click_decorators.append(click.argument(param_name))
        elif param_in == "query":
            click_type = None
            if param_type == "integer":
                click_type = int
            elif param_type == "boolean":
                click_type = bool

            option_decorator = click.option(
                f"--{python_param_name}",
                param_name.replace("-", "_"),
                type=click_type,
                help=param_description,
                required=param_required,
            )
            click_decorators.append(option_decorator)

    return click_decorators
