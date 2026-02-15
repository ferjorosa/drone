"""Bash tool."""

import asyncio
from typing import Any


async def execute_bash(arguments: dict[str, Any]) -> str:
    """Execute a bash command."""
    command = arguments.get("command")
    timeout = arguments.get("timeout")

    if not isinstance(command, str) or not command.strip():
        return "Error: 'command' must be a non-empty string."

    if timeout is not None and not isinstance(timeout, (int, float)):
        return "Error: 'timeout' must be a number when provided."

    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            if timeout is None:
                stdout, stderr = await process.communicate()
            else:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=float(timeout)
                )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return f"Error: command timed out after {timeout} seconds."

        output = stdout.decode() if stdout else ""
        error = stderr.decode() if stderr else ""

        if error:
            return f"stdout:\n{output}\nstderr:\n{error}"
        return output
    except Exception as exc:
        return f"Error executing command: {exc}"


BASH_TOOL: dict[str, Any] = {
    "name": "bash",
    "description": "Execute a bash command in the current working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "Bash command to execute"},
            "timeout": {
                "type": "number",
                "description": "Timeout in seconds (optional).",
            },
        },
        "required": ["command"],
    },
    "execute": execute_bash,
}
