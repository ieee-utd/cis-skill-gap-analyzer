"""Configuration helpers. Loads secrets from the .env file."""

import os

from dotenv import load_dotenv


def get_api_key():
    """Return the LLM API key from .env (LLM_API_KEY)."""
    load_dotenv()
    key = os.getenv("LLM_API_KEY")
    if not key or key == "your-key-here":
        raise RuntimeError("LLM_API_KEY is missing. Copy .env.example to .env and add your key.")
    return key
