"""Unified MCP Server for py_mcp_travelplanner.

This server exposes a unified interface to control all travel planner services
via the Model Context Protocol. It provides tools to start, stop, check health,
and manage all the individual travel planner servers.
"""
from __future__ import annotations

import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from . import cli_handlers

LOG = logging.getLogger("py_mcp_travelplanner.unified_mcp_server")

# Create MCP server instance
mcp = Server("py_mcp_travelplanner_unified")


@mcp.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools for managing travel planner servers."""
    return [
        Tool(
            name="list_servers",
            description="List all discovered travel planner servers",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="start_server",
            description="Start a specific travel planner server",
            inputSchema={
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description": "Name of the server to start (e.g., event_server, flight_server)"
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, only show what would be started without actually starting",
                        "default": False
                    }
                },
                "required": ["server"]
            }
        ),
        Tool(
            name="start_all_servers",
            description="Start all discovered travel planner servers (requires SERPAPI_KEY)",
            inputSchema={
                "type": "object",
                "properties": {
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, only show what would be started without actually starting",
                        "default": False
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="stop_server",
            description="Stop a running server by name or PID",
            inputSchema={
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description": "Server name or numeric PID to stop"
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Timeout in seconds to wait for graceful shutdown",
                        "default": 5.0
                    }
                },
                "required": ["server"]
            }
        ),
        Tool(
            name="health_check",
            description="Check health of a specific server (verifies main.py exists and is readable)",
            inputSchema={
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description": "Name of the server to check"
                    }
                },
                "required": ["server"]
            }
        ),
        Tool(
            name="get_status",
            description="Get overall status including discovered servers and SERPAPI_KEY presence",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="list_pids",
            description="List all registered server PIDs",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="verify_serpapi_key",
            description="Verify that the SERPAPI_KEY is valid by making a test query",
            inputSchema={
                "type": "object",
                "properties": {
                    "timeout": {
                        "type": "number",
                        "description": "Timeout in seconds for the verification request",
                        "default": 10.0
                    }
                },
                "required": []
            }
        )
    ]


@mcp.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls for server management."""

    if name == "list_servers":
        servers = cli_handlers.list_servers()
        return [TextContent(
            type="text",
            text=f"Discovered servers: {', '.join(servers) if servers else 'None'}"
        )]

    elif name == "start_server":
        server = arguments["server"]
        dry_run = arguments.get("dry_run", False)
        env_overrides = None

        # Try to get SERPAPI_KEY for server environment
        serpapi_key = cli_handlers._resolve_serpapi_key()
        if serpapi_key:
            env_overrides = {"SERPAPI_KEY": serpapi_key}

        ok = cli_handlers.start_server(server, dry_run=dry_run, env_overrides=env_overrides)
        result = f"Server '{server}' {'would be started' if dry_run else 'started'}: {ok}"

        if ok and not dry_run:
            pid = cli_handlers.get_registered_pid(server)
            result += f" (PID: {pid})" if pid else ""

        return [TextContent(type="text", text=result)]

    elif name == "start_all_servers":
        dry_run = arguments.get("dry_run", False)
        try:
            results = cli_handlers.start_all_servers(dry_run=dry_run)
            summary = "\n".join([f"  - {name}: {'started' if ok else 'failed'}" for name, ok in results.items()])
            text = f"Start all servers {'(dry-run)' if dry_run else ''}:\n{summary}"
            return [TextContent(type="text", text=text)]
        except RuntimeError as e:
            return [TextContent(type="text", text=f"Error: {e}")]

    elif name == "stop_server":
        server = arguments["server"]
        timeout = arguments.get("timeout", 5.0)

        # Try to parse as PID
        try:
            server_val = int(server)
        except ValueError:
            server_val = server

        result = cli_handlers.stop_server(server_val, timeout=timeout)
        text = f"Stop server '{server}': ok={result.get('ok')}, pid={result.get('pid')}"
        if "error" in result:
            text += f", error={result['error']}"

        return [TextContent(type="text", text=text)]

    elif name == "health_check":
        server = arguments["server"]
        ok = cli_handlers.health_check(server)
        return [TextContent(type="text", text=f"Health check '{server}': {'healthy' if ok else 'unhealthy'}")]

    elif name == "get_status":
        servers = [p.name for p in cli_handlers._find_server_dirs()]
        serpapi = cli_handlers._resolve_serpapi_key()
        pids = cli_handlers.list_registered_pids()

        status_text = f"""Status:
  Discovered servers: {len(servers)} ({', '.join(servers) if servers else 'none'})
  SERPAPI_KEY: {'present' if serpapi else 'missing'}
  Running servers: {len(pids)} ({', '.join(pids.keys()) if pids else 'none'})"""

        return [TextContent(type="text", text=status_text)]

    elif name == "list_pids":
        pids = cli_handlers.list_registered_pids()
        if not pids:
            return [TextContent(type="text", text="No registered server PIDs")]

        pid_text = "Registered PIDs:\n"
        for name, info in pids.items():
            pid_text += f"  - {name}: PID={info.get('pid')}, started={info.get('started_at')}\n"

        return [TextContent(type="text", text=pid_text)]

    elif name == "verify_serpapi_key":
        timeout = arguments.get("timeout", 10.0)
        ok, info = cli_handlers.verify_serpapi_key(timeout=timeout)

        if ok:
            text = f"SERPAPI_KEY verification: SUCCESS\n  HTTP status: {info.get('http_status')}\n  Response keys: {info.get('keys')}"
        else:
            text = f"SERPAPI_KEY verification: FAILED\n  Error: {info.get('error', 'unknown')}"

        return [TextContent(type="text", text=text)]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def serve_mcp():
    """Run the unified MCP server via stdio."""
    LOG.info("Starting unified MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(read_stream, write_stream, mcp.create_initialization_options())


def run_mcp_server():
    """Synchronous entry point for running the MCP server."""
    import asyncio
    asyncio.run(serve_mcp())


if __name__ == "__main__":
    run_mcp_server()

