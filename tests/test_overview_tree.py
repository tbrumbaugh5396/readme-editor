#!/usr/bin/env python3
"""
Test script to verify that Overview appears in tree and can be edited
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class OverviewTreeTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test overview in tree functionality
        wx.CallAfter(self.test_overview_in_tree)
        
        return True
    
    def test_overview_in_tree(self):
        """Test that Overview appears in tree and can be edited"""
        print("Testing Overview in tree functionality...")
        
        # Get the structured editor
        editor = self.frame.structured_editor
        tree_ctrl = editor.tree_ctrl
        
        # 1. Check that Overview appears in tree
        print(f"\n1. Checking tree structure:")
        root_item = tree_ctrl.GetRootItem()
        if root_item.IsOk():
            root_text = tree_ctrl.GetItemText(root_item)
            print(f"   Root: '{root_text}'")
            
            # Find Overview in children
            overview_item = None
            child, cookie = tree_ctrl.GetFirstChild(root_item)
            children = []
            while child.IsOk():
                child_text = tree_ctrl.GetItemText(child)
                children.append(child_text)
                if child_text == "Overview":
                    overview_item = child
                child, cookie = tree_ctrl.GetNextChild(root_item, cookie)
            
            print(f"   Children: {children[:5]}")
            
            if overview_item:
                print("✅ PASS: Overview found in tree")
            else:
                print("❌ FAIL: Overview not found in tree")
                return
        
        # 2. Test selecting Overview in tree
        print(f"\n2. Testing Overview selection:")
        if overview_item:
            # Select the Overview item
            tree_ctrl.SelectItem(overview_item)
            
            # Trigger selection event
            event = wx.TreeEvent(wx.EVT_TREE_SEL_CHANGED.typeId, tree_ctrl.GetId())
            event.SetEventObject(tree_ctrl)
            event.SetItem(overview_item)
            editor.on_tree_selection(event)
            
            # Check current section
            current_section_label = editor.current_section_label.GetLabel()
            print(f"   Current section label: '{current_section_label}'")
            
            # Check if editing root content
            is_editing_root = editor.current_section == editor.template_root
            print(f"   Editing root content: {is_editing_root}")
        
        # 3. Test editing Overview content through section editor
        print(f"\n3. Testing Overview editing through section editor:")
        overview_text = "This is the project overview edited through the section editor."
        editor.section_editor.SetValue(overview_text)
        
        # Trigger text change event
        text_event = wx.CommandEvent(wx.EVT_TEXT.typeId)
        text_event.SetEventObject(editor.section_editor)
        editor.on_section_text_changed(text_event)
        
        # Check synchronization
        overview_ctrl_text = editor.overview_ctrl.GetValue()
        root_content = editor.template_root.content
        
        print(f"   Section editor: '{overview_text}'")
        print(f"   Overview control: '{overview_ctrl_text}'")
        print(f"   Root content: '{root_content}'")
        
        # 4. Test editing through overview control
        print(f"\n4. Testing editing through overview control:")
        overview_text2 = "This is edited through the overview control."
        editor.overview_ctrl.SetValue(overview_text2)
        
        # Trigger overview change event
        overview_event = wx.CommandEvent(wx.EVT_TEXT.typeId)
        overview_event.SetEventObject(editor.overview_ctrl)
        editor.on_overview_changed(overview_event)
        
        # Check synchronization
        section_editor_text = editor.section_editor.GetValue()
        root_content2 = editor.template_root.content
        
        print(f"   Overview control: '{overview_text2}'")
        print(f"   Section editor: '{section_editor_text}'")
        print(f"   Root content: '{root_content2}'")
        
        # 5. Generate markdown and verify
        print(f"\n5. Testing markdown generation:")
        editor.project_name_ctrl.SetValue("Test Project")
        content = editor.get_content()
        lines = content.split('\n')
        
        print(f"   First few lines of markdown:")
        for i, line in enumerate(lines[:5]):
            print(f"     {i+1}: '{line}'")
        
        # 6. Verify results
        print(f"\n--- Test Results ---")
        
        # Check that Overview appears in tree
        has_overview_in_tree = overview_item is not None
        if has_overview_in_tree:
            print("✅ PASS: Overview appears in tree structure")
        else:
            print("❌ FAIL: Overview missing from tree structure")
        
        # Check bidirectional sync
        sync_works = (overview_ctrl_text == overview_text and 
                     section_editor_text == overview_text2 and
                     root_content2 == overview_text2)
        if sync_works:
            print("✅ PASS: Bidirectional synchronization works")
        else:
            print("❌ FAIL: Synchronization issues detected")
        
        # Check markdown generation
        has_correct_markdown = (len(lines) >= 3 and 
                               lines[0] == "# Test Project" and 
                               overview_text2 in lines[2])
        if has_correct_markdown:
            print("✅ PASS: Overview content appears correctly in markdown")
        else:
            print("❌ FAIL: Overview content not in correct markdown position")
        
        print(f"\nOverview tree testing completed!")
        
        # Close the app after a short delay
        wx.CallLater(3000, self.frame.Close)

if __name__ == "__main__":
    app = OverviewTreeTestApp()
    app.MainLoop() 