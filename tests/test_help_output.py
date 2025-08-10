"""Tests for help output of the CLI."""

from click.testing import CliRunner

from ecosystems_cli.cli import main as cli


def test_main_help_output():
    """Test that main help output includes expected information."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Ecosystems CLI for interacting with ecosyste.ms APIs" in result.output
    assert "--timeout" in result.output
    assert "--format" in result.output
    assert "--domain" in result.output
    assert "advisories" in result.output


def test_advisories_help_output():
    """Test that advisories command help output includes expected information."""
    runner = CliRunner()
    result = runner.invoke(cli, ["advisories", "--help"])

    assert result.exit_code == 0
    assert "advisories" in result.output.lower()
    assert "--timeout" in result.output
    assert "--format" in result.output


def test_subcommand_help_includes_global_options():
    """Test that subcommand help includes global options."""
    runner = CliRunner()
    result = runner.invoke(cli, ["advisories", "--help"])

    assert result.exit_code == 0
    assert "--timeout" in result.output
    assert "--format" in result.output
    assert "--domain" in result.output
