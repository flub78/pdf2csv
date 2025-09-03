#!/usr/bin/env python3
"""
Test script for pdf2csv functionality.
"""

import os
import subprocess
import sys
from pathlib import Path


def test_help_option():
    """Test the --help option."""
    print("Testing --help option...")
    result = subprocess.run([sys.executable, 'pdf2csv.py', '--help'], 
                          capture_output=True, text=True)
    if result.returncode == 0 and 'Convert PDF bank statements' in result.stdout:
        print("✓ --help option works correctly")
        return True
    else:
        print("✗ --help option failed")
        return False


def test_version_option():
    """Test the --version option."""
    print("Testing --version option...")
    result = subprocess.run([sys.executable, 'pdf2csv.py', '--version'], 
                          capture_output=True, text=True)
    if result.returncode == 0 and '1.0.0' in result.stdout:
        print("✓ --version option works correctly")
        return True
    else:
        print("✗ --version option failed")
        return False


def test_no_files():
    """Test behavior when no files are provided."""
    print("Testing behavior with no files...")
    result = subprocess.run([sys.executable, 'pdf2csv.py'], 
                          capture_output=True, text=True)
    if result.returncode != 0 and 'No PDF files specified' in result.stdout:
        print("✓ Correctly handles no files provided")
        return True
    else:
        print("✗ Failed to handle no files correctly")
        return False


def main():
    """Run basic tests."""
    print("Running basic tests for pdf2csv.py...")
    print("=" * 50)
    
    # Change to the script directory
    os.chdir(Path(__file__).parent.parent)
    
    tests = [
        test_help_option,
        test_version_option,
        test_no_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All basic tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
