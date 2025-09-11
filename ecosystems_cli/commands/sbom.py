"""Commands for the sbom API."""

from ecosystems_cli.commands.generator import APICommandGenerator

sbom = APICommandGenerator.create_api_group("sbom")
