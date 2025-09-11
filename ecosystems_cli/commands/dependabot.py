"""Commands for the dependabot API."""

from ecosystems_cli.commands.generator import APICommandGenerator

dependabot = APICommandGenerator.create_api_group("dependabot")
