#!/usr/bin/env python3
"""
Setup script for README Editor.
"""

import os
from pathlib import Path
from setuptools import setup, find_packages

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')


# Read requirements
def read_requirements(filename):
    """Read requirements from file."""

    requirements_file = this_directory / filename
    if requirements_file.exists():
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = []
            for line in f:
                line = line.strip()
                # Skip empty lines, comments, and -r references
                if line and not line.startswith('#') and not line.startswith('-r'):
                    requirements.append(line)
            return requirements
    return []


# Read version from the package __init__.py in src layout
def get_version():
    """Extract version from src/readme_editor/__init__.py."""
    version_file = this_directory / "src" / "readme_editor" / "__init__.py"
    if version_file.exists():
        import re
        content = version_file.read_text(encoding='utf-8')
        version_match = re.search(r"__version__\s*=\s*['\"]([^'\"]*)['\"]", content)
        if version_match:
            return version_match.group(1)
    return "1.0.0"

setup(
    name="readme-editor",
    version=get_version(),
    author="README Editor Team",
    author_email="info@example.com",
    description="A desktop GUI to edit and generate high-quality project README files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/readme-editor",
    project_urls={
        "Bug Reports": "https://github.com/example/readme-editor/issues",
        "Source": "https://github.com/example/readme-editor",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=[],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Environment :: X11 Applications :: GTK",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    keywords="readme editor markdown gui wxpython",
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "gui": ["wxpython>=4.2.0"],
    },
    entry_points={
        "console_scripts": [
            # Optional console launcher that starts the GUI
            "readme-editor=readme_editor.__main__:main",
        ],
        "gui_scripts": [
            # Native GUI entry point (on Windows it hides the console)
            "readme-editor-gui=readme_editor.__main__:main",
        ],
    },
    zip_safe=False,
    platforms=["any"],
    license="MIT",
) 