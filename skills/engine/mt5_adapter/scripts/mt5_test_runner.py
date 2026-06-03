#!/usr/bin/env python
"""
Deterministic test runner for MT5 Adapter unit tests.

This script invokes pytest to execute the unit test suite for the
Mt5Adapter implementation with a fully mocked MetaTrader5 SDK.
It ensures consistent execution across environments and can be used
in CI pipelines.
"""
import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run pytest on the MT5 adapter test module."""
    test_file = Path(__file__).resolve().parents[1] / "tests" / "test_mt5_adapter.py"
    if not test_file.is_file():
        print("Test file not found:", test_file, file=sys.stderr)
        sys.exit(1)

    # Execute pytest with verbose output
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-v"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print("Tests failed:", result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    run_tests()