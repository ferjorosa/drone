"""Shared provider response types."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCallRequest:
    """A tool call request from the LLM."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    """Response from an LLM provider."""

    content: str | None
    tool_calls: list[ToolCallRequest] = field(default_factory=list)
    finish_reason: str = "stop"
    reasoning_content: str | None = None

    @property
    def has_tool_calls(self) -> bool:
        """Check if response contains tool calls."""
        return len(self.tool_calls) > 0
