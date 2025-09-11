"""Commands for the advisories API."""

from ecosystems_cli.commands.generator import APICommandGenerator

advisories = APICommandGenerator.create_api_group("advisories")
