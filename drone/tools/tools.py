"""Tool registry."""

from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from openai.types.chat import ChatCompletionToolUnionParam

from drone.tools.bash import BASH_TOOL
from drone.tools.edit import EDIT_TOOL
from drone.tools.read import READ_TOOL
from drone.tools.write import WRITE_TOOL

ToolExecutor = Callable[[dict[str, Any]], Awaitable[str]]


@dataclass(frozen=True)
class Tool:
    """Definition of an agent tool."""

    name: str
    description: str
    parameters: dict[str, Any]
    execute: ToolExecutor


def _to_tool(tool_def: dict[str, Any]) -> Tool:
    return Tool(
        name=tool_def["name"],
        description=tool_def["description"],
        parameters=tool_def["parameters"],
        execute=tool_def["execute"],
    )


TOOL_LIST: list[Tool] = [
    _to_tool(READ_TOOL),
    _to_tool(WRITE_TOOL),
    _to_tool(EDIT_TOOL),
    _to_tool(BASH_TOOL),
]


def _build_tools_map(tools: list[Tool]) -> dict[str, Tool]:
    tools_map: dict[str, Tool] = {}
    for tool in tools:
        if tool.name in tools_map:
            raise ValueError(f"Duplicate tool name: {tool.name}")
        tools_map[tool.name] = tool
    return tools_map


TOOLS: dict[str, Tool] = _build_tools_map(TOOL_LIST)


def get_openai_tool_definitions() -> list[ChatCompletionToolUnionParam]:
    """Return tools in OpenAI-compatible function-calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            },
        }
        for tool in TOOL_LIST
    ]
