# Unified MCP Server Documentation

## Overview

The `py_mcp_travelplanner` unified MCP server provides a **single entry point** to access all travel planning services through the Model Context Protocol (MCP). Instead of running multiple separate MCP servers, you can use one unified server that automatically discovers and integrates all available subservices.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         py_mcp_travelplanner Unified MCP Server             │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Control & Management Tools                  │  │
│  │  - list_servers                                       │  │
│  │  - list_services                                      │  │
│  │  - get_service_manifest                               │  │
│  │  - start_server, stop_server, health_check            │  │
│  │  - get_status, list_pids, verify_serpapi_key          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Integrated Subservice Tools                 │  │
│  │                                                        │  │
│  │  event.search_events                                  │  │
│  │  event.get_event_details                              │  │
│  │  event.list_events                                    │  │
│  │                                                        │  │
│  │  flight.search_flights                                │  │
│  │  flight.get_flight_details                            │  │
│  │  flight.list_flights                                  │  │
│  │                                                        │  │
│  │  hotel.search_hotels                                  │  │
│  │  hotel.get_hotel_details                              │  │
│  │  hotel.list_hotels                                    │  │
│  │                                                        │  │
│  │  weather.get_weather                                  │  │
│  │  weather.get_forecast                                 │  │
│  │                                                        │  │
│  │  geocoder.geocode                                     │  │
│  │  geocoder.reverse_geocode                             │  │
│  │                                                        │  │
│  │  finance.get_exchange_rates                           │  │
│  │  finance.convert_currency                             │  │
│  │                                                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. **Dynamic Service Discovery**
The unified server automatically discovers all available subservices at startup by scanning for server directories with `main.py` files.

### 2. **Tool Namespacing**
All subservice tools are namespaced to avoid conflicts:
- Original: `search_events`
- Namespaced: `event.search_events`

### 3. **Single MCP Interface**
Access all travel planning tools through a single MCP connection, simplifying client configuration.

### 4. **Service Management**
Control and monitor subservices through management tools without leaving the MCP interface.

### 5. **Lazy Initialization**
Subservices are loaded only when needed, reducing startup time and memory usage.

## Available Services

The unified server integrates the following subservices:

| Service | Description | Tools |
|---------|-------------|-------|
| **event_server** | Event search and discovery | `search_events`, `get_event_details`, `list_events` |
| **flight_server** | Flight search and booking | `search_flights`, `get_flight_details`, `list_flights` |
| **hotel_server** | Hotel search and reservations | `search_hotels`, `get_hotel_details`, `list_hotels` |
| **weather_server** | Weather forecasts | `get_weather`, `get_forecast` |
| **geocoder_server** | Location geocoding | `geocode`, `reverse_geocode` |
| **finance_server** | Currency exchange | `get_exchange_rates`, `convert_currency` |

## Control Tools

### Service Discovery

#### `list_services`
Lists all integrated subservices and their available tools.

```python
# Returns:
Integrated Services (6):
  - event_server: 3 tools (search_events, get_event_details, list_events)
  - flight_server: 3 tools (search_flights, get_flight_details, list_flights)
  ...
```

#### `get_service_manifest`
Get detailed JSON manifest of all services and their tools.

```python
# Arguments:
{
  "service": "event_server"  # Optional: filter to specific service
}

# Returns:
{
  "unified_server": "py_mcp_travelplanner_unified",
  "total_services": 6,
  "total_tools": 18,
  "services": {
    "event_server": {
      "tool_count": 3,
      "tools": [
        {
          "name": "event.search_events",
          "original_name": "search_events",
          "description": "Search for events..."
        }
      ]
    }
  }
}
```

### Server Management

#### `list_servers`
Lists all discovered server directories.

#### `start_server`
Start a specific subservice server.

```python
{
  "server": "event_server",
  "dry_run": false
}
```

#### `stop_server`
Stop a running server by name or PID.

```python
{
  "server": "event_server",  # or PID number
  "timeout": 5.0
}
```

#### `health_check`
Check if a server's main.py exists and is readable.

```python
{
  "server": "event_server"
}
```

#### `get_status`
Get overall system status including integrated services and running servers.

