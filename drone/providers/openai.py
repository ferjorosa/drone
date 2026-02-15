"""OpenAI-compatible LLM provider."""

import json
from dataclasses import dataclass
from typing import Any, Iterable

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolUnionParam

from drone.providers.base import LLMResponse, ToolCallRequest


@dataclass
class OpenAIProvider:
    """OpenAI-compatible provider (works with OpenAI, vLLM, Ollama, etc.)."""

    model: str = "gpt-4o-mini"
    base_url: str | None = None
    api_key: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7

    def __post_init__(self):
        self._client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    async def chat(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        tools: Iterable[ChatCompletionToolUnionParam] | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> LLMResponse:
        """Send a chat completion request."""
        resolved_model = model or self.model
        resolved_max_tokens = self.max_tokens if max_tokens is None else max_tokens
        resolved_temperature = self.temperature if temperature is None else temperature

        try:
            if tools:
                response = await self._client.chat.completions.create(
                    model=resolved_model,
                    messages=messages,
                    max_tokens=resolved_max_tokens,
                    temperature=resolved_temperature,
                    tools=tools,
                    tool_choice="auto",
                )
            else:
                response = await self._client.chat.completions.create(
                    model=resolved_model,
                    messages=messages,
                    max_tokens=resolved_max_tokens,
                    temperature=resolved_temperature,
                )
            return self._parse_response(response)
        except Exception as e:
            return LLMResponse(
                content=f"Error calling LLM: {str(e)}",
                finish_reason="error",
            )

    def _parse_response(self, response: Any) -> LLMResponse:
        """Parse OpenAI response into standard format."""
        choice = response.choices[0]
        message = choice.message

        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                args = tc.function.arguments
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {"raw": args}

                tool_calls.append(
                    ToolCallRequest(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=args,
                    )
                )

        return LLMResponse(
            content=message.content,
            tool_calls=tool_calls,
            finish_reason=choice.finish_reason or "stop",
        )

    def get_default_model(self) -> str:
        return self.model
