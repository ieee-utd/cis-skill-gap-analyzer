"""Turn resume or job posting text into a clean list of skills using the LLM."""

import json
import logging
from pathlib import Path

from skill_gap.llm_client import ask_llm

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = REPO_ROOT / "prompts" / "extract_skills.txt"
FALLBACK_SKILLS_FILE = REPO_ROOT / "experiments" / "skills.txt"

# Other ways people write the skills in skills.txt (from the AB#17 experiment).
SYNONYMS = {
    "ML": "Machine Learning",
    "machine-learning": "Machine Learning",
    "deep-learning": "Deep Learning",
    "NLP": "Natural Language Processing",
    "computer-vision": "Computer Vision",
    "CV": "Computer Vision",
    "JS": "JavaScript",
    "Postgres": "PostgreSQL",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "Amazon Web Services": "AWS",
    "REST endpoints": "REST APIs",
    "REST API": "REST APIs",
    "MS Excel": "Excel",
    "scrum": "Agile",
    "data analysis": "Data Analysis",
}

logger = logging.getLogger(__name__)


def extract_skills(text: str) -> list:
    """Send text to the LLM and return a list of {"name", "requirement_type"} dicts.

    Names are lowercase and trimmed, with duplicates removed (first one wins).
    Raises ValueError if the LLM reply is not valid JSON.
    If the LLM call itself fails, falls back to spaCy matching when spaCy is installed.
    """
    with open(PROMPT_FILE, encoding="utf-8") as f:
        prompt = f.read()
    prompt = prompt.replace("{text}", text)

    try:
        reply = ask_llm(prompt)
    except Exception as llm_error:
        logger.warning("LLM call failed (%s). Falling back to spaCy matching.", llm_error)
        try:
            skills = extract_skills_spacy(text)
        except (ImportError, OSError):
            # spaCy or its English model is not installed, so there is no fallback.
            raise llm_error
        return clean_skills(skills)

    # Keep only the part from the first [ to the last ], in case the LLM adds extra text.
    start = reply.find("[")
    end = reply.rfind("]")
    json_text = reply[start : end + 1] if start != -1 and end > start else reply

    try:
        skills = json.loads(json_text)
    except json.JSONDecodeError:
        raise ValueError("The LLM did not return valid JSON.")

    if not isinstance(skills, list):
        raise ValueError("The LLM did not return a JSON list.")

    return clean_skills(skills)


def clean_skills(skills: list) -> list:
    """Lowercase and strip every name, and drop duplicates and empty names."""
    cleaned = []
    seen = set()
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        name = str(skill.get("name", "")).strip().lower()
        if not name or name in seen:
            continue
        seen.add(name)
        cleaned.append(
            {
                "name": name,
                "requirement_type": skill.get("requirement_type", "Required"),
            }
        )
    return cleaned


def extract_skills_spacy(text: str) -> list:
    """Backup extractor: match skills from experiments/skills.txt with spaCy (no API needed).

    It cannot tell required from preferred, so every skill is marked "Required".
    Raises ImportError or OSError if spaCy or en_core_web_sm is not installed.
    """
    import spacy
    from spacy.matcher import PhraseMatcher

    with open(FALLBACK_SKILLS_FILE, encoding="utf-8") as f:
        skills = [line.strip() for line in f if line.strip()]

    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    for skill in skills:
        matcher.add(skill, [nlp.make_doc(skill)])
    for alt, official in SYNONYMS.items():
        if official in skills:
            matcher.add(official, [nlp.make_doc(alt)])

    doc = nlp(text)
    found = {nlp.vocab.strings[match_id] for match_id, _, _ in matcher(doc)}
    return [{"name": s, "requirement_type": "Required"} for s in skills if s in found]
