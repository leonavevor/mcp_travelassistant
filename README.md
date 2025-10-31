# MCP Travel Planner

**A unified MCP (Model Context Protocol) server providing a single entry point to comprehensive travel planning services.**

This project implements ONE unified MCP server that orchestrates multiple travel-related backend services (flights, hotels, weather, geocoding, events, finance). MCP clients like Claude Desktop connect to a single server interface and access all travel planning capabilities through it.

## Key Features

- **Single MCP Server Entry Point**: One unified server (`mcp_server.py`) for all travel services
- **Service Orchestration**: Manages multiple backend services through one interface  
- **MCP Tools**: Expose travel planning capabilities via Model Context Protocol
- **Claude Desktop Integration**: Ready-to-use configuration for Claude Desktop
- **Modular Backend**: Each service runs independently but is coordinated by the unified server

## What You Need to Know

**This is a unified MCP server - you connect to ONE server that provides ALL travel services.**

- **MCP Client Config**: Use `.mcp_server_config.json` or `claude_desktop_config_template.json`
- **Quick Setup**: See [QUICKSTART_MCP.md](QUICKSTART) for Claude Desktop integration
- **Implementation Details**: See [MCP_IMPLEMENTATION_SUMMARY.md](MCP_IMPLEMENTATION_SUMMARY.md)

**Two Configuration Files (Different Purposes)**:
1. **`.mcp_server_config.json`** → For MCP clients (Claude Desktop) to connect to the server
2. **`mcp_config.json`** → For the server to manage backend services internally

## Architecture

```
MCP Client (Claude Desktop) 
        ↓ (stdio)
Unified MCP Server (single entry point)
        ↓ (orchestrates)
Backend Services (flight, hotel, weather, geocoder, finance, events)
```

Status
- Prototype / Proof-of-Concept. Intended for local development, experimentation, and as a reference implementation for orchestration patterns.

Key concepts
- Modular microservice-style servers implemented as small Python scripts under `py_mcp_travelplanner/`.
- Each service lives in its own folder (for example `flight_server/`, `hotel_server/`, `weather_server/`) with a `main.py` or server entrypoint.
- A small CLI and control server are provided for orchestration and to demonstrate inter-service interactions.

Contents (not exhaustive)
- `py_mcp_travelplanner/` — main package containing CLI, control server and per-service folders.
  - `flight_server/`, `hotel_server/`, `weather_server/`, `geocoder_server/`, `event_server/`, `finance_server/` — example service implementations.
- `requirements.txt` — pinned runtime/dev dependencies used by the project (single (root) source of truth is recommended).
- `tests/` — pytest-based unit tests and lifecycle tests.

Quick start (local development)

Prerequisites
- Linux / macOS / Windows with WSL
- Python 3.12.1 or later is recommended for development here, but the project should be constrained to exclude Python 4.0 to remain compatible with dependencies that only declare <4.0 support (see Development Notes).

Recommended: create and use a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install dependencies

Option A — pip (quick)

```bash
pip install -r requirements.txt
```

Option B — poetry (if you prefer pyproject/poetry workflows)

```bash
poetry install
```

Running services

Each server folder contains a runnable entrypoint (usually `main.py`). From the repository root you can start any server directly with Python. For example:

```bash
# run the flight server
python py_mcp_travelplanner/flight_server/main.py

# run the weather server
python py_mcp_travelplanner/weather_server/main.py

# run the control server (if present)
python py_mcp_travelplanner/control_server.py
```

Note: some servers may expect environment variables or API keys; check the server's README under the corresponding server folder (for example `flight_server/flights_server_readme.md`) for provider-specific setup.

CLI

A simple CLI is available under `py_mcp_travelplanner/cli.py` and `py_mcp_travelplanner/cli_handlers.py`. You can run the CLI script to access helper commands used in development:

```bash
python -m py_mcp_travelplanner.cli
```

