"""Read tool."""

from pathlib import Path
from typing import Any


async def execute_read(arguments: dict[str, Any]) -> str:
    """Read file contents with optional offset and limit."""
    path = arguments.get("path")
    offset = arguments.get("offset", 1)
    limit = arguments.get("limit", 2000)

    if not isinstance(path, str) or not path.strip():
        return "Error: 'path' must be a non-empty string."
    if not isinstance(offset, int) or offset < 1:
        return "Error: 'offset' must be an integer >= 1."
    if not isinstance(limit, int) or limit < 1:
        return "Error: 'limit' must be an integer >= 1."

    try:
        file_path = Path(path)
        lines = file_path.read_text().splitlines()
        sliced = lines[offset - 1 : offset - 1 + limit]
        if not sliced:
            return ""
        return "\n".join(sliced)
    except Exception as exc:
        return f"Error reading file: {exc}"


READ_TOOL: dict[str, Any] = {
    "name": "read",
    "description": "Read the contents of a file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the file to read."},
            "offset": {
                "type": "integer",
                "description": "Line number to start from (1-indexed).",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of lines to read.",
            },
        },
        "required": ["path"],
    },
    "execute": execute_read,
}
