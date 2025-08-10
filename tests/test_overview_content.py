#!/usr/bin/env python3
"""
Test script to verify that overview content appears correctly after project name
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class OverviewTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test overview functionality
        wx.CallAfter(self.test_overview_functionality)
        
        return True
    
    def test_overview_functionality(self):
        """Test that overview content works correctly"""
        print("Testing overview content functionality...")
        
        # Get the structured editor
        editor = self.frame.structured_editor
        
        # 1. Set project name and overview
        print(f"\n1. Setting project name and overview:")
        editor.project_name_ctrl.SetValue("Amazing Library")
        
        overview_text = "This is an amazing library that does incredible things for developers."
        editor.overview_ctrl.SetValue(overview_text)
        
        # Trigger events to save the content
        name_event = wx.CommandEvent(wx.EVT_TEXT.typeId)
        name_event.SetEventObject(editor.project_name_ctrl)
        editor.on_project_name_changed(name_event)
        
        overview_event = wx.CommandEvent(wx.EVT_TEXT.typeId)
        overview_event.SetEventObject(editor.overview_ctrl)
        editor.on_overview_changed(overview_event)
        
        print(f"   Project name: '{editor.project_name_ctrl.GetValue()}'")
        print(f"   Overview: '{editor.overview_ctrl.GetValue()}'")
        
        # 2. Generate markdown content
        print(f"\n2. Generated markdown content:")
        content = editor.get_content()
        print("=" * 60)
        print(content[:300] + "..." if len(content) > 300 else content)
        print("=" * 60)
        
        # 3. Check tree structure
        print(f"\n3. Tree structure:")
        tree_ctrl = editor.tree_ctrl
        root_item = tree_ctrl.GetRootItem()
        if root_item.IsOk():
            root_text = tree_ctrl.GetItemText(root_item)
            print(f"   Root: '{root_text}'")
            
            # Show first few children
            child, cookie = tree_ctrl.GetFirstChild(root_item)
            count = 0
            while child.IsOk() and count < 5:
                child_text = tree_ctrl.GetItemText(child)
                print(f"   Child {count+1}: '{child_text}'")
                child, cookie = tree_ctrl.GetNextChild(root_item, cookie)
                count += 1
        
        # 4. Verify results
        print(f"\n--- Test Results ---")
        
        # Check that overview content appears after project name in markdown
        lines = content.split('\n')
        if len(lines) >= 3 and lines[0] == "# Amazing Library" and overview_text in lines[2]:
            print("✅ PASS: Overview content appears after project name")
        else:
            print("❌ FAIL: Overview content not in correct position")
            if len(lines) >= 3:
                print(f"   Expected: '# Amazing Library' -> '{overview_text}'")
                print(f"   Got: '{lines[0]}' -> '{lines[2]}'")
        
        # Check that Overview is not in tree as separate section
        has_overview_section = False
        if root_item.IsOk():
            child, cookie = tree_ctrl.GetFirstChild(root_item)
            while child.IsOk():
                child_text = tree_ctrl.GetItemText(child)
                if "Overview" in child_text:
                    has_overview_section = True
                    break
                child, cookie = tree_ctrl.GetNextChild(root_item, cookie)
        
        if not has_overview_section:
            print("✅ PASS: Overview not shown as separate section in tree")
        else:
            print("❌ FAIL: Overview still appears as separate section in tree")
        
        # Check that root content is stored correctly
        if editor.template_root.content == overview_text:
            print("✅ PASS: Overview content correctly stored in root section")
        else:
            print(f"❌ FAIL: Overview content storage issue")
            print(f"   Expected: '{overview_text}'")
            print(f"   Got: '{editor.template_root.content}'")
        
        print(f"\nOverview testing completed!")
        
        # Close the app after a short delay
        wx.CallLater(3000, self.frame.Close)

if __name__ == "__main__":
    app = OverviewTestApp()
    app.MainLoop() 