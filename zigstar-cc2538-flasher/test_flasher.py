#!/usr/bin/env python3
"""
Test script for ZigStar CC2538 Flasher
"""

import os
import sys
import subprocess

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import socket
        import argparse
        import subprocess
        import requests
        from pathlib import Path
        print("✓ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_cc2538_bsl():
    """Test if cc2538-bsl tool is available"""
    try:
        result = subprocess.run(
            ["python3", "-m", "cc2538_bsl.cc2538_bsl", "--help"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ cc2538-bsl tool is available")
            return True
        else:
            print("✗ cc2538-bsl tool not working properly")
            return False
    except Exception as e:
        print(f"✗ Error testing cc2538-bsl: {e}")
        return False

def test_flasher_script():
    """Test if the flasher script exists and is executable"""
    script_path = "/usr/bin/zigstar-flasher"
    if os.path.exists(script_path):
        if os.access(script_path, os.X_OK):
            print("✓ ZigStar flasher script exists and is executable")
            return True
        else:
            print("✗ ZigStar flasher script exists but is not executable")
            return False
    else:
        print("✗ ZigStar flasher script not found")
        return False

def test_web_interface():
    """Test if the web interface script exists and is executable"""
    script_path = "/usr/bin/web-interface.py"
    if os.path.exists(script_path):
        if os.access(script_path, os.X_OK):
            print("✓ Web interface script exists and is executable")
            return True
        else:
            print("✗ Web interface script exists but is not executable")
            return False
    else:
        print("✗ Web interface script not found")
        return False

def test_requests_library():
    """Test if the requests library is working"""
    try:
        import requests
        # Test a simple request
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✓ Requests library is working correctly")
            return True
        else:
            print("✗ Requests library test failed")
            return False
    except Exception as e:
        print(f"✗ Error testing requests library: {e}")
        return False

def test_flasher_help():
    """Test if the flasher script shows help"""
    try:
        result = subprocess.run(
            ["zigstar-flasher", "--help"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and "ZigStar CC2538 Flasher" in result.stdout:
            print("✓ Flasher script help is working")
            return True
        else:
            print("✗ Flasher script help not working properly")
            return False
    except Exception as e:
        print(f"✗ Error testing flasher help: {e}")
        return False

def main():
    """Run all tests"""
    print("ZigStar CC2538 Flasher - Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_requests_library,
        test_cc2538_bsl,
        test_flasher_script,
        test_web_interface,
        test_flasher_help
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The add-on is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
