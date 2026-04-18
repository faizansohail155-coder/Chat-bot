"""Minimal CLI chatbot backed by the OpenAI API.

Usage:
    export OPENAI_API_KEY=sk-...
    python chatbot.py

Optional environment variables:
    OPENAI_MODEL   - model name (default: gpt-4o-mini)
    SYSTEM_PROMPT  - override the default system prompt
"""

from __future__ import annotations

import os
import sys
from typing import List, Dict

try:
    from openai import OpenAI
    from openai import (
        APIConnectionError,
        APIStatusError,
        AuthenticationError,
        RateLimitError,
    )
except ImportError:
    sys.stderr.write(
        "Missing dependency 'openai'. Install it with:\n"
        "    pip install -r requirements.txt\n"
    )
    sys.exit(1)


DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    "You are a concise, helpful assistant. Keep answers short and clear.",
)


def build_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.stderr.write(
            "OPENAI_API_KEY is not set. Export it first:\n"
            "    export OPENAI_API_KEY=sk-...\n"
        )
        sys.exit(1)
    return OpenAI(api_key=api_key)


def chat_once(client: OpenAI, messages: List[Dict[str, str]], model: str) -> str:
    """Send the conversation to the API and return the assistant reply."""
    try:
        response = client.chat.completions.create(model=model, messages=messages)
    except AuthenticationError:
        return "[error] Invalid OPENAI_API_KEY. Please check your credentials."
    except RateLimitError:
        return "[error] Rate limit or quota exceeded. Try again shortly."
    except APIConnectionError:
        return "[error] Network issue reaching OpenAI. Check your connection."
    except APIStatusError as exc:
        return f"[error] OpenAI API returned status {exc.status_code}."
    except Exception as exc:  # noqa: BLE001 - last-resort safety net for a CLI
        return f"[error] Unexpected error: {exc}"

    choice = response.choices[0].message.content if response.choices else None
    return choice or "[error] Empty response from the model."


def run() -> int:
    client = build_client()
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT}
    ]

    print(f"Chatbot ready (model={DEFAULT_MODEL}). Type 'exit' or Ctrl-D to quit.")
    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", ":q"}:
            return 0

        messages.append({"role": "user", "content": user_input})
        reply = chat_once(client, messages, DEFAULT_MODEL)
        messages.append({"role": "assistant", "content": reply})
        print(f"bot> {reply}")


if __name__ == "__main__":
    raise SystemExit(run())
