#!/usr/bin/env python3
"""Simple test runner to verify all tests can be executed."""
import subprocess
import sys

def run_test(test_file, description):
    """Run a single test file and report results."""
    print(f"\n{'='*80}")
    print(f"Running: {description}")
    print(f"File: {test_file}")
    print('='*80)
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', test_file, '-v'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {description} PASSED")
            return True
        else:
            print(f"✗ {description} FAILED")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {description} TIMEOUT")
        return False
    except Exception as e:
        print(f"✗ {description} ERROR: {e}")
        return False

def main():
    """Run all test suites."""
    print("="*80)
    print("MCP Travel Planner - Test Suite Runner")
    print("="*80)
    
    tests = [
        ('tests/test_cli_handlers.py', 'CLI Handlers Tests'),
        ('tests/test_config.py', 'Configuration Tests'),
        ('tests/test_pid_lifecycle.py', 'PID Lifecycle Tests'),
        ('tests/test_tool_fix.py', 'Tool Delegation Fix Tests'),
        ('tests/test_all_tools.py', 'Comprehensive Tool Tests'),
        ('tests/verify_fix.py', 'Final Verification Tests'),
    ]
    
    results = []
    for test_file, description in tests:
        success = run_test(test_file, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} - {description}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
        return 0
    else:
        print(f"\n✗ {total - passed} test suite(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