(If the package isn't installed as a module, run the file directly: `python py_mcp_travelplanner/cli.py`.)

Unified MCP Server — Single Entry Point Architecture

This project provides **ONE unified MCP server** that acts as a single entry point to all travel planner services. The server is located at `py_mcp_travelplanner/mcp_server.py` and orchestrates all backend services (flights, hotels, weather, geocoding, events, finance) through a single Model Context Protocol interface.

Architecture Overview
- **Single MCP Server**: One unified server exposing all travel planning capabilities
- **Service Orchestration**: The MCP server manages and coordinates multiple backend services
- **Unified Interface**: MCP clients connect to one server and access all travel services through it

MCP Server Configuration

The repository includes a ready-to-use MCP server configuration file at `.mcp_server_config.json`:

```json
{
  "mcpServers": {
    "travel-planner": {
      "command": "python",
      "args": ["-m", "py_mcp_travelplanner.mcp_server"],
      "cwd": "/path/to/mcp_travelplanner",
      "env": {
        "PYTHONPATH": "/path/to/mcp_travelplanner"
      }
    }
  }
}
```

Update the `cwd` and `PYTHONPATH` values to match your installation directory.

What the unified MCP server exposes
- **Tools**: `list_servers`, `start_server`, `start_all_servers`, `stop_server`, `health_check`, `get_status`, `list_pids`, `verify_serpapi_key`
- **Services**: event_server, finance_server, flight_server, geocoder_server, hotel_server, weather_server
- Each tool accepts a JSON-like arguments object and returns TextContent responses

Environment variables
- **SERPAPI_KEY**: Required for flight_server operations. Set in your environment before starting the MCP server.

Running the MCP server (stdio)

The unified MCP server runs via stdio transport and can be used with any MCP-compatible client.

Method 1: Direct execution

```bash
# Start the unified MCP server
python -m py_mcp_travelplanner.mcp_server

# Or use the CLI helper
python -m py_mcp_travelplanner.cli mcp
```

Method 2: Configure in Claude Desktop (or other MCP client)

1. Locate your Claude Desktop config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the travel-planner MCP server:

```json
{
  "mcpServers": {
    "travel-planner": {
      "command": "python",
      "args": ["-m", "py_mcp_travelplanner.mcp_server"],
      "cwd": "/absolute/path/to/mcp_travelplanner",
      "env": {
        "PYTHONPATH": "/absolute/path/to/mcp_travelplanner",
        "SERPAPI_KEY": "your_key_here_if_needed"
      }
    }
  }
}
```

3. Restart Claude Desktop

4. The travel-planner tools will be available in your Claude conversations

Available MCP Tools

When connected to the unified MCP server, you'll have access to these tools:

- **list_servers**: List all available travel service backends
- **start_server**: Start a specific service (event, flight, hotel, weather, etc.)
- **start_all_servers**: Start all services at once
- **stop_server**: Stop a running service by name or PID
- **health_check**: Verify a service is healthy and ready
- **get_status**: Get overall system status and running services
- **list_pids**: List all running service process IDs
- **verify_serpapi_key**: Test if SERPAPI_KEY is configured correctly

Tool call JSON examples (conceptual)

When calling a tool via an MCP client you will call the tool by name and pass the corresponding arguments object. The exact outer envelope depends on the MCP client library you use; below are the argument payloads for the most common operations (these are the values the MCP server expects in the `arguments` parameter of a tool call):

- Start a server (dry run):

```json
{ "server": "flight_server", "dry_run": true }
```

- Start a server (actual start):

```json
{ "server": "flight_server", "dry_run": false }
```

- Start all servers (dry run):

```json
{ "dry_run": true }
```

- Stop a server (by name):

```json
{ "server": "flight_server", "timeout": 5.0 }
```

- Stop a server (by PID):

```json
{ "server": 12345, "timeout": 5.0 }
```

- Health check:

```json
{ "server": "flight_server" }
```

- Get overall status (no arguments):

```json
{}
```

Expected responses
- The server returns an array of TextContent objects (the `mcp` library encodes this). When using an MCP client, you should inspect the returned text field(s). For example a `get_status` call may return a single element whose `text` contains a human-readable status summary.

HTTP control server (concrete, scriptable)

For convenience there is a small HTTP control server (`py_mcp_travelplanner/control_server.py`) that wraps a subset of the MCP server functionality and exposes simple HTTP endpoints. This is recommended for quick scripting and interactive use.

Start the control server (background):

```bash
python py_mcp_travelplanner/control_server.py
# or, using the CLI helper
python -m py_mcp_travelplanner.cli serve --host 127.0.0.1 --port 8787
```

Useful curl examples

- Get status (discovered servers + SERPAPI presence):

```bash
curl -s http://127.0.0.1:8787/status | jq
```

- Health check for a server:

```bash
curl -s "http://127.0.0.1:8787/health?server=flight_server" | jq
```

- Start a single server (dry run):

```bash
curl -X POST "http://127.0.0.1:8787/start?server=flight_server&dry=true" | jq
```

- Start all servers (actual start):

```bash
curl -X POST "http://127.0.0.1:8787/start_all?dry=false" | jq
```

- Stop a server by name:

```bash
curl -X POST "http://127.0.0.1:8787/stop?server=flight_server" | jq
```

- List registered PIDs:

```bash
curl -s http://127.0.0.1:8787/pids | jq
```

- Verify SERPAPI_KEY (performs a test request using the configured key):

```bash
curl -X POST http://127.0.0.1:8787/test_key | jq
```

Example JSON config file (optional)

If you prefer to keep a small JSON file describing which servers to start and any environment overrides, here's a suggested format you can use in your own scripts. The project currently does not read this file automatically — it's a spec you can adopt for automation scripts that call the HTTP control server or an MCP client.

mcp_config.json

```json
{
  "servers": [
    {"name": "flight_server", "env": {"SERPAPI_KEY": "${SERPAPI_KEY}"}},
    {"name": "weather_server"}
  ],
  "start_all": {"dry_run": false}
}
```

A small Python example showing how to use the HTTP control server

```python
import requests

BASE = "http://127.0.0.1:8787"

# get status
print(requests.get(f"{BASE}/status").json())

# start flight server (dry-run)
print(requests.post(f"{BASE}/start?server=flight_server&dry=true").json())

# start all
print(requests.post(f"{BASE}/start_all?dry=false").json())

# verify serpapi
print(requests.post(f"{BASE}/test_key").json())
```

Runtime Configuration (mcp_config.json)

The file `mcp_config.json` at the repository root is used for **internal runtime orchestration** of backend services. This is separate from the MCP server configuration above.

Purpose: Define which backend services to start and their runtime settings
Location: `/mcp_config.json` (repository root)

This repository uses a single, authoritative runtime configuration file:

```json
{
  "name": "travel-planner",
  "servers": [
    { "name": "event_server" },
    { "name": "finance_server" },
    { "name": "flight_server" },
    { "name": "geocoder_server" },
    { "name": "hotel_server" },
    { "name": "weather_server" }
  ],
  "start_all": { "dry_run": true }
}
```

This config is used by:
- The HTTP control server for orchestration
- The `run_mcp_from_config.py` runner script for batch operations

Note: This is NOT the MCP server config. The MCP server config (`.mcp_server_config.json`) is for MCP clients to connect to the unified server.

Why a single config?
- Centralized orchestration: keep server names and env overrides in one place.
- Reproducible local dev and CI: commit one config and share it across your
  team or CI jobs.
- Simple automation: the included runner script (`scripts/run_mcp_from_config.py`)
  consumes this single file and applies it via the HTTP control server or the
  local handler fallback.

Schema (recommended)
- Root object with keys:
  - `servers`: array of objects describing servers to manage
    - each server object fields:
      - `name` (string, required): server folder / identifier (e.g. "flight_server")
      - `env` (object, optional): mapping of environment variables to values
      - `dry_run` (boolean, optional): override to start this server in dry-run mode
  - `start_all` (object, optional): behavior for starting all servers
    - `dry_run` (boolean, optional): default dry-run flag used by runner when starting all

Recommended strict example (`mcp_config.json`)

```json
{
  "servers": [
    {
      "name": "flight_server",
      "env": {
        "SERPAPI_KEY": "${SERPAPI_KEY}"
      }
    },
    {
      "name": "weather_server"
    }
  ],
  "start_all": {
    "dry_run": false
  }
}
```

How the runner uses the unified config
- Script: `scripts/run_mcp_from_config.py` (included in this repo)
- Behavior:
  1. The runner attempts to contact the local HTTP control server at
     `127.0.0.1:8787` (the endpoint started by
     `python -m py_mcp_travelplanner.cli serve` or by running
     `py_mcp_travelplanner/control_server.py`). If reachable the runner will
     POST to the control server endpoints to start/stop/check servers.
  2. If the HTTP control server is not reachable or `requests` is not
     available, the runner falls back to directly importing
     `py_mcp_travelplanner.cli_handlers` and invoking the local helper
     functions (`start_server`, `start_all_servers`, etc.).
  3. The runner respects `dry_run` values: per-server `dry_run` overrides a
     global `start_all.dry_run` value. Command-line flags `--dry-run` and
     `--no-dry-run` can force an override when running the script.

Runner usage (concrete commands)

1) Start the HTTP control server (recommended):

