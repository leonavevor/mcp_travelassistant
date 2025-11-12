import argparse
try:
    # Prefer relative import when run as a package
    from .weather_server import mcp
except Exception:
    # Fallback to absolute import when run as a script
    from py_mcp_travelplanner.weather_server.weather_server import mcp


def main():
    parser = argparse.ArgumentParser(description="Weather MCP Server entrypoint")
    parser.add_argument('--transport', choices=['stdio', 'http'], default='stdio', help='Transport type (stdio or http)')
    parser.add_argument('--host', default='127.0.0.1', help='Host for HTTP transport')
    parser.add_argument('--port', type=int, default=8791, help='Port for HTTP transport')
    parser.add_argument('--manifest', action='store_true', help='Print tool manifest and exit')
    args = parser.parse_args()

    if args.manifest:
        # Print the tool manifest/schema for debugging
        import json
        print(json.dumps(mcp.describe_tools(), indent=2))
        return

    if args.transport == 'http':
        print(f"Starting weather-server on http://{args.host}:{args.port}")
        # FastMCP.run() does not accept a 'host' keyword in this project; only pass port
        mcp.run(transport='http', port=args.port)
    else:
        print("Starting weather-server with stdio transport")
        mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
