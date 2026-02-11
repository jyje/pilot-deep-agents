# pilot-deep-agents

A **LangChain-based** Python example following the [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) docs. It works with **OpenAI-compatible APIs**.

## Summary

| Item | Description |
|------|-------------|
| Entry point | `main.py` |
| Python | 3.12+ (see `.python-version`) |
| Package manager | [uv](https://docs.astral.sh/uv/), `pyproject.toml` |
| Environment | `.env` (sample: `.env.example` — copy to use) |
| Lint / format | ruff, ty (dev dependencies) |

## Install

```bash
# Create venv and install dependencies (Python 3.12)
uv sync

# Include dev tools (ruff, ty)
uv sync --group dev
```

## Environment (.env)

API key and endpoint are configured via **`.env`**. `.env` is not committed to git.

**`.env.example`** is the sample file. **Copy it to `.env`** and use as-is or edit as needed.

```bash
cp .env.example .env
```

### Variables

| Variable | Required | Description |
|----------|:--------:|-------------|
| `OPENAI_API_KEY` | ✅ | API key |
| `OPENAI_API_BASE` | | OpenAI-compatible endpoint URL (omit to use OpenAI official API) |
| `OPENAI_MODEL` | | Model name (default with base: gpt-4o) |
| `OPENAI_MINIMAL` | | Set to `1` for small-context models (e.g. 4096 tokens); uses no tools |

## Run

```bash
uv run python main.py
```

### Example output

The script asks the agent a composite question (weather + current time). Tool calls and their responses are printed, then the final answer.

```
User: What's the weather in Seoul and what time is it now?

--- Tool calls and responses ---
  [Tool call] get_weather({'city': 'Seoul'})
  [Tool call] get_current_time({})
  [Tool response] Weather in Seoul: sunny, 22°C
  [Tool response] 2026-02-11 21:50:50 UTC

Agent response: The weather in Seoul is sunny with a temperature of 22°C. The current time in UTC is 2026-02-11 21:50:50.
```

## Lint / format (dev)

```bash
uv sync --group dev
uv run ruff check . && uv run ruff format .
uv run ty check .
```

## Example stack

- **deepagents** `create_deep_agent()`: built-in todo list (write_todos), filesystem (read_file/write_file), subagents
- **langchain-openai** `ChatOpenAI`: OpenAI-compatible API (base_url supported)
- **python-dotenv**: loads `.env`
- Custom tools `get_weather` and `get_current_time`; tool calls and responses are printed

## References

- [Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [Deep Agents Customization](https://docs.langchain.com/oss/python/deepagents/customization)
