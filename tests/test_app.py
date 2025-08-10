#!/usr/bin/env python3
"""
Test script for README Editor
This script will run the application and perform basic validation
"""

import sys
import os


def test_imports():
    """Test that all required modules can be imported"""
    try:
        import wx
        print("✓ wxPython imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import wxPython: {e}")
        return False

    try:
        import markdown
        print("✓ markdown imported successfully")
    except ImportError as e:
        print(f"⚠ markdown not available: {e}")
        print("  Preview will fall back to plain text")

    try:
        from readme_editor import ReadmeEditorApp
        print("✓ ReadmeEditorApp imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ReadmeEditorApp: {e}")
        return False

    try:
        from structured_template import create_readme_template
        print("✓ structured_template imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import structured_template: {e}")
        return False

    return True


def main():
    print("README Editor - Test Script")
    print("=" * 40)

    # Test imports
    if not test_imports():
        print("\n✗ Import tests failed")
        sys.exit(1)

    print("\n✓ All imports successful!")
    print("\nTo run the README Editor:")
    print("python readme_editor.py")
    print("\nFeatures to test:")
    print("- General editor text editing")
    print("- Structured editor section navigation")
    print("- Preview panel toggle (F12 or View menu)")
    print("- File operations (New, Open, Save)")
    print("- Real-time preview updates")


if __name__ == "__main__":
    main()
