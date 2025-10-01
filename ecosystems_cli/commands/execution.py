"""API execution helpers for ecosystems CLI commands."""

from typing import Optional

from rich.console import Console

from ecosystems_cli.bravado_client import _factory as bravado_factory
from ecosystems_cli.commands.handlers import OperationHandlerFactory
from ecosystems_cli.constants import DEFAULT_OUTPUT_FORMAT, DEFAULT_TIMEOUT
from ecosystems_cli.exceptions import EcosystemsCLIError
from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence
from ecosystems_cli.helpers.print_error import print_error
from ecosystems_cli.helpers.print_output import print_output

console = Console()


def update_context(ctx, timeout: int, format: str, domain: Optional[str], mailto: Optional[str] = None):
    """Update context with command-level options if they differ from defaults.

    Args:
        ctx: Click context
        timeout: Timeout value from command options
        format: Format value from command options
        domain: Domain value from command options
        mailto: Email address for polite pool access
    """
    ctx.ensure_object(dict)
    if timeout != DEFAULT_TIMEOUT:
        ctx.obj["timeout"] = timeout
    if format != DEFAULT_OUTPUT_FORMAT:
        ctx.obj["format"] = format
    if domain is not None:
        ctx.obj["domain"] = domain
    if mailto is not None:
        ctx.obj["mailto"] = mailto


def execute_api_call(
    ctx,
    api_name: str,
    method_name: Optional[str] = None,
    operation_id: Optional[str] = None,
    call_args: tuple = (),
    call_kwargs: Optional[dict] = None,
):
    """Execute an API call with proper error handling.

    Args:
        ctx: Click context
        api_name: Name of the API (e.g., 'repos', 'packages')
        method_name: API client method name (for direct method calls)
        operation_id: Operation ID (for call method)
        call_args: Positional arguments for the API call
        call_kwargs: Keyword arguments for the API call
    """
    if call_kwargs is None:
        call_kwargs = {}

    # Get domain with proper precedence
    domain = get_domain_with_precedence(api_name, ctx.obj.get("domain"))
    base_url = build_base_url(domain, api_name)

    try:
        if operation_id:
            if call_args or call_kwargs:
                # Use operation handler to build parameters
                handler = OperationHandlerFactory.get_handler(api_name)
                path_params, query_params = handler.build_params(operation_id, call_args, call_kwargs)
                result = bravado_factory.call(
                    api_name,
                    operation_id,
                    path_params=path_params,
                    query_params=query_params,
                    timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT),
                    mailto=ctx.obj.get("mailto"),
                    base_url=base_url,
                )
            else:
                # Simple operation call without parameters
                result = bravado_factory.call(
                    api_name,
                    operation_id,
                    path_params={},
                    query_params={},
                    timeout=ctx.obj.get("timeout", DEFAULT_TIMEOUT),
                    mailto=ctx.obj.get("mailto"),
                    base_url=base_url,
                )
        elif method_name:
            raise ValueError("Direct method calls not supported with Bravado client")
        else:
            raise ValueError("Either method_name or operation_id must be provided")

        print_output(result, ctx.obj.get("format", DEFAULT_OUTPUT_FORMAT), console=console)
    except EcosystemsCLIError as e:
        print_error(str(e), console=console)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}", console=console)
