"""Commands for the opencollective API."""

from ecosystems_cli.commands.generator import APICommandGenerator

opencollective = APICommandGenerator.create_api_group("opencollective")
