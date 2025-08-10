#!/usr/bin/env python3
"""
Debug test for Overview in tree
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class DebugApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Debug tree structure
        wx.CallAfter(self.debug_tree)
        
        return True
    
    def debug_tree(self):
        """Debug the tree structure"""
        print("Debugging tree structure...")
        
        editor = self.frame.structured_editor
        tree_ctrl = editor.tree_ctrl
        
        print(f"Template root: {editor.template_root}")
        print(f"Template root name: {editor.template_root.name if editor.template_root else 'None'}")
        
        # Check current tree structure
        root_item = tree_ctrl.GetRootItem()
        if root_item.IsOk():
            print(f"Root item text: '{tree_ctrl.GetItemText(root_item)}'")
            
            # List all children
            child, cookie = tree_ctrl.GetFirstChild(root_item)
            children = []
            while child.IsOk():
                child_text = tree_ctrl.GetItemText(child)
                children.append(child_text)
                child, cookie = tree_ctrl.GetNextChild(root_item, cookie)
            
            print(f"Children ({len(children)}): {children}")
            
            # Check if Overview is there
            if "Overview" in children:
                print("✅ Overview found in tree!")
            else:
                print("❌ Overview NOT found in tree")
                print("Forcing tree refresh...")
                
                # Manually trigger refresh
                editor.refresh_tree_root()
                
                # Check again
                child, cookie = tree_ctrl.GetFirstChild(root_item)
                new_children = []
                while child.IsOk():
                    child_text = tree_ctrl.GetItemText(child)
                    new_children.append(child_text)
                    child, cookie = tree_ctrl.GetNextChild(root_item, cookie)
                
                print(f"After refresh ({len(new_children)}): {new_children}")
                
                if "Overview" in new_children:
                    print("✅ Overview found after manual refresh!")
                else:
                    print("❌ Overview still missing after refresh")
        
        # Close after a delay
        wx.CallLater(3000, self.frame.Close)

if __name__ == "__main__":
    app = DebugApp()
    app.MainLoop() 