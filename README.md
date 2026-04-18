# Minimal CLI Chatbot

A tiny Python CLI chatbot backed by the OpenAI API. Keeps conversation context
across turns and handles network/auth/rate-limit errors gracefully without
crashing.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Run

```bash
python chatbot.py
```

Type your message at the `you>` prompt. Type `exit`, `quit`, `:q`, or press
Ctrl-D to leave.

## Configuration

All via environment variables:

| Variable         | Default                                                   |
|------------------|-----------------------------------------------------------|
| `OPENAI_API_KEY` | _required_                                                |
| `OPENAI_MODEL`   | `gpt-4o-mini`                                             |
| `SYSTEM_PROMPT`  | `You are a concise, helpful assistant. Keep answers short and clear.` |

## Error handling

The bot never crashes on API issues. Instead it prints a readable message and
keeps the REPL open:

- Invalid API key -> `[error] Invalid OPENAI_API_KEY...`
- Rate limit / quota -> `[error] Rate limit or quota exceeded...`
- Network failure -> `[error] Network issue reaching OpenAI...`
- Any other API status -> `[error] OpenAI API returned status <code>.`
