"""Commands for the packages API."""

import click

from ecosystems_cli.commands.base import BaseCommand


class PackagesCommands(BaseCommand):
    """Commands for the packages API."""

    def __init__(self) -> None:
        super().__init__("packages", "Commands for the packages API.")
        self._register_commands()

    def _register_commands(self) -> None:
        """Register all commands for the packages API."""
        # Register list operations command
        self.list_operations()

        # Register simple commands
        self.create_simple_command("registries", "get_registries", "Get all package registries.")

        # Custom implementation for get_registry to handle argument name mapping
        @self.group.command("registry", help="Get a specific registry by name.")
        @click.argument("name")
        @click.option(
            "--format",
            default="table",
            type=click.Choice(["table", "json", "tsv", "jsonl"]),
            help="Output format. Default is table.",
        )
        @click.option(
            "--timeout",
            default=20,
            help="Timeout in seconds for API requests. Default is 20 seconds.",
        )
        @click.option(
            "--domain",
            default=None,
            help="Override the API domain. Example: api.example.com",
        )
        @click.pass_context
        def get_registry(ctx, name: str, format: str, timeout: int, domain: str) -> None:
            """Get a specific registry by name."""
            from ecosystems_cli.api_client import get_client
            from ecosystems_cli.exceptions import EcosystemsCLIError
            from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence
            from ecosystems_cli.helpers.print_error import print_error
            from ecosystems_cli.helpers.print_output import print_output

            # Update context with command-level options
            ctx.ensure_object(dict)
            if timeout != 20:
                ctx.obj["timeout"] = timeout
            if format != "table":
                ctx.obj["format"] = format
            if domain is not None:
                ctx.obj["domain"] = domain

            # Get domain with proper precedence
            domain = get_domain_with_precedence(self.api_name, ctx.obj.get("domain"))
            base_url = build_base_url(domain, self.api_name)

            client = get_client(self.api_name, base_url=base_url, timeout=ctx.obj.get("timeout", 20))
            try:
                # Map arguments to expected parameter names
                result = client.get_registry(registry_name=name)
                print_output(result, ctx.obj.get("format", "table"), console=self.console)
            except EcosystemsCLIError as e:
                print_error(str(e), console=self.console)
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}", console=self.console)

        # Custom implementation for get_package to handle argument name mapping
        @self.group.command("package", help="Get a specific package from a registry.")
        @click.argument("registry")
        @click.argument("package")
        @click.option(
            "--format",
            default="table",
            type=click.Choice(["table", "json", "tsv", "jsonl"]),
            help="Output format. Default is table.",
        )
        @click.option(
            "--timeout",
            default=20,
            help="Timeout in seconds for API requests. Default is 20 seconds.",
        )
        @click.option(
            "--domain",
            default=None,
            help="Override the API domain. Example: api.example.com",
        )
        @click.pass_context
        def get_package(ctx, registry: str, package: str, format: str, timeout: int, domain: str) -> None:
            """Get a specific package from a registry."""
            from ecosystems_cli.api_client import get_client
            from ecosystems_cli.exceptions import EcosystemsCLIError
            from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence
            from ecosystems_cli.helpers.print_error import print_error
            from ecosystems_cli.helpers.print_output import print_output

            # Update context with command-level options
            ctx.ensure_object(dict)
            if timeout != 20:
                ctx.obj["timeout"] = timeout
            if format != "table":
                ctx.obj["format"] = format
            if domain is not None:
                ctx.obj["domain"] = domain

            # Get domain with proper precedence
            domain = get_domain_with_precedence(self.api_name, ctx.obj.get("domain"))
            base_url = build_base_url(domain, self.api_name)

            client = get_client(self.api_name, base_url=base_url, timeout=ctx.obj.get("timeout", 20))
            try:
                # Map arguments to expected parameter names
                result = client.get_package(registry_name=registry, package_name=package)
                print_output(result, ctx.obj.get("format", "table"), console=self.console)
            except EcosystemsCLIError as e:
                print_error(str(e), console=self.console)
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}", console=self.console)

        # Custom implementation for get_package_version to handle argument name mapping
        @self.group.command("version", help="Get a specific package version.")
        @click.argument("registry")
        @click.argument("package")
        @click.argument("version")
        @click.option(
            "--format",
            default="table",
            type=click.Choice(["table", "json", "tsv", "jsonl"]),
            help="Output format. Default is table.",
        )
        @click.option(
            "--timeout",
            default=20,
            help="Timeout in seconds for API requests. Default is 20 seconds.",
        )
        @click.option(
            "--domain",
            default=None,
            help="Override the API domain. Example: api.example.com",
        )
        @click.pass_context
        def get_package_version(ctx, registry: str, package: str, version: str, format: str, timeout: int, domain: str) -> None:
            """Get a specific package version."""
            from ecosystems_cli.api_client import get_client
            from ecosystems_cli.exceptions import EcosystemsCLIError
            from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence
            from ecosystems_cli.helpers.print_error import print_error
            from ecosystems_cli.helpers.print_output import print_output

            # Update context with command-level options
            ctx.ensure_object(dict)
            if timeout != 20:
                ctx.obj["timeout"] = timeout
            if format != "table":
                ctx.obj["format"] = format
            if domain is not None:
                ctx.obj["domain"] = domain

            # Get domain with proper precedence
            domain = get_domain_with_precedence(self.api_name, ctx.obj.get("domain"))
            base_url = build_base_url(domain, self.api_name)

            client = get_client(self.api_name, base_url=base_url, timeout=ctx.obj.get("timeout", 20))
            try:
                # Map arguments to expected parameter names
                result = client.get_package_version(registry_name=registry, package_name=package, version=version)
                print_output(result, ctx.obj.get("format", "table"), console=self.console)
            except EcosystemsCLIError as e:
                print_error(str(e), console=self.console)
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}", console=self.console)


packages_base = PackagesCommands()

# Export the properly named group
packages = packages_base.group
packages.name = "packages"
