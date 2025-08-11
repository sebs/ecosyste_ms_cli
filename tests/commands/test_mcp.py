"""Tests for the MCP command."""

from unittest.mock import patch

from click.testing import CliRunner

from ecosystems_cli.commands.mcp import mcp


class TestMCPCommand:
    """Test cases for the MCP command."""

    def test_mcp_command_stdio(self):
        """Test MCP command with stdio transport."""
        runner = CliRunner()

        with patch("ecosystems_cli.mcp_server.run_mcp_server") as mock_run:
            result = runner.invoke(mcp, ["--transport", "stdio"])

            # Check the command ran successfully
            assert result.exit_code == 0
            assert "Starting MCP server with stdio transport" in result.output

            # Verify run_mcp_server was called
            mock_run.assert_called_once()

    def test_mcp_command_default_transport(self):
        """Test MCP command with default transport (stdio)."""
        runner = CliRunner()

        with patch("ecosystems_cli.mcp_server.run_mcp_server") as mock_run:
            result = runner.invoke(mcp)

            # Check the command ran successfully
            assert result.exit_code == 0
            assert "Starting MCP server with stdio transport" in result.output

            # Verify run_mcp_server was called
            mock_run.assert_called_once()

    def test_mcp_command_http_not_implemented(self):
        """Test MCP command with HTTP transport (not implemented)."""
        runner = CliRunner()

        result = runner.invoke(mcp, ["--transport", "http", "--port", "8080"])

        # Check the command failed with expected error
        assert result.exit_code != 0
        assert "HTTP transport is not yet implemented" in result.output

    def test_mcp_command_help(self):
        """Test MCP command help output."""
        runner = CliRunner()
        result = runner.invoke(mcp, ["--help"])

        assert result.exit_code == 0
        assert "Start an MCP (Model Context Protocol) server" in result.output
        assert "--transport" in result.output
        assert "--host" in result.output
        assert "--port" in result.output
        assert "stdio" in result.output
        assert "http" in result.output

    def test_mcp_command_with_custom_host(self):
        """Test MCP command with custom host parameter."""
        runner = CliRunner()

        with patch("ecosystems_cli.mcp_server.run_mcp_server") as mock_run:
            result = runner.invoke(mcp, ["--host", "0.0.0.0"])

            # Check the command ran successfully
            assert result.exit_code == 0
            # Note: host parameter is currently not used for stdio transport
            mock_run.assert_called_once()

    def test_mcp_command_invalid_transport(self):
        """Test MCP command with invalid transport option."""
        runner = CliRunner()

        result = runner.invoke(mcp, ["--transport", "invalid"])

        # Check the command failed with validation error
        assert result.exit_code != 0
        assert "Invalid value" in result.output or "invalid" in result.output
