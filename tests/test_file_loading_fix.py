#!/usr/bin/env python3
"""
Test script to verify that file loading works correctly in structured editor
without needing to visit the general tab first
"""

import wx
import sys
import os
import tempfile

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class FileLoadingTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Test file loading functionality
        wx.CallAfter(self.test_file_loading)
        
        return True
    
    def test_file_loading(self):
        """Test that file loading works correctly"""
        print("Testing file loading functionality...")
        
        # Create a temporary markdown file with content
        test_content = """# Test Project Name

This is a test project description that should appear in the overview.

## Installation

Install this project by running:

```bash
pip install test-project
```

## Usage

Use this project like this:

```python
import test_project
test_project.run()
```

## Contributing

Please contribute to this project.
"""
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            temp_file_path = f.name
        
        try:
            print(f"\n1. Created test file: {temp_file_path}")
            
            # 2. Start in structured editor (don't visit general tab)
            print(f"\n2. Switching directly to structured editor:")
            self.frame.notebook.SetSelection(1)  # Go directly to structured editor
            current_tab = self.frame.notebook.GetSelection()
            print(f"   Current tab: {'Structured' if current_tab == 1 else 'General'}")
            
            # 3. Check initial state of structured editor (should be default)
            initial_project_name = self.frame.structured_editor.project_name_ctrl.GetValue()
            initial_overview = self.frame.structured_editor.overview_ctrl.GetValue()
            print(f"\n3. Initial structured editor state:")
            print(f"   Project name: '{initial_project_name}'")
            print(f"   Overview: '{initial_overview}'")
            
            # 4. Load the file using the file opening mechanism
            print(f"\n4. Loading file directly into structured editor...")
            with open(temp_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Simulate what the fixed on_open method does
            self.frame.general_editor.load_content(content)
            self.frame.structured_editor.load_content(content)
            self.frame.current_file = temp_file_path
            
            # 5. Check if content was loaded properly
            loaded_project_name = self.frame.structured_editor.project_name_ctrl.GetValue()
            loaded_overview = self.frame.structured_editor.overview_ctrl.GetValue()
            
            print(f"\n5. After loading file:")
            print(f"   Project name: '{loaded_project_name}'")
            print(f"   Overview: '{loaded_overview}'")
            
            # 6. Test tree structure
            print(f"\n6. Checking tree structure:")
            root_item = self.frame.structured_editor.tree_ctrl.GetRootItem()
            if root_item.IsOk():
                root_text = self.frame.structured_editor.tree_ctrl.GetItemText(root_item)
                print(f"   Tree root: '{root_text}'")
                
                # Check if we can find expected sections
                child, cookie = self.frame.structured_editor.tree_ctrl.GetFirstChild(root_item)
                found_sections = []
                while child.IsOk():
                    section_name = self.frame.structured_editor.tree_ctrl.GetItemText(child)
                    found_sections.append(section_name)
                    child, cookie = self.frame.structured_editor.tree_ctrl.GetNextChild(root_item, cookie)
                
                print(f"   Found sections: {found_sections}")
            
            # 7. Verify results
            print(f"\n--- Test Results ---")
            
            # Check if project name was extracted
            if loaded_project_name == "Test Project Name":
                print("✅ PASS: Project name correctly extracted from H1 header")
            else:
                print(f"❌ FAIL: Expected 'Test Project Name', got '{loaded_project_name}'")
            
            # Check if tree root shows project name
            if root_item.IsOk() and self.frame.structured_editor.tree_ctrl.GetItemText(root_item) == "Test Project Name":
                print("✅ PASS: Tree root shows correct project name")
            else:
                print(f"❌ FAIL: Tree root shows incorrect name")
            
            # Check if sections are populated
            expected_sections = ["Overview", "Installation", "Usage", "Contributing"]
            sections_found = all(section in found_sections for section in expected_sections)
            if sections_found:
                print("✅ PASS: Expected sections found in tree")
            else:
                print(f"❌ FAIL: Some expected sections missing. Expected: {expected_sections}, Found: {found_sections}")
            
            # 8. Test that you don't need to visit general tab
            print(f"\n8. Testing that general tab visit is not required:")
            print("   (We loaded directly into structured editor without visiting general tab)")
            if loaded_project_name == "Test Project Name":
                print("✅ PASS: Content loaded without visiting general tab")
            else:
                print("❌ FAIL: Content did not load properly")
            
            print(f"\nFile loading test completed!")
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
                print(f"\nCleaned up temporary file: {temp_file_path}")
            except OSError:
                pass
            
            # Close after a delay
            wx.CallLater(3000, self.frame.Close)

if __name__ == "__main__":
    app = FileLoadingTestApp()
    app.MainLoop() 