"""Commands for the docker API."""

from ecosystems_cli.commands.generator import APICommandGenerator

docker = APICommandGenerator.create_api_group("docker")
