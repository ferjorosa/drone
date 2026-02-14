"""Basic example of using the ReAct agent."""

import asyncio
import os

from drone import OpenAIProvider, ReActAgent


async def main():
    # Create provider - uses OPENAI_API_KEY env var by default
    # For vLLM or other OpenAI-compatible servers, set base_url
    provider = OpenAIProvider(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        base_url=os.getenv("OPENAI_BASE_URL"),  # e.g., "http://localhost:8000/v1"
        api_key=os.getenv("OPENAI_API_KEY", "dummy-key-for-local"),
    )

    # Create agent
    agent = ReActAgent(
        provider=provider,
        max_iterations=5,
    )

    # Run a simple test
    result = await agent.run(
        message="What is the current directory? Use bash to check.",
    )

    print("Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
