#!/bin/bash
# Test script to verify UV MCP configurations work correctly

set -e

echo "=========================================="
echo "MCP UV Configuration Test Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check UV installation
echo -n "Checking UV installation... "
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo -e "${GREEN}✓${NC} ($UV_VERSION)"
else
    echo -e "${RED}✗${NC}"
    echo ""
    echo "UV is not installed. Install with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo ""
echo "=========================================="
echo "Testing UV configurations"
echo "=========================================="
echo ""

# Test 1: Standard PyPI (if published)
echo "Test 1: Standard PyPI"
echo "Command: uv run --with py_mcp_travelplanner --no-project -- python -c \"import py_mcp_travelplanner; print('OK')\""
if uv run --with py_mcp_travelplanner --no-project -- python -c "import py_mcp_travelplanner; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✓ Package available on PyPI${NC}"
else
    echo -e "${YELLOW}⚠ Package not yet published to PyPI (this is expected)${NC}"
fi

echo ""

# Test 2: Test PyPI
echo "Test 2: Test PyPI"
echo "Command: uv run --index https://test.pypi.org/simple --with py_mcp_travelplanner --no-project -- python -c \"import py_mcp_travelplanner; print('OK')\""
if uv run --index https://test.pypi.org/simple --with py_mcp_travelplanner --no-project -- python -c "import py_mcp_travelplanner; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✓ Package available on Test PyPI${NC}"
else
    echo -e "${YELLOW}⚠ Package not yet published to Test PyPI (this is expected)${NC}"
fi

echo ""

# Test 3: List servers command (if package is available)
echo "Test 3: CLI Command Test"
echo "Command: uv run --with py_mcp_travelplanner --no-project -- py_mcp_travelplanner_cli list"
if uv run --with py_mcp_travelplanner --no-project -- py_mcp_travelplanner_cli list 2>/dev/null; then
    echo -e "${GREEN}✓ CLI command works${NC}"
else
    echo -e "${YELLOW}⚠ CLI command failed (package may not be published yet)${NC}"
fi

echo ""
echo "=========================================="
echo "Configuration File Locations"
echo "=========================================="
echo ""

# Detect OS and show config path
case "$(uname -s)" in
    Darwin*)
        CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
        echo "macOS detected"
        echo "Config path: $CONFIG_PATH"
        ;;
    Linux*)
        CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
        echo "Linux detected"
        echo "Config path: $CONFIG_PATH"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        CONFIG_PATH="$APPDATA/Claude/claude_desktop_config.json"
        echo "Windows detected"
        echo "Config path: $CONFIG_PATH"
        ;;
    *)
        echo "Unknown OS"
        CONFIG_PATH=""
        ;;
esac

if [ -n "$CONFIG_PATH" ]; then
    if [ -f "$CONFIG_PATH" ]; then
        echo -e "${GREEN}✓ Config file exists${NC}"
    else
        echo -e "${YELLOW}⚠ Config file does not exist yet${NC}"
        echo ""
        echo "Create it with one of these commands:"
        echo ""
        echo "For Test PyPI:"
        echo "  cp examples/claude_desktop_config_uv_testpypi.json \"$CONFIG_PATH\""
        echo ""
        echo "For PyPI:"
        echo "  cp examples/claude_desktop_config_uv_pypi.json \"$CONFIG_PATH\""
    fi
fi

echo ""
echo "=========================================="
echo "Next Steps"
echo "=========================================="
echo ""
echo "1. Get a SERPAPI key from https://serpapi.com/"
echo "2. Choose a config file:"
echo "   • claude_desktop_config_template.json - Local installation"
echo "   • claude_desktop_config_uv_pypi.json - UV with PyPI"
echo "   • claude_desktop_config_uv_testpypi.json - UV with Test PyPI"
echo ""
echo "3. Copy to Claude Desktop config location"
echo "4. Replace 'your_serpapi_key_here' with your actual key"
echo "5. Restart Claude Desktop"
echo ""
echo "See MCP_CONFIG_README.md for detailed instructions"
echo ""

