# MCP Server

## Quick Start

```bash
# Start server
ecosystems mcp

# Test with inspector
npx @modelcontextprotocol/inspector "python -m ecosystems_cli.mcp_server"
```

## Claude Code Setup

Add to config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ecosystems": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "ecosystems_cli.mcp_server"],
      "env": {}
    }
  }
}
```

Restart Claude Code after saving.
