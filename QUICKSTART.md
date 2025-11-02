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

Once connected, you have access to **10 control tools** and **18+ subservice tools**:

### Control & Management Tools

| Tool | Description |
|------|-------------|
| `list_services` | List all integrated subservices and their tools |
| `get_service_manifest` | Get detailed JSON manifest of all services |
| `get_status` | Get overall system status and integrated services |
| `list_servers` | List all available travel service backends |
| `start_server` | Start a specific service (flight, hotel, weather, etc.) |
| `stop_server` | Stop a running service |
| `health_check` | Check if a service is healthy |
| `list_pids` | List running service process IDs |
| `verify_serpapi_key` | Test SERPAPI_KEY configuration |

### Integrated Subservice Tools

All travel planning tools are available through the unified server with namespaced names:

| Service | Tools | Description |
|---------|-------|-------------|
| **event** | `event.search_events`, `event.get_event_details`, `event.list_events` | Event search and discovery |
| **flight** | `flight.search_flights`, `flight.get_flight_details`, `flight.list_flights` | Flight search and booking |
| **hotel** | `hotel.search_hotels`, `hotel.get_hotel_details`, `hotel.list_hotels` | Hotel reservations |
| **weather** | `weather.get_weather`, `weather.get_forecast` | Weather forecasts |
| **geocoder** | `geocoder.geocode`, `geocoder.reverse_geocode` | Location geocoding |
| **finance** | `finance.get_exchange_rates`, `finance.convert_currency` | Currency exchange |

## Example Usage in Claude

Once configured, you can ask Claude things like:

**Service Management:**
- "List all available travel services"
- "Show me the service manifest"
- "What's the current status of the travel planner?"
- "Check the health of the flight server"

**Direct Travel Queries:**
- "Search for concerts in New York next week" (uses `event.search_events`)
- "Find flights from JFK to LAX on June 15th" (uses `flight.search_flights`)
- "What's the weather forecast for Paris?" (uses `weather.get_forecast`)
- "Find hotels in San Francisco for next month" (uses `hotel.search_hotels`)
- "Convert 100 USD to EUR" (uses `finance.convert_currency`)

Claude will automatically use the appropriate namespaced tools to fulfill your requests.

## Testing the Server Directly

You can test the server without Claude:

```bash
# Start the server directly (stdio mode)
python -m py_mcp_travelplanner.mcp_server

# Or via CLI
python -m py_mcp_travelplanner.cli mcp
```

## Advanced Usage: Multi-Server Orchestration & HTTP API

### Launch All Servers from Config

You can launch all backend servers (weather, event, hotel, flight, finance, geocoder) with a single command using the unified launcher script:

```bash
python scripts/run_mcp_from_config.py --config runtime_config.yaml
```

Example config (runtime_config.yaml):
```yaml
servers:
  weather:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8791
  event:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8796
  hotel:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8795
  flight:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8793
  finance:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8792
  geocoder:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8794
SERPAPI_KEY: "your_serpapi_key_here"
```

### HTTP/stdio Options and Manifest

Each server can be started with stdio (default) or HTTP transport, and exposes a manifest for tool discovery:

```bash
# Start weather server with HTTP API
python -m py_mcp_travelplanner.weather_server.main --transport http --host 127.0.0.1 --port 8791

# Print tool manifest/schema for debugging
python -m py_mcp_travelplanner.weather_server.main --manifest
```

### Integration Testing: HTTP Endpoints & Manifest

You can test HTTP endpoints and manifest output for any server:

```bash
curl http://127.0.0.1:8791/manifest
```

You can also write integration tests in pytest to verify HTTP endpoints and manifest output. See the 'tests/' folder for examples.

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
