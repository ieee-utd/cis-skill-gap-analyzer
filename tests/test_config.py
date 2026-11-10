import pytest

from skill_gap import config


def test_missing_key_shows_helpful_error(monkeypatch):
    # Don't read a real .env file, and make sure no real key is set
    monkeypatch.setattr(config, "load_dotenv", lambda: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(RuntimeError) as error:
        config.get_api_key()

    assert "GEMINI_API_KEY not found" in str(error.value)
    assert "Copy .env.example to .env" in str(error.value)  