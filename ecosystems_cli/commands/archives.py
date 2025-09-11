"""Commands for the archives API."""

from ecosystems_cli.commands.generator import APICommandGenerator

archives = APICommandGenerator.create_api_group("archives")
