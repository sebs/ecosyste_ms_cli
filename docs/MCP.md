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

### Python Installation

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

### Docker Installation

1. Build the Docker image:
```bash
docker build -t ecosystems-mcp .
```

2. Add to config:
```json
{
  "mcpServers": {
    "ecosystems": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "ecosystems-mcp"
      ]
    }
  }
}
```

Restart Claude Code after saving.
