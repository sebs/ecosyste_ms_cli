"""
Tests for the main CLI functionality.
"""
import pytest
from typer.testing import CliRunner

from ecosyste_ms_cli.main import app


@pytest.fixture
def runner():
    """
    Create a test runner for the CLI.
    """
    return CliRunner()


def test_version_command(runner):
    """
    Test that the version command displays version information.
    
    Arrange: Set up the CLI runner
    Act: Execute the version command
    Assert: Check that version information is displayed
    """
    result = runner.invoke(app, ["version"])
    
    assert result.exit_code == 0
    assert "Ecosyste.ms CLI version:" in result.stdout


def test_help_command(runner):
    """
    Test that the help command displays help information.
    
    Arrange: Set up the CLI runner
    Act: Execute the help command
    Assert: Check that help information is displayed
    """
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
