#!/bin/bash
# Run all tests in the tests directory

set -e

echo "=========================================="
echo "Running MCP Travel Planner Tests"
echo "=========================================="
echo ""

# Run existing unit tests
echo "1. Running existing unit tests..."
python -m pytest tests/test_cli_handlers.py tests/test_config.py tests/test_pid_lifecycle.py -v

echo ""
echo "2. Running tool delegation fix tests..."
python -m pytest tests/test_tool_fix.py -v -s

echo ""
echo "3. Running comprehensive tool tests..."
python -m pytest tests/test_all_tools.py -v -s

echo ""
echo "4. Running final verification..."
python -m pytest tests/verify_fix.py -v -s

echo ""
echo "=========================================="
echo "All Tests Complete!"
echo "=========================================="

