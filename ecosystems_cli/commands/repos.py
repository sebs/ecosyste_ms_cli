"""Commands for the repos API."""

from ecosystems_cli.commands.generator import APICommandGenerator

repos = APICommandGenerator.create_api_group("repos")
