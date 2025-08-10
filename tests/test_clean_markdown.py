#!/usr/bin/env python3
"""
Test script to verify that structured editor generates clean markdown without HTML anchor tags
"""

from structured_template import create_readme_template

def test_clean_markdown_generation():
    """Test that structured editor generates clean markdown without HTML anchors"""
    
    # Create a test template
    template = create_readme_template()
    
    # Enable a few sections for testing
    template.enabled = True
    for child in template.children:
        if child.name in ["Overview", "Installation", "Usage"]:
            child.enabled = True
            # Add some test content
            child.content = f"This is test content for {child.name} section."
        else:
            child.enabled = False
    
    # Generate markdown
    markdown_content = template.to_markdown()
    
    print("Generated Markdown Content:")
    print("=" * 50)
    print(markdown_content)
    print("=" * 50)
    
    # Check for HTML anchor tags
    has_html_anchors = '<a name=' in markdown_content
    
    if has_html_anchors:
        print("❌ FAIL: HTML anchor tags found in generated markdown")
        # Show where the anchors are
        lines = markdown_content.split('\n')
        for i, line in enumerate(lines):
            if '<a name=' in line:
                print(f"Line {i+1}: {line}")
    else:
        print("✅ PASS: No HTML anchor tags found in generated markdown")
    
    # Check for proper markdown headers
    has_proper_headers = any(line.startswith('#') and not '<a name=' in line 
                           for line in markdown_content.split('\n'))
    
    if has_proper_headers:
        print("✅ PASS: Proper markdown headers found")
    else:
        print("❌ FAIL: No proper markdown headers found")
    
    return not has_html_anchors and has_proper_headers

if __name__ == "__main__":
    success = test_clean_markdown_generation()
    print(f"\nTest Result: {'PASS' if success else 'FAIL'}") 