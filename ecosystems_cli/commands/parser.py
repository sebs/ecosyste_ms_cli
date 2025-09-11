"""Commands for the parser API."""

from ecosystems_cli.commands.generator import APICommandGenerator

parser = APICommandGenerator.create_api_group("parser")
