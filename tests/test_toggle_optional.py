#!/usr/bin/env python3
"""
Test script to verify that the toggle optional button works correctly
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class ToggleOptionalTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test toggle optional functionality
        wx.CallAfter(self.test_toggle_optional)
        
        return True
    
    def test_toggle_optional(self):
        """Test that toggle optional button works correctly"""
        print("Testing toggle optional functionality...")
        
        editor = self.frame.structured_editor
        
        # 1. Check initial state
        print(f"\n1. Checking initial state:")
        initial_optional_enabled = self.count_optional_enabled(editor.template_root)
        initial_optional_total = self.count_optional_total(editor.template_root)
        initial_required_enabled = self.count_required_enabled(editor.template_root)
        
        print(f"   Optional sections enabled: {initial_optional_enabled}/{initial_optional_total}")
        print(f"   Required sections enabled: {initial_required_enabled}")
        
        # 2. Check button exists
        print(f"\n2. Checking button:")
        has_button = hasattr(editor, 'toggle_optional_btn')
        if has_button:
            button_text = editor.toggle_optional_btn.GetLabel()
            print(f"   ✅ Button found: '{button_text}'")
        else:
            print(f"   ❌ Button not found")
            return
        
        # 3. First toggle - should disable all optional (since initially enabled)
        print(f"\n3. First toggle (disable all optional):")
        self.trigger_toggle_button(editor)
        
        after_first_optional = self.count_optional_enabled(editor.template_root)
        after_first_required = self.count_required_enabled(editor.template_root)
        
        print(f"   Optional sections enabled: {after_first_optional}/{initial_optional_total}")
        print(f"   Required sections enabled: {after_first_required}")
        
        # 4. Second toggle - should enable all optional (since all disabled)
        print(f"\n4. Second toggle (enable all optional):")
        self.trigger_toggle_button(editor)
        
        after_second_optional = self.count_optional_enabled(editor.template_root)
        after_second_required = self.count_required_enabled(editor.template_root)
        
        print(f"   Optional sections enabled: {after_second_optional}/{initial_optional_total}")
        print(f"   Required sections enabled: {after_second_required}")
        
        # 5. Test partial state - disable some optional manually, then toggle
        print(f"\n5. Testing partial state toggle:")
        # Manually disable half the optional sections
        self.disable_some_optional(editor.template_root, 0.5)
        partial_optional = self.count_optional_enabled(editor.template_root)
        
        print(f"   Optional sections after partial disable: {partial_optional}/{initial_optional_total}")
        
        # Now toggle - should disable all remaining optional
        self.trigger_toggle_button(editor)
        after_partial_toggle = self.count_optional_enabled(editor.template_root)
        
        print(f"   Optional sections after toggle: {after_partial_toggle}/{initial_optional_total}")
        
        # 6. Verify results
        print(f"\n--- Test Results ---")
        
        # Check first toggle disabled all optional
        if after_first_optional == 0:
            print("✅ PASS: First toggle disabled all optional sections")
        else:
            print(f"❌ FAIL: First toggle left {after_first_optional} optional sections enabled")
        
        # Check second toggle enabled all optional
        if after_second_optional == initial_optional_total:
            print("✅ PASS: Second toggle enabled all optional sections")
        else:
            print(f"❌ FAIL: Second toggle enabled {after_second_optional}/{initial_optional_total} optional sections")
        
        # Check required sections unchanged
        if (after_first_required == initial_required_enabled and 
            after_second_required == initial_required_enabled):
            print("✅ PASS: Required sections unchanged throughout")
        else:
            print("❌ FAIL: Required sections were affected")
        
        # Check partial state toggle works
        if after_partial_toggle == 0:
            print("✅ PASS: Partial state toggle correctly disabled all optional")
        else:
            print(f"❌ FAIL: Partial state toggle left {after_partial_toggle} optional sections enabled")
        
        print(f"\nToggle optional testing completed!")
        
        # Close after a delay
        wx.CallLater(3000, self.frame.Close)
    
    def trigger_toggle_button(self, editor):
        """Trigger the toggle optional button"""
        event = wx.CommandEvent(wx.EVT_BUTTON.typeId)
        event.SetEventObject(editor.toggle_optional_btn)
        editor.on_toggle_optional_sections(event)
    
    def count_optional_enabled(self, section):
        """Count enabled optional sections"""
        count = 0
        if section.optional and section.enabled:
            count += 1
        for child in section.children:
            count += self.count_optional_enabled(child)
        return count
    
    def count_optional_total(self, section):
        """Count total optional sections"""
        count = 0
        if section.optional:
            count += 1
        for child in section.children:
            count += self.count_optional_total(child)
        return count
    
    def count_required_enabled(self, section):
        """Count enabled required (non-optional) sections"""
        count = 0
        if not section.optional and section.enabled:
            count += 1
        for child in section.children:
            count += self.count_required_enabled(child)
        return count
    
    def disable_some_optional(self, section, ratio):
        """Disable a ratio of optional sections (for testing partial state)"""
        import random
        
        def disable_optional_recursive(sec, r):
            if sec.optional and random.random() < r:
                sec.enabled = False
            for child in sec.children:
                disable_optional_recursive(child, r)
        
        disable_optional_recursive(section, ratio)

if __name__ == "__main__":
    app = ToggleOptionalTestApp()
    app.MainLoop() 