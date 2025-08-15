"""
Compatibility shim for legacy imports of `structured_template` at project root.

Re-exports from the package module `readme_editor.structured_template`.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from readme_editor.structured_template import (  # type: ignore
    ReadmeSection,
    create_readme_template,
    populate_tree_ctrl,
)

__all__ = [
    "ReadmeSection",
    "create_readme_template",
    "populate_tree_ctrl",
]


