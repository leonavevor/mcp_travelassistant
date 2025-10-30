# Unified MCP Server for py_mcp_travelplanner

The unified MCP server provides a single interface to manage all travel planner services through the Model Context Protocol.

## Features

- **Unified Interface**: Control all travel planner servers (event, flight, hotel, weather, geocoder, finance) through a single MCP endpoint
- **Service Management**: Start, stop, and monitor individual servers or all at once
- **Health Checks**: Verify server status and SERPAPI_KEY validity
- **PID Tracking**: Track running processes and manage their lifecycle

## Available Tools

The MCP server exposes the following tools:

### 1. `list_servers`
List all discovered travel planner servers.

**Input**: None

**Example**:
```json
{
  "name": "list_servers",
  "arguments": {}
}
```

### 2. `start_server`
Start a specific travel planner server.

**Input**:
- `server` (required): Server name (e.g., "event_server", "flight_server")
- `dry_run` (optional): If true, only show what would be started

**Example**:
```json
{
  "name": "start_server",
  "arguments": {
    "server": "event_server",
    "dry_run": false
  }
}
```

### 3. `start_all_servers`
Start all discovered servers (requires SERPAPI_KEY).

**Input**:
- `dry_run` (optional): If true, only show what would be started

**Example**:
```json
{
  "name": "start_all_servers",
  "arguments": {
    "dry_run": false
  }
}
```

### 4. `stop_server`
Stop a running server by name or PID.

**Input**:
- `server` (required): Server name or numeric PID
- `timeout` (optional): Timeout in seconds (default: 5.0)

**Example**:
```json
{
  "name": "stop_server",
  "arguments": {
    "server": "event_server",
    "timeout": 5.0
  }
}
```

### 5. `health_check`
Check if a server's main.py exists and is readable.

**Input**:
- `server` (required): Server name

**Example**:
```json
{
  "name": "health_check",
  "arguments": {
    "server": "event_server"
  }
}
```

### 6. `get_status`
Get overall status including discovered servers, SERPAPI_KEY presence, and running servers.

**Input**: None

**Example**:
```json
{
  "name": "get_status",
  "arguments": {}
}
```

### 7. `list_pids`
List all registered server PIDs.

**Input**: None

**Example**:
```json
{
  "name": "list_pids",
  "arguments": {}
}
```

### 8. `verify_serpapi_key`
Verify the SERPAPI_KEY by making a test query.

**Input**:
- `timeout` (optional): Timeout in seconds (default: 10.0)

**Example**:
```json
{
  "name": "verify_serpapi_key",
  "arguments": {
    "timeout": 10.0
  }
}
```

## Usage

### Running the MCP Server

Run the unified MCP server via stdio:

```bash
python -m py_mcp_travelplanner.cli mcp
```

Or use the direct script:

```bash
python -m py_mcp_travelplanner.unified_mcp_server
```

### Configuration for Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "travel-planner": {
      "command": "python",
      "args": [
        "-m",
        "py_mcp_travelplanner.cli",
        "mcp"
      ],
      "env": {
        "SERPAPI_KEY": "your-serpapi-key-here"
      }
    }
  }
}
```

### Configuration for Other MCP Clients

The server uses stdio transport, so any MCP client can connect by spawning:

```bash
python -m py_mcp_travelplanner.cli mcp
```

Ensure `SERPAPI_KEY` is set in the environment or in a `.env` file.

## Environment Setup

### Required

- **SERPAPI_KEY**: Required for starting servers that use SerpAPI

Set via:
1. Environment variable: `export SERPAPI_KEY="your-key"`
2. Package `.env` file: `py_mcp_travelplanner/.env`
3. Repo root `.env` file: `.env`

### Optional

Configure logging level:

```bash
python -m py_mcp_travelplanner.cli mcp -v   # INFO level
python -m py_mcp_travelplanner.cli mcp -vv  # DEBUG level
```

## Example Workflows

### Starting All Services

1. Verify SERPAPI_KEY:
```json
{
  "name": "verify_serpapi_key",
  "arguments": {}
}
```

2. Check status:
```json
{
  "name": "get_status",
  "arguments": {}
}
```

3. Start all servers:
```json
{
  "name": "start_all_servers",
  "arguments": {"dry_run": false}
}
```

4. Verify they're running:
```json
{
  "name": "list_pids",
  "arguments": {}
}
```

### Managing Individual Services

Start a specific server:
```json
{
  "name": "start_server",
  "arguments": {"server": "event_server"}
}
```

Check its health:
```json
{
  "name": "health_check",
  "arguments": {"server": "event_server"}
}
```

Stop it when done:
```json
{
  "name": "stop_server",
  "arguments": {"server": "event_server"}
}
```

## PID Tracking

Server PIDs are stored in `.mcp_pids.json` at the repository root. This file tracks:
- Process ID (PID)
- Start timestamp
- Server name

The file is automatically managed by the start/stop tools.

## Comparison with HTTP Control Server

| Feature | MCP Server (`mcp`) | HTTP Server (`serve`) |
|---------|-------------------|----------------------|
| Protocol | MCP (stdio) | HTTP/REST |
| Use Case | AI assistants, automation | Manual control, debugging |
| Transport | Process stdio | TCP socket |
| Authentication | N/A (local process) | None (add if needed) |
| Tools | 8 MCP tools | 6 HTTP endpoints |

Both servers provide similar functionality - choose based on your integration needs.

## Troubleshooting

### "SERPAPI_KEY not found"
Set the key in your environment or `.env` file before starting servers.

### "No servers found to start"
Check that server directories exist under `py_mcp_travelplanner/` with `main.py` files.

### Process won't stop
Increase the `timeout` parameter in `stop_server` calls, or check if processes are zombie/stuck.

### MCP client can't connect
Ensure the command and args are correct in your MCP client configuration.

## Development

To add new management tools:

1. Add a new tool definition in `list_tools()`
2. Add handling logic in `call_tool()`
3. Update this documentation

See `unified_mcp_server.py` for implementation details.

