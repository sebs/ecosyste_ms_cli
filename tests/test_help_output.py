from unittest import mock

from click.testing import CliRunner

from ecosystems_cli.cli import main as cli


def test_subcommand_help_includes_global_options():
    """Test that subcommand help includes global options from parent."""
    runner = CliRunner()

    # Test repos subcommand help
    result = runner.invoke(cli, ["repos", "--help"])
    assert result.exit_code == 0

    # Check that global options are shown
    assert "--timeout" in result.output
    assert "Timeout in seconds for API requests" in result.output
    assert "--format" in result.output
    assert "Output format" in result.output

    # Test another subcommand to ensure consistency
    result = runner.invoke(cli, ["packages", "--help"])
    assert result.exit_code == 0
    assert "--timeout" in result.output
    assert "--format" in result.output


@mock.patch("ecosystems_cli.commands.base.get_client")
@mock.patch("ecosystems_cli.commands.base.print_output")
def test_subcommand_shows_inherited_options(mock_print_output, mock_get_client):
    """Test that subcommands can use inherited global options from parent."""
    runner = CliRunner()

    # Mock the API client
    mock_client = mock.MagicMock()
    mock_client.get_topics.return_value = {"data": []}
    mock_get_client.return_value = mock_client

    # Test that we can use global options at the subcommand level
    result = runner.invoke(cli, ["repos", "--timeout", "30", "--format", "json", "topics"])
    assert result.exit_code == 0
    # Check that the client was called with the correct timeout
    mock_get_client.assert_called_with("repos", base_url=None, timeout=30)

    # Reset mocks
    mock_get_client.reset_mock()

    # Test that we can also specify them at the main level
    result = runner.invoke(cli, ["--timeout", "40", "--format", "json", "repos", "topics"])
    assert result.exit_code == 0
    # Check that the client was called with the correct timeout from main level
    mock_get_client.assert_called_with("repos", base_url=None, timeout=40)
