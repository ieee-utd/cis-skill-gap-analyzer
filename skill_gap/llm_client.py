"""Thin wrapper around the LLM provider (Google Gemini)."""

from google import genai

from skill_gap.config import get_api_key

MODEL = "gemini-flash-latest"


def ask_llm(prompt):
    """Send a prompt to the LLM and return the text response."""
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text
