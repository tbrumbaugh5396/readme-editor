#!/usr/bin/env python3
"""
Test script to verify that the complete structured editor generates clean markdown
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from structured_template import create_readme_template

class MockProjectNameCtrl:
    """Mock control for project name"""
    def GetValue(self):
        return "Test Project"

class MockStructuredEditor:
    """Mock structured editor to simulate the real editor's get_content method"""
    
    def __init__(self):
        self.template_root = create_readme_template()
        self.project_name_ctrl = MockProjectNameCtrl()
        
        # Enable key sections for testing
        for child in self.template_root.children:
            if child.name in ["Table of contents", "Overview", "Installation", "Usage"]:
                child.enabled = True
                if child.name == "Overview":
                    child.content = "This is a comprehensive README editor."
                elif child.name == "Installation":
                    child.content = "Install by running pip install readme-editor."
                elif child.name == "Usage":
                    child.content = "Launch the application by running python readme_editor.py."
            else:
                child.enabled = False
    
    def get_content(self):
        """Get the current content as markdown (mimics the real method)"""
        if self.template_root:
            project_name = self.project_name_ctrl.GetValue() or "My Project"

            # Start with project name as main H1
            content = f"# {project_name}\n\n"

            # Add any root content if present
            if self.template_root.content:
                content += self.template_root.content + "\n\n"

            # Add all child sections, with special handling for Table of Contents
            for child in self.template_root.children:
                if not child.enabled:
                    continue

                if child.name == "Table of contents":
                    # Auto-generate table of contents
                    auto_toc = self.template_root.generate_table_of_contents()

                    # Create TOC section
                    toc_header = "## Table of contents\n\n"

                    if child.content.strip():
                        # Use custom content and add auto-generated TOC
                        toc_content = toc_header + child.content + "\n\n" + auto_toc + "\n"
                    else:
                        # Use auto-generated TOC only
                        toc_content = toc_header + auto_toc + "\n"

                    content += toc_content + "\n"
                else:
                    # Regular section
                    child_content = child.to_markdown()
                    if child_content.strip():
                        content += child_content + "\n"

            return content.rstrip() + "\n"
        else:
            project_name = self.project_name_ctrl.GetValue() or "My Project"
            return f"# {project_name}\n\nNo content available."

def test_complete_structured_editor():
    """Test the complete structured editor output"""
    
    print("Testing complete structured editor content generation...")
    
    # Create a mock structured editor
    editor = MockStructuredEditor()
    
    # Generate the complete content
    content = editor.get_content()
    
    print("Generated Complete Content:")
    print("=" * 60)
    print(content)
    print("=" * 60)
    
    # Check for HTML anchor tags
    has_html_anchors = '<a name=' in content
    
    if has_html_anchors:
        print("❌ FAIL: HTML anchor tags found in complete content")
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '<a name=' in line:
                print(f"Line {i+1}: {line}")
    else:
        print("✅ PASS: No HTML anchor tags found in complete content")
    
    # Check that table of contents is generated properly
    has_toc = "## Table of contents" in content
    has_toc_links = "- [" in content and "](#" in content
    
    if has_toc and has_toc_links:
        print("✅ PASS: Table of contents generated with proper markdown links")
    else:
        print("❌ FAIL: Table of contents not generated properly")
        print(f"Has TOC header: {has_toc}")
        print(f"Has TOC links: {has_toc_links}")
    
    # Check for proper project name
    has_project_title = content.startswith("# Test Project")
    
    if has_project_title:
        print("✅ PASS: Project title generated correctly")
    else:
        print("❌ FAIL: Project title not found at start")
    
    return not has_html_anchors and has_toc and has_toc_links and has_project_title

if __name__ == "__main__":
    success = test_complete_structured_editor()
    print(f"\nOverall Test Result: {'PASS' if success else 'FAIL'}") 