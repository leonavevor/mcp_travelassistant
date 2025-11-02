#!/usr/bin/env python3
"""
Demo script showing the unified MCP server in action.

This script demonstrates:
1. Service discovery
2. Tool extraction and namespacing
3. Service manifest generation
4. Tool delegation

Run with: python scripts/demo_unified_server.py
"""

import asyncio
import json
from py_mcp_travelplanner import mcp_server


async def main():
    print("=" * 80)
    print("MCP Travel Planner - Unified Server Demo")
    print("=" * 80)
    print()

    # 1. Service Discovery
    print("📡 Step 1: Discovering subservices...")
    print("-" * 80)
    services = mcp_server._discover_subservices()
    print(f"Found {len(services)} services: {', '.join(services)}")
    print()

    # 2. Initialize Service Registry
    print("🔧 Step 2: Initializing service registry...")
    print("-" * 80)
    await mcp_server._initialize_service_registry()
    print(f"✓ Loaded {len(mcp_server._SERVICE_REGISTRY)} services")
    print(f"✓ Registered {len(mcp_server._TOOL_REGISTRY)} tools")
    print()

    # 3. Show Integrated Services
    print("📋 Step 3: Integrated Services & Tools")
    print("-" * 80)
    for service_name, mcp_instance in mcp_server._SERVICE_REGISTRY.items():
        service_tools = [t for t in mcp_server._TOOL_REGISTRY.values() if t['service'] == service_name]
        tool_names = [t['original_name'] for t in service_tools]
        print(f"\n{service_name}:")
        print(f"  Tools ({len(tool_names)}): {', '.join(tool_names)}")
        print(f"  Namespaced names:")
        for tool in service_tools[:3]:  # Show first 3
            print(f"    - {tool['namespaced_name']}")
        if len(service_tools) > 3:
            print(f"    ... and {len(service_tools) - 3} more")
    print()

    # 4. List All Available Tools
    print("🔧 Step 4: Listing all available MCP tools...")
    print("-" * 80)
    tools = await mcp_server.list_tools()
    print(f"Total tools: {len(tools)}")
    
    control_tools = [t for t in tools if '.' not in t.name]
    subservice_tools = [t for t in tools if '.' in t.name]
    
    print(f"\nControl tools ({len(control_tools)}):")
    for tool in control_tools[:5]:
        print(f"  - {tool.name}: {tool.description[:60]}...")
    
    print(f"\nSubservice tools ({len(subservice_tools)}):")
    for tool in subservice_tools[:10]:
        print(f"  - {tool.name}: {tool.description[:60]}...")
    if len(subservice_tools) > 10:
        print(f"  ... and {len(subservice_tools) - 10} more")
    print()

    # 5. Get Service Manifest
    print("📄 Step 5: Generating service manifest...")
    print("-" * 80)
    result = await mcp_server.call_tool("get_service_manifest", {})
    manifest = json.loads(result[0].text)
    
    print(f"Unified Server: {manifest['unified_server']}")
    print(f"Total Services: {manifest['total_services']}")
    print(f"Total Tools: {manifest['total_tools']}")
    print()
    
    print("Services breakdown:")
    for service_name, service_info in manifest['services'].items():
        print(f"  {service_name}: {service_info['tool_count']} tools")
    print()

    # 6. Get Status
    print("📊 Step 6: Getting system status...")
    print("-" * 80)
    result = await mcp_server.call_tool("get_status", {})
    print(result[0].text)
    print()

    # 7. Example Tool Namespacing
    print("🏷️  Step 7: Tool Namespacing Examples")
    print("-" * 80)
    print("Original tool names → Namespaced names:")
    print()
    examples = [
        ("event_server", "search_events", "event.search_events"),
        ("flight_server", "search_flights", "flight.search_flights"),
        ("hotel_server", "search_hotels", "hotel.search_hotels"),
        ("weather_server", "get_weather", "weather.get_weather"),
        ("geocoder_server", "geocode", "geocoder.geocode"),
        ("finance_server", "get_exchange_rates", "finance.get_exchange_rates"),
    ]
    
    for service, original, namespaced in examples:
        if namespaced in mcp_server._TOOL_REGISTRY:
            tool_info = mcp_server._TOOL_REGISTRY[namespaced]
            status = "✓ Registered"
        else:
            status = "✗ Not found"
        print(f"  {original:20} → {namespaced:30} [{status}]")
    print()

    # 8. Summary
    print("=" * 80)
    print("✨ Summary")
    print("=" * 80)
    print(f"✓ Discovered {len(services)} subservices")
    print(f"✓ Loaded {len(mcp_server._SERVICE_REGISTRY)} services successfully")
    print(f"✓ Registered {len(mcp_server._TOOL_REGISTRY)} subservice tools")
    print(f"✓ Total available tools: {len(tools)} (control + subservice)")
    print()
    print("The unified MCP server is ready to use!")
    print("Connect via Claude Desktop or any MCP client to access all travel planning tools.")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())

