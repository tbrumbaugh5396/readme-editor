"""
Structured README Template
Defines the hierarchical structure for the project README template
"""

import wx
from typing import Dict, List, Optional


class ReadmeSection:
    """Represents a section in the README structure"""

    def __init__(self,
                 name: str,
                 content: str = "",
                 optional: bool = False,
                 level: int = 1):
        self.name = name
        self.content = content
        self.optional = optional
        self.level = level
        self.enabled = True  # Track if section is enabled/disabled
        self.children: List['ReadmeSection'] = []
        self.parent: Optional['ReadmeSection'] = None

    def add_child(self, child: 'ReadmeSection'):
        """Add a child section"""
        child.parent = self
        child.level = self.level + 1
        self.children.append(child)
        return child

    def get_full_path(self) -> str:
        """Get the full path of this section"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name

    def get_markdown_header(self) -> str:
        """Get the markdown header for this section with anchor"""
        header = "#" * self.level + " " + self.name
        # Add HTML anchor for navigation
        anchor_id = self.get_anchor_id()
        return f'<a name="{anchor_id}"></a>\n{header}'

    def get_anchor_id(self) -> str:
        """Get the anchor ID for linking (GitHub-style)"""
        # Convert to lowercase, replace spaces and special chars with hyphens
        anchor = self.name.lower()
        anchor = anchor.replace(' ', '-')
        anchor = ''.join(c if c.isalnum() or c == '-' else '' for c in anchor)
        anchor = anchor.strip('-')
        return anchor

    def to_markdown(self, include_disabled: bool = False) -> str:
        """Convert this section and its children to markdown"""
        # Skip disabled sections unless explicitly requested
        if not self.enabled and not include_disabled:
            return ""

        result = []

        # Add header
        if self.level > 0:
            result.append(self.get_markdown_header())
            result.append("")

            # Add return link to table of contents (except for TOC itself and root level)
            if self.level > 1 and self.name != "Table of contents":
                result.append("[← Table of Contents](#table-of-contents)")
                result.append("")

        # Add content
        if self.content.strip():
            result.append(self.content.strip())
            result.append("")

        # Add children (only enabled ones unless include_disabled is True)
        for child in self.children:
            if child.enabled or include_disabled:
                child_md = child.to_markdown(include_disabled)
                if child_md.strip():
                    result.append(child_md)

        return "\n".join(result)

    def collect_all_headers(
            self,
            headers_list: List['ReadmeSection'] = None
    ) -> List['ReadmeSection']:
        """Collect all headers from this section and its children"""
        if headers_list is None:
            headers_list = []

        # Add this section if it has a header (level > 0) and is enabled
        if self.level > 0 and self.enabled:
            headers_list.append(self)

        # Add children recursively
        for child in self.children:
            if child.enabled:
                child.collect_all_headers(headers_list)

        return headers_list

    def generate_table_of_contents(self) -> str:
        """Generate a table of contents with links to all headers"""
        headers = self.collect_all_headers()

        if not headers:
            return "No sections available."

        toc_lines = []
        for header in headers:
            # Skip the project name (level 1) and table of contents itself
            if header.level <= 1 or header.name == "Table of contents":
                continue

            # Create indentation based on level (start from level 2 as base)
            indent = "  " * (header.level - 2)
            anchor = header.get_anchor_id()
            toc_line = f"{indent}- [{header.name}](#{anchor})"
            toc_lines.append(toc_line)

        return "\n".join(
            toc_lines
        ) if toc_lines else "No sections to display in table of contents."


def create_readme_template() -> ReadmeSection:
    """Create the complete structured README template"""

    # Root section
    root = ReadmeSection("Project", level=0)

    # Project Name
    project_name = root.add_child(ReadmeSection("Project Name"))

    # Overview
    overview = root.add_child(ReadmeSection("Overview"))
    overview.add_child(ReadmeSection("Audience", optional=True))

    # Philosophy of Development
    philosophy = overview.add_child(
        ReadmeSection("Philosophy of Development", optional=True))
    philosophy.add_child(ReadmeSection("Readability", optional=True))
    philosophy.add_child(ReadmeSection("Types", optional=True))
    philosophy.add_child(ReadmeSection("Automation", optional=True))
    philosophy.add_child(ReadmeSection("Testing", optional=True))
    philosophy.add_child(ReadmeSection("Coding Standards", optional=True))
    philosophy.add_child(ReadmeSection("Code Artifacts", optional=True))
    philosophy.add_child(
        ReadmeSection("Distribution and Packaging", optional=True))

    # Documentation Overview
    doc_overview = overview.add_child(
        ReadmeSection("Documentation Overview", optional=True))
    doc_overview.add_child(
        ReadmeSection("Documentation Principle", optional=True))
    doc_overview.add_child(ReadmeSection("Documentation should include"))

    # Table of contents
    toc_section = root.add_child(ReadmeSection("Table of contents"))

    # Run Software
    run_software = root.add_child(ReadmeSection("Run Software"))

    # Run Software as a User
    run_user = run_software.add_child(ReadmeSection("Run Software as a User"))

    # Install and Run Locally on Computer
    install_local = run_user.add_child(
        ReadmeSection("Install and Run Locally on Computer"))

    # Get executables
    get_exec = install_local.add_child(ReadmeSection("Get executables"))
    get_exec.add_child(ReadmeSection("For MacOS"))
    get_exec.add_child(ReadmeSection("For Windows OS"))
    get_exec.add_child(ReadmeSection("For Linux OS"))

    # For Docker
    docker_section = get_exec.add_child(ReadmeSection("For Docker"))
    docker_section.add_child(ReadmeSection("Install Docker"))
    docker_section.add_child(ReadmeSection("Setup Docker Environment"))

    # Run executables
    install_local.add_child(ReadmeSection("Run executables"))

    # Run in Web Browser
    run_user.add_child(ReadmeSection("Run in Web Browser"))

    # Run as Developer
    run_dev = run_software.add_child(ReadmeSection("Run as Developer"))
    run_dev.add_child(ReadmeSection("Get Software using Pypi"))
    run_dev.add_child(ReadmeSection("Get Software using Git"))
    run_dev.add_child(ReadmeSection("Get Software using Zip"))
    run_dev.add_child(ReadmeSection("Install prequisites"))

    # Project Architecture
    architecture = root.add_child(ReadmeSection("Project Architecture"))
    architecture.add_child(ReadmeSection("Project Structure"))
    architecture.add_child(ReadmeSection("Dependency"))

    # Usage
    usage = root.add_child(ReadmeSection("Usage"))

    # Running the Project Structure
    running_structure = usage.add_child(
        ReadmeSection("Running the Project Structure"))
    running_structure.add_child(ReadmeSection("Run Database"))
    running_structure.add_child(
        ReadmeSection("Run API and Documentation Server"))
    running_structure.add_child(ReadmeSection("Run Frontend"))
    running_structure.add_child(ReadmeSection("Run Backend"))
    running_structure.add_child(ReadmeSection("Run Main"))

    # API Reference
    usage.add_child(ReadmeSection("API Reference", optional=True))

    # Example Code
    example_code = root.add_child(ReadmeSection("Example Code"))
    example_code.add_child(ReadmeSection("Database"))
    example_code.add_child(ReadmeSection("API"))
    example_code.add_child(ReadmeSection("Backend"))
    example_code.add_child(ReadmeSection("Frontend"))
    example_code.add_child(ReadmeSection("Main"))

    # Developer Guide
    dev_guide = root.add_child(ReadmeSection("Developer Guide"))
    dev_guide.add_child(ReadmeSection("Install Developer Tools"))
    dev_guide.add_child(ReadmeSection("Run Tests"))
    dev_guide.add_child(ReadmeSection("UI/UX Styleguide"))

    # References
    references = root.add_child(ReadmeSection("References"))

    # Appendix
    appendix = references.add_child(ReadmeSection("Appendix"))

    # Python section
    python_section = appendix.add_child(ReadmeSection("Python"))
    python_section.add_child(ReadmeSection("Install Python"))

    # Node section
    node_section = appendix.add_child(ReadmeSection("Node"))
    node_section.add_child(ReadmeSection("Install Node"))

    # Docker section
    docker_appendix = appendix.add_child(ReadmeSection("Docker"))
    docker_appendix.add_child(ReadmeSection("Install Docker"))

    # TypeScript section
    ts_section = appendix.add_child(ReadmeSection("Typescript"))
    ts_section.add_child(ReadmeSection("Install Typescript"))

    # Electron section
    electron_section = appendix.add_child(ReadmeSection("Electron"))
    electron_section.add_child(ReadmeSection("Install Electron"))

    # SQL section
    sql_section = appendix.add_child(ReadmeSection("SQL"))
    sql_section.add_child(ReadmeSection("Install SQL"))

    # Git section
    git_section = appendix.add_child(ReadmeSection("Git"))
    git_section.add_child(ReadmeSection("Install Git"))

    # IconUtil section
    iconutil_section = appendix.add_child(ReadmeSection("IconUtil"))
    iconutil_section.add_child(ReadmeSection("Install IconUtil"))

    # Install Javascript Packages
    js_packages = appendix.add_child(
        ReadmeSection("Install Javascript Packages"))
    js_packages.add_child(ReadmeSection("Install Typescript"))
    js_packages.add_child(ReadmeSection("Install Electron"))

    # Install Python Packages
    py_packages = appendix.add_child(ReadmeSection("Install Python Packages"))
    py_packages.add_child(ReadmeSection("Install Pyinstaller"))
    py_packages.add_child(ReadmeSection("Install Pipenv"))

    # Install Testing Tools
    references.add_child(ReadmeSection("Install Testing Tools"))

    # Extending the Code
    extending = references.add_child(ReadmeSection("Extending the Code"))
    extending.add_child(ReadmeSection("Extending Streamlit Component"))
    extending.add_child(ReadmeSection("Extending Electron Application"))
    extending.add_child(ReadmeSection("Extending a Desktop Application"))
    extending.add_child(ReadmeSection("Creating a Python Package"))
    extending.add_child(ReadmeSection("Autogenerating Documentation"))
    extending.add_child(ReadmeSection("Screenshots", optional=True))

    # Glossary
    glossary = references.add_child(ReadmeSection("Glossary"))
    glossary.add_child(ReadmeSection("Technology Stack"))

    # Installation
    installation = root.add_child(ReadmeSection("Installation"))

    # Source Code Installation
    source_install = installation.add_child(
        ReadmeSection("Source Code Installation"))
    source_install.add_child(ReadmeSection("Clone the Repository"))
    source_install.add_child(ReadmeSection("Virtual Environment"))
    source_install.add_child(ReadmeSection("Install Dependencies"))

    # Python Package Installation
    package_install = installation.add_child(
        ReadmeSection("Python Package Installation"))
    package_install.add_child(ReadmeSection("Install from Pypi.org"))

    # Project Structure (under Installation)
    installation.add_child(ReadmeSection("Project Structure"))

    # Software Dependencies
    dependencies = installation.add_child(
        ReadmeSection("Software Dependencies"))

    # Python Libraries
    py_libs = dependencies.add_child(ReadmeSection("Python Libraries"))
    py_libs.add_child(ReadmeSection("Python Standard Libraries"))
    py_libs.add_child(ReadmeSection("Additional Python Libraries Used"))

    # Improvement Plan
    improvement = root.add_child(ReadmeSection("Improvement Plan"))
    improvement.add_child(ReadmeSection("Todo List"))
    improvement.add_child(ReadmeSection("Roadmap"))

    # Final sections
    root.add_child(ReadmeSection("Contributing"))
    root.add_child(ReadmeSection("License"))
    root.add_child(ReadmeSection("Acknowledgements"))

    return root


def populate_tree_ctrl(
        tree_ctrl: wx.TreeCtrl,
        root_section: ReadmeSection) -> Dict[wx.TreeItemId, ReadmeSection]:
    """Populate a tree control with the README structure"""
    tree_ctrl.DeleteAllItems()

    # Mapping from tree item to section
    item_to_section = {}

    def add_section_to_tree(
            section: ReadmeSection,
            parent_item: Optional[wx.TreeItemId] = None) -> wx.TreeItemId:
        # Create display name with enabled/disabled status
        display_name = section.name
        if section.optional:
            display_name += " (Optional)"
        if not section.enabled:
            display_name += " [DISABLED]"

        # Add to tree
        if parent_item is None:
            item = tree_ctrl.AddRoot(display_name)
        else:
            item = tree_ctrl.AppendItem(parent_item, display_name)

        # Visual styling for disabled items
        if not section.enabled:
            tree_ctrl.SetItemTextColour(item, wx.Colour(
                128, 128, 128))  # Gray out disabled items

        # Store mapping
        item_to_section[item] = section

        # Add children
        for child in section.children:
            add_section_to_tree(child, item)

        return item

    # Add the root section's children as top-level items (H1 sections)
    if root_section.children:
        # Create a hidden root item
        hidden_root = tree_ctrl.AddRoot("")

        # Add each child as a direct child of the hidden root
        for child in root_section.children:
            add_section_to_tree(child, hidden_root)

        # Expand all and hide the root to show H1 sections as top level
        tree_ctrl.ExpandAll()
        tree_ctrl.SetWindowStyleFlag(tree_ctrl.GetWindowStyleFlag()
                                     | wx.TR_HIDE_ROOT)

    return item_to_section
