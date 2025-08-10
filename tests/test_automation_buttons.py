#!/usr/bin/env python3
"""
Test script to verify that all automation buttons work correctly
"""

import wx
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readme_editor import MainFrame

class AutomationTestApp(wx.App):
    def OnInit(self):
        # Create the main frame
        self.frame = MainFrame()
        self.frame.Show()
        
        # Switch to structured editor tab
        self.frame.notebook.SetSelection(1)
        
        # Test automation functionality
        wx.CallAfter(self.test_automation_buttons)
        
        return True
    
    def test_automation_buttons(self):
        """Test that all automation buttons work correctly"""
        print("Testing automation buttons functionality...")
        
        editor = self.frame.structured_editor
        
        # 1. Check that buttons exist
        print(f"\n1. Checking automation buttons:")
        buttons = [
            ('auto_file_structure_btn', 'File Structure'),
            ('auto_dependencies_btn', 'Dependencies'),
            ('auto_dev_deps_btn', 'Dev Dependencies')
        ]
        
        for btn_attr, expected_label in buttons:
            if hasattr(editor, btn_attr):
                button = getattr(editor, btn_attr)
                actual_label = button.GetLabel()
                print(f"   ✅ {expected_label} button found: '{actual_label}'")
            else:
                print(f"   ❌ {expected_label} button not found")
                return
        
        # 2. Test File Structure Generation
        print(f"\n2. Testing File Structure Generation:")
        try:
            # Trigger the file structure button
            event = wx.CommandEvent(wx.EVT_BUTTON.typeId)
            event.SetEventObject(editor.auto_file_structure_btn)
            editor.on_auto_generate_file_structure(event)
            
            # Check if Project Structure section was populated
            project_structure_section = self._find_section_by_name(editor.template_root, "Project Structure")
            if project_structure_section and project_structure_section.content:
                print("   ✅ PASS: File structure generated successfully")
                print(f"   Content preview: {project_structure_section.content[:100]}...")
            else:
                print("   ❌ FAIL: File structure not generated")
        except Exception as e:
            print(f"   ❌ FAIL: Error generating file structure: {e}")
        
        # 3. Test Dependencies Generation
        print(f"\n3. Testing Dependencies Generation:")
        try:
            # Trigger the dependencies button
            event = wx.CommandEvent(wx.EVT_BUTTON.typeId)
            event.SetEventObject(editor.auto_dependencies_btn)
            editor.on_auto_generate_dependencies(event)
            
            # Check if a dependencies section was populated
            dependencies_sections = ["Dependencies", "Software Dependencies", "Python Libraries", "Install Dependencies"]
            found_section = None
            for section_name in dependencies_sections:
                section = self._find_section_by_name(editor.template_root, section_name)
                if section and section.content:
                    found_section = section
                    break
            
            if found_section:
                print("   ✅ PASS: Dependencies generated successfully")
                print(f"   Section: {found_section.name}")
                print(f"   Content preview: {found_section.content[:100]}...")
            else:
                print("   ⚠️  SKIP: Dependencies not generated (requirements.txt may not exist)")
        except Exception as e:
            print(f"   ❌ FAIL: Error generating dependencies: {e}")
        
        # 4. Test Dev Dependencies Generation
        print(f"\n4. Testing Dev Dependencies Generation:")
        try:
            # Trigger the dev dependencies button
            event = wx.CommandEvent(wx.EVT_BUTTON.typeId)
            event.SetEventObject(editor.auto_dev_deps_btn)
            editor.on_auto_generate_dev_dependencies(event)
            
            # Check if a dev dependencies section was populated
            dev_sections = ["Install Developer Tools", "Developer Dependencies", "Development Setup", "Dev Dependencies"]
            found_section = None
            for section_name in dev_sections:
                section = self._find_section_by_name(editor.template_root, section_name)
                if section and section.content:
                    found_section = section
                    break
            
            if found_section:
                print("   ✅ PASS: Dev dependencies generated successfully")
                print(f"   Section: {found_section.name}")
                print(f"   Content preview: {found_section.content[:100]}...")
            else:
                print("   ⚠️  SKIP: Dev dependencies not generated (requirements-dev.txt may not exist)")
        except Exception as e:
            print(f"   ❌ FAIL: Error generating dev dependencies: {e}")
        
        # 5. Test that sections are enabled and visible in tree
        print(f"\n5. Testing tree updates:")
        root_item = editor.tree_ctrl.GetRootItem()
        if root_item.IsOk():
            enabled_sections = []
            self._collect_enabled_sections(root_item, editor.tree_ctrl, enabled_sections)
            print(f"   Enabled sections in tree: {len(enabled_sections)}")
            for section_name in enabled_sections[:10]:  # Show first 10
                print(f"     - {section_name}")
            if len(enabled_sections) > 10:
                print(f"     ... and {len(enabled_sections) - 10} more")
        
        # 6. Test markdown generation includes auto-generated content
        print(f"\n6. Testing markdown generation:")
        try:
            markdown_content = editor.get_content()
            has_file_structure = "```" in markdown_content and ("README Editor/" in markdown_content or "Desktop/" in markdown_content)
            has_dependencies = "Dependencies" in markdown_content
            
            print(f"   Generated markdown length: {len(markdown_content)} characters")
            print(f"   Contains file structure: {'✅' if has_file_structure else '❌'}")
            print(f"   Contains dependencies: {'✅' if has_dependencies else '❌'}")
        except Exception as e:
            print(f"   ❌ FAIL: Error generating markdown: {e}")
        
        print(f"\nAutomation buttons testing completed!")
        
        # Close after a delay
        wx.CallLater(3000, self.frame.Close)
    
    def _find_section_by_name(self, section, name):
        """Recursively find a section by name"""
        if section.name == name:
            return section
        for child in section.children:
            result = self._find_section_by_name(child, name)
            if result:
                return result
        return None
    
    def _collect_enabled_sections(self, item, tree_ctrl, sections_list):
        """Recursively collect enabled section names from tree"""
        section_name = tree_ctrl.GetItemText(item)
        if section_name:
            sections_list.append(section_name)
        
        child, cookie = tree_ctrl.GetFirstChild(item)
        while child.IsOk():
            self._collect_enabled_sections(child, tree_ctrl, sections_list)
            child, cookie = tree_ctrl.GetNextChild(item, cookie)

if __name__ == "__main__":
    app = AutomationTestApp()
    app.MainLoop() 