```bash
# foreground (use Ctrl-C to stop)
python py_mcp_travelplanner/control_server.py

# or start via the CLI helper (same server)
python -m py_mcp_travelplanner.cli serve --host 127.0.0.1 --port 8787
```

2) Run the unified config with the runner:

```bash
# Dry-run: show what would be started (honors config's dry_run values)
python scripts/run_mcp_from_config.py --config mcp_config.json --dry-run

# Start the configured servers (force actual start)
python scripts/run_mcp_from_config.py --config mcp_config.json --no-dry-run

# Use a different control host/port if needed
python scripts/run_mcp_from_config.py --config mcp_config.json --http-host 0.0.0.0 --http-port 8787
```

Runner behavior notes and best practices
- Environment overrides: the runner will forward the `env` mapping to the local
  handler functions when using the fallback path. If you need the runner to
  actually spawn subprocesses with those environment variables applied, ask me
  and I will extend the runner to spawn subprocesses and inject `env` into the
  child's environment.
- Keep `mcp_config.json` under version control for reproducible development
  and CI. You can maintain environment-variable placeholders (for example
  `${SERPAPI_KEY}`) and populate them at runtime using your preferred secrets
  mechanism or by exporting variables into your shell before running the
  control server/runner.
- Use a separate `mcp_config.local.json` or similar for machine-local overrides
  and do not commit secrets.

