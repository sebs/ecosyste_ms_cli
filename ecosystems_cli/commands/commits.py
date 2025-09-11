"""Commands for the commits API."""

from ecosystems_cli.commands.generator import APICommandGenerator

commits = APICommandGenerator.create_api_group("commits")
