#!/usr/bin/env python3
"""
Test script to verify that the tree structure shows and updates the project name
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class TreeTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test the tree updates
        wx.CallAfter(self.test_tree_updates)
        
        return True
    
    def test_tree_updates(self):
        """Test that tree structure updates when project name changes"""
        print("Testing tree structure updates...")
        
        # Get the tree control
        tree_ctrl = self.frame.structured_editor.tree_ctrl
        
        # Function to get root item text
        def get_root_text():
            root_item = tree_ctrl.GetRootItem()
            if root_item.IsOk():
                return tree_ctrl.GetItemText(root_item)
            return "No root item"
        
        # 1. Check initial state
        print(f"\n1. Initial tree root:")
        initial_root = get_root_text()
        print(f"   Root text: '{initial_root}'")
        
        # 2. Change project name to something specific
        print(f"\n2. Setting project name to 'Amazing Web App':")
        self.frame.structured_editor.project_name_ctrl.SetValue("Amazing Web App")
        
        # Trigger the project name change event
        event = wx.CommandEvent(wx.EVT_TEXT.typeId)
        event.SetEventObject(self.frame.structured_editor.project_name_ctrl)
        self.frame.structured_editor.on_project_name_changed(event)
        
        updated_root = get_root_text()
        print(f"   Root text: '{updated_root}'")
        
        # 3. Change to another name
        print(f"\n3. Setting project name to 'Super Cool Library':")
        self.frame.structured_editor.project_name_ctrl.SetValue("Super Cool Library")
        
        # Trigger the event again
        event = wx.CommandEvent(wx.EVT_TEXT.typeId)
        event.SetEventObject(self.frame.structured_editor.project_name_ctrl)
        self.frame.structured_editor.on_project_name_changed(event)
        
        final_root = get_root_text()
        print(f"   Root text: '{final_root}'")
        
        # 4. Show tree structure
        print(f"\n4. Current tree structure:")
        self.print_tree_structure(tree_ctrl, tree_ctrl.GetRootItem(), 0)
        
        # Verify results
        print(f"\n--- Test Results ---")
        
        if "Amazing Web App" in updated_root:
            print("✅ PASS: First project name update reflected in tree")
        else:
            print(f"❌ FAIL: First project name not in tree (expected 'Amazing Web App', got '{updated_root}')")
        
        if "Super Cool Library" in final_root:
            print("✅ PASS: Second project name update reflected in tree")
        else:
            print(f"❌ FAIL: Second project name not in tree (expected 'Super Cool Library', got '{final_root}')")
        
        # Check that tree is not empty and has children
        root_item = tree_ctrl.GetRootItem()
        if root_item.IsOk() and tree_ctrl.ItemHasChildren(root_item):
            print("✅ PASS: Tree has children (sections under project name)")
        else:
            print("❌ FAIL: Tree doesn't have proper structure")
        
        print(f"\nTree update testing completed!")
        
        # Close the app after a short delay
        wx.CallLater(3000, self.frame.Close)
    
    def print_tree_structure(self, tree_ctrl, item, level):
        """Recursively print tree structure"""
        if not item.IsOk():
            return
        
        indent = "  " * level
        text = tree_ctrl.GetItemText(item)
        print(f"{indent}- {text}")
        
        # Print children (limit depth to avoid too much output)
        if level < 3:
            child, cookie = tree_ctrl.GetFirstChild(item)
            while child.IsOk():
                self.print_tree_structure(tree_ctrl, child, level + 1)
                child, cookie = tree_ctrl.GetNextChild(item, cookie)

if __name__ == "__main__":
    app = TreeTestApp()
    app.MainLoop() 