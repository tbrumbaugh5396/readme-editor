#!/usr/bin/env python3
"""
Final test to verify window title updates work correctly with tab switching
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class FinalTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Test the complete workflow
        wx.CallAfter(self.test_complete_workflow)
        
        return True
    
    def test_complete_workflow(self):
        """Test the complete workflow of title updates"""
        print("Testing complete title update workflow...")
        
        # 1. Start in general editor
        print(f"\n1. Initial state (General Editor):")
        self.frame.notebook.SetSelection(0)
        initial_title = self.frame.GetTitle()
        print(f"   Title: '{initial_title}'")
        
        # 2. Switch to structured editor
        print(f"\n2. Switching to Structured Editor:")
        self.frame.notebook.SetSelection(1)
        structured_title = self.frame.GetTitle()
        print(f"   Title: '{structured_title}'")
        
        # 3. Set a project name
        print(f"\n3. Setting project name to 'My Amazing App':")
        self.frame.structured_editor.project_name_ctrl.SetValue("My Amazing App")
        # Trigger the event
        event = wx.CommandEvent(wx.EVT_TEXT.typeId)
        event.SetEventObject(self.frame.structured_editor.project_name_ctrl)
        self.frame.structured_editor.on_project_name_changed(event)
        project_title = self.frame.GetTitle()
        print(f"   Title: '{project_title}'")
        
        # 4. Switch back to general editor
        print(f"\n4. Switching back to General Editor:")
        self.frame.notebook.SetSelection(0)
        general_title = self.frame.GetTitle()
        print(f"   Title: '{general_title}'")
        
        # 5. Switch back to structured editor (should show project name again)
        print(f"\n5. Switching back to Structured Editor:")
        self.frame.notebook.SetSelection(1)
        final_title = self.frame.GetTitle()
        print(f"   Title: '{final_title}'")
        
        # Verify results
        print(f"\n--- Test Results ---")
        
        # Check that project name appears in structured mode
        if "My Amazing App" in project_title:
            print("✅ PASS: Project name appears in title when set")
        else:
            print("❌ FAIL: Project name doesn't appear in title when set")
        
        # Check that general editor doesn't show project name
        if "My Amazing App" not in general_title:
            print("✅ PASS: General editor doesn't show project name")
        else:
            print("❌ FAIL: General editor shows project name (should not)")
        
        # Check that structured editor shows project name again after switching back
        if "My Amazing App" in final_title:
            print("✅ PASS: Project name persists when returning to structured editor")
        else:
            print("❌ FAIL: Project name lost when returning to structured editor")
        
        print(f"\nTesting completed!")
        
        # Close the app after a short delay
        wx.CallLater(2000, self.frame.Close)

if __name__ == "__main__":
    app = FinalTestApp()
    app.MainLoop() 