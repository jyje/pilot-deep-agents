"""
Deep Agents minimal example (LangChain-based, OpenAI-compatible API)

Docs: https://docs.langchain.com/oss/python/deepagents/overview
- create_deep_agent() to build the agent
- Built-in: todo list (write_todos), filesystem (read_file/write_file), subagents
- OpenAI config: .env OPENAI_API_KEY, OPENAI_API_BASE (optional), OPENAI_MODEL (optional)
"""

import os

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env (OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL)
load_dotenv()


def get_weather(city: str) -> str:
    """Return weather for the given city (example)."""
    return f"Weather in {city}: sunny, 22°C"


def main() -> None:
    # OpenAI-compatible API setup
    # 1) OpenAI official: set OPENAI_API_KEY only, use model="openai:gpt-4o" etc.
    # 2) Custom endpoint: pass ChatOpenAI(base_url="https://...") instance
    api_key = os.environ.get("OPENAI_API_KEY", "sk-dummy")
    base_url = os.environ.get("OPENAI_API_BASE")  # e.g. Azure, other compatible services

    if base_url:
        # Custom endpoint (e.g. Azure). Use tools=[] for chat-only if tool calling unsupported
        model = ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            api_key=api_key,
            base_url=base_url,
        )
        agent = create_deep_agent(
            model=model,
            tools=[get_weather],
            system_prompt="You are a friendly weather assistant. Tell the user about the weather.",
        )
    else:
        # Default: provider:model string (OpenAI official API)
        agent = create_deep_agent(
            model="openai:gpt-4o",
            tools=[get_weather],
            system_prompt="You are a friendly weather assistant. Tell the user about the weather.",
        )

    # Run
    result = agent.invoke({
        "messages": [{"role": "user", "content": "What's the weather in Seoul?"}]
    })

    last_message = result["messages"][-1]
    print("Agent response:", last_message.content)


if __name__ == "__main__":
    main()