```python
# Returns:
Status:
  Discovered servers: 6 (event_server, finance_server, ...)
  Integrated services: 6
  Available tools: 18 subservice tools + 10 control tools
  SERPAPI_KEY: present
  Running servers: 2 (event_server, flight_server)
```

## Using the Unified Server

### 1. Running the Server

```bash
# Via Python module
python -m py_mcp_travelplanner.mcp_server

# Or using the CLI
py-mcp-travel unified
```

### 2. Configuration for Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "travel_planner_local": {
      "command": "python",
      "args": ["-m", "py_mcp_travelplanner.mcp_server"],
      "env": {
        "SERPAPI_KEY": "your-api-key-here"
      }
    }
  }
}
```

### 3. Using Tools

Once connected, you can use any tool with its namespaced name:

```python
# Search for events
event.search_events({
  "query": "concerts",
  "location": "New York",
  "date_filter": "week"
})

# Search for flights
flight.search_flights({
  "departure_id": "JFK",
  "arrival_id": "LAX",
  "outbound_date": "2025-06-15",
  "return_date": "2025-06-20"
})

# Get weather forecast
weather.get_forecast({
  "location": "New York",
  "days": 7
})
```

## Technical Implementation

### Service Registry

The unified server maintains two registries:

1. **_SERVICE_REGISTRY**: Maps service names to their MCP instances
2. **_TOOL_REGISTRY**: Maps namespaced tool names to tool metadata

### Tool Extraction Process

1. **Discovery**: Scan for `*_server` directories with `main.py`
2. **Loading**: Import each server's MCP instance
3. **Extraction**: Call `list_tools()` on each MCP instance
4. **Namespacing**: Prefix tool names with service identifier
5. **Registration**: Store in global registry

### Tool Delegation

When a namespaced tool is called:

1. Look up the tool in `_TOOL_REGISTRY`
2. Get the original tool name and MCP instance
3. Delegate the call to the subservice's MCP instance
4. Return the result to the caller

## Benefits

### For Developers

- **Single Integration Point**: Configure one MCP server instead of six
- **Consistent Interface**: All tools follow the same patterns
- **Easy Discovery**: Browse all available tools in one place
- **Simplified Deployment**: One process to manage

### For AI Agents

- **Unified Context**: Access all travel planning capabilities through one connection
- **Clear Namespacing**: Tool names indicate their domain
- **Rich Metadata**: Service manifest provides comprehensive tool documentation
- **Efficient**: Single connection reduces overhead

### For Operations

- **Centralized Management**: Control all services from one interface
- **Health Monitoring**: Check status of all integrated services
- **Process Control**: Start/stop individual services as needed
- **Resource Efficiency**: Lazy loading and shared runtime

## Troubleshooting

### No Tools Discovered

**Problem**: `list_services` shows 0 integrated services

**Solutions**:
1. Verify subservice directories have `main.py` files
2. Check that subservices import correctly
3. Ensure FastMCP is installed: `pip install mcp`

### Tool Not Found

**Problem**: Tool call returns "Unknown tool"

**Solutions**:
1. Use namespaced tool name (e.g., `event.search_events` not `search_events`)
2. Run `get_service_manifest` to see available tools
3. Check if service loaded successfully with `list_services`

### SERPAPI_KEY Missing

**Problem**: Services can't make API calls

**Solutions**:
1. Set environment variable: `export SERPAPI_KEY=your-key`
2. Add to server configuration
3. Verify with `verify_serpapi_key` tool

## Future Enhancements

- **HTTP Transport**: Support HTTP in addition to stdio
- **Tool Versioning**: Track and manage tool versions
- **Dynamic Reloading**: Hot-reload services without restart
- **Permission System**: Fine-grained access control per tool
- **Monitoring**: Built-in metrics and logging
- **Caching**: Share cache between integrated services

## See Also

- [QUICKSTART.md](../QUICKSTART.md) - Getting started guide
- [README.md](../README.md) - Project overview
- [Runtime Config](RUNTIME_CONFIG_IMPLEMENTATION.md) - Configuration details
- [Individual Server READMEs](../py_mcp_travelplanner/) - Service-specific docs

