"""Edit tool."""

from pathlib import Path
from typing import Any


async def execute_edit(arguments: dict[str, Any]) -> str:
    """Edit a file by exact string replacement."""
    path = arguments.get("path")
    old_text = arguments.get("oldText")
    new_text = arguments.get("newText")

    if not isinstance(path, str) or not path.strip():
        return "Error: 'path' must be a non-empty string."
    if not isinstance(old_text, str):
        return "Error: 'oldText' must be a string."
    if not isinstance(new_text, str):
        return "Error: 'newText' must be a string."
    if old_text == "":
        return "Error: 'oldText' cannot be empty."

    try:
        file_path = Path(path)
        content = file_path.read_text()
        if old_text not in content:
            return "Error: 'oldText' not found in file."
        updated = content.replace(old_text, new_text, 1)
        file_path.write_text(updated)
        return f"Edited {path}."
    except Exception as exc:
        return f"Error editing file: {exc}"


EDIT_TOOL: dict[str, Any] = {
    "name": "edit",
    "description": "Edit a file by replacing exact text.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the file to edit."},
            "oldText": {
                "type": "string",
                "description": "Exact text to find in the file.",
            },
            "newText": {"type": "string", "description": "Replacement text."},
        },
        "required": ["path", "oldText", "newText"],
    },
    "execute": execute_edit,
}
