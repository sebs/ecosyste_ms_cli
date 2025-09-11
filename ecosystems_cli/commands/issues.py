"""Commands for the issues API."""

from ecosystems_cli.commands.generator import APICommandGenerator

issues = APICommandGenerator.create_api_group("issues")
