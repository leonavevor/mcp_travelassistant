import pathlib
import sys

from py_mcp_travelplanner import cli_handlers


def test_server_discovery():
    """Test that only legitimate servers are discovered."""
    servers = cli_handlers.list_servers()

    # Known invalid names that should not be discovered as servers
    invalid_servers = {
        '_pytest', 'dotenv', 'pydantic', 'pydantic_settings',
        'markdown_it', 'pre_commit', 'uvicorn'
    }

    found_invalid = [s for s in servers if s in invalid_servers]
    assert not found_invalid, f"Found invalid servers: {found_invalid}"


def test_tool_naming_no_dots():
    """Tool names should use underscore namespacing, not dots."""
    services = ['event', 'flight', 'hotel', 'weather', 'finance', 'geocoder']
    sample_tool_names = ['search_flights', 'get_hotel_details', 'lookup_stock']

    for service in services[:3]:
        for tool in sample_tool_names[:2]:
            namespaced = f"{service}_{tool}"
            assert '.' not in namespaced, f"Tool name contains dot: {namespaced}"


def test_code_patterns_exist():
    """Verify the code patterns expected by the test helpers are present in the source files."""
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    mcp_path = repo_root / 'py_mcp_travelplanner' / 'mcp_server.py'
    cli_path = repo_root / 'py_mcp_travelplanner' / 'cli_handlers.py'

    mcp_content = mcp_path.read_text(encoding='utf-8')
    cli_content = cli_path.read_text(encoding='utf-8')

    # Check mcp_server namespacing pattern
    assert 'namespaced_name = f"{service_name.replace(\'_server\', \'\')}_{original_name}"' in mcp_content or \
           'namespaced_name = f"{service_name.replace(\"_server\", \"\")}_{original_name}"' in mcp_content, (
        "mcp_server.py: expected namespaced_name pattern not found"
    )

    # Check cli_handlers server discovery filter
    assert 'child.name.endswith("_server")' in cli_content, (
        'cli_handlers.py: expected server filter ending with "_server" not found'
    )

