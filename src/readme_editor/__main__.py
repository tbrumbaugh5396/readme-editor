"""
Package entry point for README Editor.

Run with: python -m readme_editor
"""

try:
    # When executed as package: python -m readme_editor
    from readme_editor import ReadmeEditorApp  # type: ignore
except Exception:
    # Fallback if relative import fails
    from readme_editor.readme_editor import ReadmeEditorApp  # type: ignore


def main() -> None:
    app = ReadmeEditorApp()
    app.MainLoop()


if __name__ == "__main__":
    main()


