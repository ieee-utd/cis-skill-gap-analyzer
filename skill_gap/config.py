import os

from dotenv import load_dotenv


def get_api_key() -> str:
    """Load GEMINI_API_KEY from the .env file and return it."""
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Copy .env.example to .env and add your key."
        )
    return key 