"""Basic example of using the ReAct agent."""

import asyncio
import os

from dotenv import load_dotenv
from drone import OpenAIProvider, ReActAgent


async def main():
    load_dotenv()

    # OpenRouter example: keep endpoint/model in code, API key in .env.
    provider = OpenAIProvider(
        model="openai/gpt-5.2",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    # Create agent
    agent = ReActAgent(
        provider=provider,
        max_iterations=5,
    )

    # Run a simple test
    result = await agent.run(
        message="Use bash to run `pwd` and return only the resulting path.",
    )

    print("Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
