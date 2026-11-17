import pytest

from skill_gap import extractor


def fake_llm(reply):
    """Make a fake ask_llm that always returns the given reply."""
    return lambda prompt: reply


def test_clean_json_reply(monkeypatch):
    reply = '[{"name": "Python", "requirement_type": "Required"}, {"name": "Docker", "requirement_type": "Preferred"}]'
    monkeypatch.setattr(extractor, "ask_llm", fake_llm(reply))
    assert extractor.extract_skills("some job posting") == [
        {"name": "python", "requirement_type": "Required"},
        {"name": "docker", "requirement_type": "Preferred"},
    ]


def test_extra_text_around_json(monkeypatch):
    reply = (
        "Sure! Here is your JSON:\n```json\n"
        '[{"name": "SQL", "requirement_type": "Required"}]\n'
        "```\nLet me know if you need anything else."
    )
    monkeypatch.setattr(extractor, "ask_llm", fake_llm(reply))
    assert extractor.extract_skills("text") == [{"name": "sql", "requirement_type": "Required"}]


def test_duplicates_removed_and_names_cleaned(monkeypatch):
    reply = (
        '[{"name": "  Python ", "requirement_type": "Required"},'
        ' {"name": "python", "requirement_type": "Preferred"},'
        ' {"name": "Git", "requirement_type": "Required"},'
        ' {"name": "GIT", "requirement_type": "Required"}]'
    )
    monkeypatch.setattr(extractor, "ask_llm", fake_llm(reply))
    assert extractor.extract_skills("text") == [
        {"name": "python", "requirement_type": "Required"},
        {"name": "git", "requirement_type": "Required"},
    ]


def test_not_json_raises_clear_error(monkeypatch):
    monkeypatch.setattr(extractor, "ask_llm", fake_llm("Sorry, I can't help with that."))
    with pytest.raises(ValueError, match="The LLM did not return valid JSON."):
        extractor.extract_skills("text")


def test_broken_json_raises_clear_error(monkeypatch):
    monkeypatch.setattr(extractor, "ask_llm", fake_llm('[{"name": "Python", }]'))
    with pytest.raises(ValueError, match="The LLM did not return valid JSON."):
        extractor.extract_skills("text")


def test_prompt_comes_from_file_with_text_filled_in(monkeypatch):
    sent = {}

    def capture(prompt):
        sent["prompt"] = prompt
        return "[]"

    monkeypatch.setattr(extractor, "ask_llm", capture)
    extractor.extract_skills("I know Rust and Go.")
    assert "I know Rust and Go." in sent["prompt"]
    assert "{text}" not in sent["prompt"]
    assert "requirement_type" in sent["prompt"]


def test_falls_back_when_llm_fails(monkeypatch):
    def broken_llm(prompt):
        raise RuntimeError("503 UNAVAILABLE")

    monkeypatch.setattr(extractor, "ask_llm", broken_llm)
    monkeypatch.setattr(
        extractor,
        "extract_skills_spacy",
        lambda text: [{"name": "Python", "requirement_type": "Required"}],
    )
    assert extractor.extract_skills("text") == [{"name": "python", "requirement_type": "Required"}]


def test_raises_llm_error_when_no_fallback(monkeypatch):
    def broken_llm(prompt):
        raise RuntimeError("503 UNAVAILABLE")

    def no_spacy(text):
        raise ImportError("No module named 'spacy'")

    monkeypatch.setattr(extractor, "ask_llm", broken_llm)
    monkeypatch.setattr(extractor, "extract_skills_spacy", no_spacy)
    with pytest.raises(RuntimeError, match="503"):
        extractor.extract_skills("text")


def test_spacy_fallback_finds_skills():
    spacy = pytest.importorskip("spacy")
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        pytest.skip("en_core_web_sm is not installed")
    names = [s["name"] for s in extractor.extract_skills_spacy("Built apps in Python and JS with Docker.")]
    assert "Python" in names
    assert "JavaScript" in names
    assert "Docker" in names
