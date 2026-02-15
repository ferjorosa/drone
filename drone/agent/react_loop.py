"""ReAct agent loop."""

import json
from typing import Any

from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolMessageParam

from drone.providers.openai import OpenAIProvider
from drone.tools.tools import TOOLS, get_openai_tool_definitions


class ReActAgent:
    """
    Simple ReAct (Reasoning + Acting) agent loop.

    The agent:
    1. Receives a message
    2. Calls the LLM
    3. If LLM outputs a bash command, execute it
    4. Loop until final response
    """

    def __init__(
        self,
        provider: OpenAIProvider,
        max_iterations: int = 10,
    ):
        self.provider = provider
        self.max_iterations = max_iterations

    async def run(self, message: str, system_prompt: str | None = None) -> str:
        """
        Run the agent on a single message.

        Args:
            message: User message.
            system_prompt: Optional system prompt.

        Returns:
            Final agent response.
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": message})

        return await self._run_loop(messages)

    async def _run_loop(self, messages: list[ChatCompletionMessageParam]) -> str:
        """Run the ReAct loop until completion."""

        for iteration in range(self.max_iterations):
            response = await self.provider.chat(
                messages=messages,
                tools=get_openai_tool_definitions(),
            )

            if response.has_tool_calls:
                # Add assistant message with tool calls
                messages.append(
                    {
                        "role": "assistant",
                        "content": response.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.name,
                                    "arguments": json.dumps(tc.arguments),
                                },
                            }
                            for tc in response.tool_calls
                        ],
                    }
                )

                # Execute each tool call
                for tool_call in response.tool_calls:
                    result = await self._execute_tool(
                        tool_call.name, tool_call.arguments
                    )
                    tool_message: ChatCompletionToolMessageParam = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                    messages.append(tool_message)

                # Continue loop
                messages.append({"role": "user", "content": "What is the next step?"})
            else:
                # No tool calls, we're done
                return response.content or ""

        return "Max iterations reached without final response."

    async def _execute_tool(self, name: str, arguments: dict[str, Any]) -> str:
        """Execute a tool by name."""
        tool = TOOLS.get(name)
        if tool is None:
            return f"Error: Unknown tool '{name}'"
        return await tool.execute(arguments)
