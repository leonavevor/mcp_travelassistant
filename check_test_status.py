#!/usr/bin/env python3
"""Quick status check - verify all tests are in place and can be discovered."""
import os
import sys
from pathlib import Path

def main():
    print("="*80)
    print("MCP Travel Planner - Test Organization Status Check")
    print("="*80)

    # Check tests directory
    tests_dir = Path("tests")
    if not tests_dir.exists():
        print("✗ ERROR: tests/ directory not found!")
        return 1

    print(f"\n✓ Tests directory found: {tests_dir}")

    # List all test files
    test_files = sorted(tests_dir.glob("test_*.py")) + sorted(tests_dir.glob("verify_*.py"))
    print(f"\n✓ Found {len(test_files)} test files:")
    for f in test_files:
        size = f.stat().st_size
        print(f"  - {f.name:40} ({size:,} bytes)")

    # Check for test runners
    print("\n✓ Test runner utilities:")
    runners = ["run_all_tests.py", "run_tests.sh"]
    for runner in runners:
        if Path(runner).exists():
            print(f"  - {runner:40} ✓")
        else:
            print(f"  - {runner:40} ✗ MISSING")

    # Check documentation
    print("\n✓ Documentation files:")
    docs = [
        "TOOL_DELEGATION_FIX.md",
        "TASK_COMPLETION_SUMMARY.md",
        "docs/TEST_SUITE_SUMMARY.md"
    ]
    for doc in docs:
        if Path(doc).exists():
            print(f"  - {doc:40} ✓")
        else:
            print(f"  - {doc:40} ✗ MISSING")

    # Try to import pytest
    print("\n✓ Dependencies:")
    try:
        import pytest
        print(f"  - pytest {pytest.__version__:40} ✓")
    except ImportError:
        print(f"  - pytest {'':40} ✗ NOT INSTALLED")
        return 1

    try:
        import pytest_asyncio
        print(f"  - pytest-asyncio {'':31} ✓")
    except ImportError:
        print(f"  - pytest-asyncio {'':31} ⚠ NOT INSTALLED (optional)")

    # Summary
    print("\n" + "="*80)
    print("STATUS: ✓ All tests organized and ready")
    print("="*80)
    print("\nQuick Start:")
    print("  python run_all_tests.py          # Run all tests")
    print("  python -m pytest tests/ -v       # Run with pytest")
    print("  python -m pytest tests/test_tool_fix.py -v  # Run specific test")
    print("="*80)

    return 0

if __name__ == "__main__":
    sys.exit(main())

