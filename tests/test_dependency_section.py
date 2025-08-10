#!/usr/bin/env python3
"""
Test script to verify that the dependency button finds the Dependency section under Project Architecture
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class DependencyTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test dependency section finding
        wx.CallAfter(self.test_dependency_section)
        
        return True
    
    def test_dependency_section(self):
        """Test that dependency button finds the correct section"""
        print("Testing dependency section targeting...")
        
        editor = self.frame.structured_editor
        
        # 1. Find the Dependency section manually to verify it exists
        print(f"\n1. Looking for 'Dependency' section under Project Architecture:")
        dependency_section = self._find_section_by_name(editor.template_root, "Dependency")
        if dependency_section:
            print(f"   ✅ Found 'Dependency' section: {dependency_section.get_full_path()}")
        else:
            print(f"   ❌ 'Dependency' section not found")
            return
        
        # 2. Test the dependency button targeting
        print(f"\n2. Testing dependency button targeting:")
        try:
            # Clear any existing content
            dependency_section.content = ""
            dependency_section.enabled = False
            
            # Trigger the dependencies button
            event = wx.CommandEvent(wx.EVT_BUTTON.typeId)
            event.SetEventObject(editor.auto_dependencies_btn)
            editor.on_auto_generate_dependencies(event)
            
            # Check if the Dependency section was populated
            if dependency_section.content and dependency_section.enabled:
                print(f"   ✅ PASS: Dependency section populated successfully")
                print(f"   Section path: {dependency_section.get_full_path()}")
                print(f"   Content preview: {dependency_section.content[:100]}...")
            else:
                print(f"   ❌ FAIL: Dependency section not populated")
                # Check what section was actually found
                target_sections = ["Dependencies", "Software Dependencies", "Python Libraries", "Install Dependencies", "Dependency"]
                for section_name in target_sections:
                    section = self._find_section_by_name(editor.template_root, section_name)
                    if section and section.content:
                        print(f"   Found content in: {section.get_full_path()}")
                        break
                        
        except Exception as e:
            print(f"   ❌ FAIL: Error testing dependency button: {e}")
        
        # 3. Check tree display
        print(f"\n3. Checking tree display:")
        root_item = editor.tree_ctrl.GetRootItem()
        if root_item.IsOk():
            dependency_found_in_tree = self._find_item_in_tree(editor.tree_ctrl, root_item, "Dependency")
            if dependency_found_in_tree:
                print(f"   ✅ 'Dependency' section visible in tree")
            else:
                print(f"   ❌ 'Dependency' section not visible in tree")
        
        print(f"\nDependency section testing completed!")
        
        # Close after a delay
        wx.CallLater(2000, self.frame.Close)
    
    def _find_section_by_name(self, section, name):
        """Recursively find a section by name"""
        if section.name == name:
            return section
        for child in section.children:
            result = self._find_section_by_name(child, name)
            if result:
                return result
        return None
    
    def _find_item_in_tree(self, tree_ctrl, item, target_name):
        """Recursively find an item in the tree by name"""
        item_text = tree_ctrl.GetItemText(item)
        if target_name in item_text:  # Check if target_name is in the text (handles "Dependency" vs "Dependency (Optional)" etc.)
            return item
        
        child, cookie = tree_ctrl.GetFirstChild(item)
        while child.IsOk():
            result = self._find_item_in_tree(tree_ctrl, child, target_name)
            if result:
                return result
            child, cookie = tree_ctrl.GetNextChild(item, cookie)
        
        return None

if __name__ == "__main__":
    app = DependencyTestApp()
    app.MainLoop() 