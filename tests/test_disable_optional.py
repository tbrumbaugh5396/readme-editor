#!/usr/bin/env python3
"""
Test script to verify that the disable all optional button works correctly
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class DisableOptionalTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test disable optional functionality
        wx.CallAfter(self.test_disable_optional)
        
        return True
    
    def test_disable_optional(self):
        """Test that disable all optional button works correctly"""
        print("Testing disable all optional functionality...")
        
        editor = self.frame.structured_editor
        
        # 1. Check initial state - count optional sections
        print(f"\n1. Checking initial state:")
        initial_optional_enabled, initial_optional_total = self.count_optional_sections(editor.template_root)
        initial_required_enabled, initial_required_total = self.count_required_sections(editor.template_root)
        
        print(f"   Optional sections enabled: {initial_optional_enabled}/{initial_optional_total}")
        print(f"   Required sections enabled: {initial_required_enabled}/{initial_required_total}")
        
        # 2. Check that button exists
        print(f"\n2. Checking button exists:")
        has_button = hasattr(editor, 'disable_optional_btn')
        if has_button:
            button_text = editor.disable_optional_btn.GetLabel()
            print(f"   ✅ Button found: '{button_text}'")
        else:
            print(f"   ❌ Button not found")
            return
        
        # 3. Test disable optional functionality
        print(f"\n3. Testing disable optional functionality:")
        
        # Trigger the disable optional button
        event = wx.CommandEvent(wx.EVT_BUTTON.typeId)
        event.SetEventObject(editor.disable_optional_btn)
        editor.on_disable_optional_sections(event)
        
        # Check state after disabling optional
        after_optional_enabled, after_optional_total = self.count_optional_sections(editor.template_root)
        after_required_enabled, after_required_total = self.count_required_sections(editor.template_root)
        
        print(f"   Optional sections enabled after: {after_optional_enabled}/{after_optional_total}")
        print(f"   Required sections enabled after: {after_required_enabled}/{after_required_total}")
        
        # 4. Verify tree display
        print(f"\n4. Checking tree display:")
        disabled_count, total_count = self.count_disabled_in_tree(editor.tree_ctrl)
        print(f"   Tree items showing [DISABLED]: {disabled_count}/{total_count}")
        
        # 5. Generate markdown and check
        print(f"\n5. Testing markdown generation:")
        content = editor.get_content()
        section_count = content.count('\n# ') + content.count('\n## ')
        print(f"   Generated sections in markdown: {section_count}")
        
        # 6. Verify results
        print(f"\n--- Test Results ---")
        
        # Check that all optional sections are disabled
        if after_optional_enabled == 0:
            print("✅ PASS: All optional sections disabled")
        else:
            print(f"❌ FAIL: {after_optional_enabled} optional sections still enabled")
        
        # Check that required sections are still enabled
        if after_required_enabled == initial_required_enabled:
            print("✅ PASS: Required sections remain enabled")
        else:
            print(f"❌ FAIL: Required sections changed from {initial_required_enabled} to {after_required_enabled}")
        
        # Check that tree shows disabled items
        if disabled_count > 0:
            print("✅ PASS: Tree shows disabled sections")
        else:
            print("❌ FAIL: Tree not showing disabled sections")
        
        print(f"\nDisable optional testing completed!")
        
        # Close after a delay
        wx.CallLater(3000, self.frame.Close)
    
    def count_optional_sections(self, section):
        """Count enabled and total optional sections"""
        enabled = 0
        total = 0
        
        if section.optional:
            total += 1
            if section.enabled:
                enabled += 1
        
        for child in section.children:
            child_enabled, child_total = self.count_optional_sections(child)
            enabled += child_enabled
            total += child_total
        
        return enabled, total
    
    def count_required_sections(self, section):
        """Count enabled and total required (non-optional) sections"""
        enabled = 0
        total = 0
        
        if not section.optional:
            total += 1
            if section.enabled:
                enabled += 1
        
        for child in section.children:
            child_enabled, child_total = self.count_required_sections(child)
            enabled += child_enabled
            total += child_total
        
        return enabled, total
    
    def count_disabled_in_tree(self, tree_ctrl):
        """Count items showing [DISABLED] in tree"""
        disabled_count = 0
        total_count = 0
        
        def count_tree_items(item):
            nonlocal disabled_count, total_count
            if not item.IsOk():
                return
            
            total_count += 1
            text = tree_ctrl.GetItemText(item)
            if "[DISABLED]" in text:
                disabled_count += 1
            
            child, cookie = tree_ctrl.GetFirstChild(item)
            while child.IsOk():
                count_tree_items(child)
                child, cookie = tree_ctrl.GetNextChild(item, cookie)
        
        root_item = tree_ctrl.GetRootItem()
        if root_item.IsOk():
            count_tree_items(root_item)
        
        return disabled_count, total_count

if __name__ == "__main__":
    app = DisableOptionalTestApp()
    app.MainLoop() 