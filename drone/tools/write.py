"""Write tool."""

from pathlib import Path
from typing import Any


async def execute_write(arguments: dict[str, Any]) -> str:
    """Write full content to a file."""
    path = arguments.get("path")
    content = arguments.get("content")

    if not isinstance(path, str) or not path.strip():
        return "Error: 'path' must be a non-empty string."
    if not isinstance(content, str):
        return "Error: 'content' must be a string."

    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Wrote {len(content)} bytes to {path}."
    except Exception as exc:
        return f"Error writing file: {exc}"


WRITE_TOOL: dict[str, Any] = {
    "name": "write",
    "description": (
        "Write content to a file. Creates the file if needed and overwrites existing content."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the file to write."},
            "content": {"type": "string", "description": "Content to write."},
        },
        "required": ["path", "content"],
    },
    "execute": execute_write,
}
