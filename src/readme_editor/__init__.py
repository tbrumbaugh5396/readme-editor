"""
readme_editor package

Public API:
    from readme_editor import MainFrame, ReadmeEditorApp

We use lazy attribute loading to avoid circular imports when running
"python -m readme_editor" which initializes the package before __main__.
"""

from typing import Any

__all__ = [
    "ReadmeEditorApp",
    "MainFrame",
    "GeneralEditor",
    "StructuredEditor",
    "__version__",
]

# Semantic version for setup.py to read
__version__ = "1.0.0"


def __getattr__(name: str) -> Any:
    """Lazily import heavy GUI symbols to prevent circular import issues."""
    if name in {"ReadmeEditorApp", "MainFrame", "GeneralEditor", "StructuredEditor"}:
        from .readme_editor import (
            ReadmeEditorApp,
            MainFrame,
            GeneralEditor,
            StructuredEditor,
        )
        return {
            "ReadmeEditorApp": ReadmeEditorApp,
            "MainFrame": MainFrame,
            "GeneralEditor": GeneralEditor,
            "StructuredEditor": StructuredEditor,
        }[name]
    raise AttributeError(f"module 'readme_editor' has no attribute {name!r}")

