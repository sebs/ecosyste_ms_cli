"""Commands for the advisories API."""

import re

import click

from ecosystems_cli.commands.base import BaseCommand
from ecosystems_cli.helpers.load_api_spec import load_api_spec


class AdvisoriesCommands(BaseCommand):
    """Commands for the advisories API."""

    def __init__(self):
        super().__init__("advisories", "Commands for the advisories API.")
        self._register_commands()

    def _operation_id_to_command_name(self, operation_id: str) -> str:
        """Convert operationId to command name.

        Examples:
        - getAdvisories -> get_advisories
        - getAdvisoriesPackages -> get_advisories_packages
        - getAdvisory -> get_advisory
        """
        # Convert camelCase to snake_case
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", operation_id)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def _register_commands(self):
        """Register all commands for the advisories API dynamically from OpenAPI spec."""
        # Load the OpenAPI spec
        spec = load_api_spec("advisories")

        # Iterate through all paths and operations
        for path, path_item in spec.get("paths", {}).items():
            for method, operation in path_item.items():
                if method in ["get", "post", "put", "delete", "patch"]:
                    operation_id = operation.get("operationId")
                    if not operation_id:
                        continue

                    # Convert operationId to command name
                    command_name = self._operation_id_to_command_name(operation_id)
                    description = operation.get("summary", f"Execute {operation_id}")

                    # Get parameters
                    parameters = operation.get("parameters", [])

                    # Build click options and arguments
                    click_decorators = []
                    for param in parameters:
                        param_name = param.get("name")
                        param_in = param.get("in")
                        param_description = param.get("description", "")
                        param_required = param.get("required", False)
                        param_schema = param.get("schema", {})
                        param_type = param_schema.get("type", "string")

                        # Convert parameter name to Python-friendly format
                        python_param_name = param_name.replace("_", "-")

                        if param_in == "path":
                            # Path parameters become arguments
                            click_decorators.append(click.argument(param_name))
                        elif param_in == "query":
                            # Query parameters become options
                            click_type = None
                            if param_type == "integer":
                                click_type = int
                            elif param_type == "boolean":
                                click_type = bool

                            option_decorator = click.option(
                                f"--{python_param_name}",
                                param_name.replace("-", "_"),  # Use underscore for Python variable
                                type=click_type,
                                help=param_description,
                                required=param_required,
                            )
                            click_decorators.append(option_decorator)

                    # Create the command
                    if not parameters:
                        # Simple command without parameters
                        self.create_simple_command(command_name, "call", description, operation_id=operation_id)
                    else:
                        # Command with parameters
                        @self.create_command_with_operation(command_name, operation_id, description, *click_decorators)
                        def command_impl(**kwargs):
                            pass


advisories_base = AdvisoriesCommands()

# Export the properly named group
advisories = advisories_base.group
advisories.name = "advisories"
