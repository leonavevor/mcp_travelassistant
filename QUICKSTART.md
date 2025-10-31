# Unified MCP Server - Quick Start Guide

## What is this?

This is a **unified MCP (Model Context Protocol) server** that provides a single entry point to all travel planning services. Instead of running multiple separate servers, you connect to ONE server that orchestrates all travel services.

## Architecture

```
┌─────────────────────────────────────────┐
│   MCP Client (Claude Desktop, etc.)     │
└──────────────────┬──────────────────────┘
                   │ MCP Protocol (stdio)
┌──────────────────▼──────────────────────┐
│   Unified MCP Server (mcp_server.py)    │
│   - Single entry point                  │
│   - Exposes all travel tools            │
└──────────────────┬──────────────────────┘
                   │ Orchestrates
         ┌─────────┼─────────┐
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │ Flight │ │ Hotel  │ │Weather │ ...
    │ Server │ │ Server │ │ Server │
    └────────┘ └────────┘ └────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd /path/to/mcp_travelplanner
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Environment Variables (if needed)

```bash
# For flight searches (optional)
export SERPAPI_KEY="your_serpapi_key_here"
```

### 3. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration (replace `/path/to/` with your actual path):

```json
{
  "mcpServers": {
    "travel-planner": {
      "command": "python",
      "args": ["-m", "py_mcp_travelplanner.mcp_server"],
      "cwd": "/absolute/path/to/mcp_travelplanner",
      "env": {
        "PYTHONPATH": "/absolute/path/to/mcp_travelplanner"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

The travel-planner server will now be available in Claude.

## Available Tools

Once connected, you can use these tools through Claude:

| Tool | Description |
|------|-------------|
| `list_servers` | List all available travel service backends |
| `start_server` | Start a specific service (flight, hotel, weather, etc.) |
| `start_all_servers` | Start all services at once |
| `stop_server` | Stop a running service |
| `health_check` | Check if a service is healthy |
| `get_status` | Get system status and running services |
| `list_pids` | List running service process IDs |
| `verify_serpapi_key` | Test SERPAPI_KEY configuration |

## Example Usage in Claude

Once configured, you can ask Claude things like:

- "Can you start all the travel planner services?"
- "Check the health of the flight server"
- "What travel services are currently running?"
- "Start the hotel server"

Claude will use the MCP tools to interact with your travel planner services.

## Testing the Server Directly

You can test the server without Claude:

```bash
# Start the server directly (stdio mode)
python -m py_mcp_travelplanner.mcp_server

# Or via CLI
python -m py_mcp_travelplanner.cli mcp
```

## Troubleshooting

### Server won't start
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.12.1 or later: `python --version`
- Check the logs for errors

### Tools not appearing in Claude
- Verify the `cwd` path in your config is absolute and correct
- Restart Claude Desktop after config changes
- Check Claude's MCP server status in settings

### SERPAPI_KEY errors
- Only needed for flight search features
- Set it in the `env` section of your MCP config, or export it before starting Claude
- Test with: Use the `verify_serpapi_key` tool

## What's Next?

- See `README.md` for detailed documentation
- Check individual service READMEs in `py_mcp_travelplanner/*/README.md`
- Review `mcp_config.json` for runtime service configuration

## Support

For issues or questions, open an issue in the repository with:
- Your environment (OS, Python version)
- The error message or unexpected behavior
- Steps to reproduce