Consolidation reminder

- After migrating server-level metadata to the root `pyproject.toml` and
  consolidating runtime configuration into `mcp_config.json`, remove or
  archive any per-service `pyproject.toml` files. The repository should have a
  single root `pyproject.toml` and one `mcp_config.json` to configure runtime
  orchestration for all services.

Tests

Run the test suite with pytest:

```bash
# Run all tests
pytest -q

# Run MCP server tests specifically
pytest tests/test_mcp_server.py -v

# Run with coverage
pytest --cov=py_mcp_travelplanner --cov-report=html
```

**Test Coverage**:
- **MCP Server Tests**: 25 tests covering all 8 tools, initialization, and workflows
- See [MCP Server Test Documentation](docs/MCP_SERVER_TESTS.md) for detailed test information

Development notes (important)

1) Consolidate pyproject files
- The repository currently contains service-level metadata and possibly extra `pyproject.toml` files inside server folders. For a single-source-of-truth dependency management approach, consolidate those service-level `pyproject.toml` contents into the root `pyproject.toml` and remove or archive the per-server `pyproject.toml` files. This simplifies CI, local dependency installation, and version pinning.

2) Harmonize shared dependencies (requests example)
- Several service folders may declare their own `requests` version. To avoid mismatched runtime behavior, pin `requests` at the root `pyproject.toml` (or `requirements.txt`) to a single compatible version range and update any server-specific files to rely on the root manifest.

3) Python compatibility and dependency constraints
- Some dependencies in the ecosystem (for example `openapi-pydantic`) declare compatibility for Python versions `<4.0,>=3.8`. To remain compatible with such packages while still using modern Python, set the project Python requirement to a range that excludes Python 4.0. For example in `pyproject.toml` set:

```toml
python = ">=3.12.1,<4.0"
```

This avoids dependency resolution errors if someone installs or runs the project on Python 4.x while the dependencies do not declare support for it.

4) Harmonize dependency versions across the monorepo
- When merging per-server manifests, ensure shared libraries (requests, aiohttp, pydantic, etc.) are pinned consistently. Run a dependency resolver (pip-tools, poetry) and test local execution after changes.

Troubleshooting

- If a server fails to start due to missing environment variables or API keys, check the server folder README for provider-specific instructions.
- If you hit dependency resolution errors, run `pip check` or `poetry lock` to see conflicts and adjust the root manifest accordingly.

Contributing

- Fork the repository, create a feature branch, and open a pull request against the main branch.
- Keep changes focused: if you're changing dependencies, update `pyproject.toml`/`requirements.txt` and add a short rationale in the PR summary.
- Run tests locally and ensure linting passes before opening a PR.

License

- See the `LICENSE` file in the repository root.

Acknowledgements

- This repository is a learning / POC project showcasing modular service layouts, simple orchestration, and packaging considerations for small multi-service Python projects.

Contact

- For questions or help, open an issue in this repository with details about your environment and the problem you're encountering.

--

(Developer notes: if you want, I can also help consolidate per-server `pyproject.toml` files into the root `pyproject.toml`, harmonize `requests` versions across the repo, and adjust the `python` range to `">=3.12.1,<4.0"` to avoid the `openapi-pydantic` compatibility issue.)
