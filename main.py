"""
Deep Agents minimal example (LangChain-based, OpenAI-compatible API)

Docs: https://docs.langchain.com/oss/python/deepagents/overview
- create_deep_agent() to build the agent
- Built-in: todo list (write_todos), filesystem (read_file/write_file), subagents
- OpenAI config: .env OPENAI_API_KEY, OPENAI_API_BASE (optional), OPENAI_MODEL (optional)
- OPENAI_MINIMAL=1: use no tools and short prompt to fit small context (e.g. 4096)
"""

import os
from datetime import UTC, datetime

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env (OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL, OPENAI_MINIMAL)
load_dotenv()


def get_weather(city: str) -> str:
    """Return weather for the given city (example)."""
    return f"Weather in {city}: sunny, 22°C"


def get_current_time() -> str:
    """Return the current date and time in UTC (ISO format)."""
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def _print_tool_calls_and_responses(messages: list) -> None:
    """Print each tool call and its response from the message list."""
    for msg in messages:
        tool_calls = getattr(msg, "tool_calls", None) or []
        for tc in tool_calls:
            name = tc.get("name", "?")
            args = tc.get("args", {})
            print(f"  [Tool call] {name}({args})")
        # ToolMessage: has content and type "tool" or class name "ToolMessage"
        cls_name = type(msg).__name__
        content = getattr(msg, "content", None)
        if content and (cls_name == "ToolMessage" or getattr(msg, "type", "") == "tool"):
            print(f"  [Tool response] {content}")


def main() -> None:
    # --- Step 1: OpenAI-compatible API setup ---
    api_key = os.environ.get("OPENAI_API_KEY", "sk-dummy")
    base_url = os.environ.get("OPENAI_API_BASE")
    use_minimal = os.environ.get("OPENAI_MINIMAL", "").strip() in ("1", "true", "yes")

    if base_url:
        model = ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            api_key=api_key,
            base_url=base_url,
        )
        # Small context models (e.g. 4096): use tools=[] and short prompt
        tools = [] if use_minimal else [get_weather, get_current_time]
        agent = create_deep_agent(
            model=model,
            tools=tools,
            system_prompt=(
                "You are a friendly assistant for weather and time. Answer briefly."
                if use_minimal
                else "Use get_weather for weather, get_current_time for current time."
            ),
        )
    else:
        agent = create_deep_agent(
            model="openai:gpt-4o",
            tools=[get_weather, get_current_time],
            system_prompt="Use get_weather for weather, get_current_time for current time.",
        )

    # --- Step 2: Run agent ---
    user_query = "What's the weather in Seoul and what time is it now?"
    print("User:", user_query)
    print()

    result = agent.invoke({"messages": [{"role": "user", "content": user_query}]})

    messages = result.get("messages", [])

    # --- Step 3: Print tool calls and responses ---
    has_tool_calls = any(len(getattr(m, "tool_calls", None) or []) > 0 for m in messages)
    if has_tool_calls:
        print("--- Tool calls and responses ---")
        _print_tool_calls_and_responses(messages)
        print()

    # --- Step 4: Print final agent response ---
    last_message = messages[-1] if messages else None
    if last_message:
        content = getattr(last_message, "content", None) or ""
        print("Agent response:", content)


if __name__ == "__main__":
    main()
