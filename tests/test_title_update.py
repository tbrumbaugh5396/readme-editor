#!/usr/bin/env python3
"""
Test script to verify that window title updates with project name changes
"""

import wx
import sys
import os
import time

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame, ReadmeEditorApp

class TestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test title updates
        wx.CallAfter(self.test_title_updates)
        
        return True
    
    def test_title_updates(self):
        """Test that title updates when project name changes"""
        print("Testing window title updates...")
        
        # Get initial title
        initial_title = self.frame.GetTitle()
        print(f"Initial title: '{initial_title}'")
        
        # Change project name
        test_names = ["My Awesome Project", "Super Cool App", ""]
        
        for i, test_name in enumerate(test_names):
            print(f"\nTest {i+1}: Setting project name to '{test_name}'")
            
            # Set the project name
            self.frame.structured_editor.project_name_ctrl.SetValue(test_name)
            
            # Simulate the text change event
            event = wx.CommandEvent(wx.EVT_TEXT.typeId)
            event.SetEventObject(self.frame.structured_editor.project_name_ctrl)
            self.frame.structured_editor.on_project_name_changed(event)
            
            # Get the updated title
            updated_title = self.frame.GetTitle()
            print(f"Updated title: '{updated_title}'")
            
            # Check if title contains the project name (unless empty)
            if test_name.strip():
                if test_name.strip() in updated_title:
                    print("✅ PASS: Project name found in title")
                else:
                    print("❌ FAIL: Project name not found in title")
            else:
                if "README Editor" in updated_title and test_name not in updated_title:
                    print("✅ PASS: Empty project name handled correctly")
                else:
                    print("❌ FAIL: Empty project name not handled correctly")
        
        # Test switching tabs
        print(f"\nTest: Switching to General Editor tab")
        self.frame.notebook.SetSelection(0)
        self.frame.update_title()
        general_title = self.frame.GetTitle()
        print(f"General editor title: '{general_title}'")
        
        print(f"\nTest: Switching back to Structured Editor tab")
        self.frame.notebook.SetSelection(1)
        self.frame.update_title()
        structured_title = self.frame.GetTitle()
        print(f"Structured editor title: '{structured_title}'")
        
        print("\nTitle update testing completed!")
        
        # Close the app after a short delay
        wx.CallLater(2000, self.frame.Close)

if __name__ == "__main__":
    app = TestApp()
    app.MainLoop() 