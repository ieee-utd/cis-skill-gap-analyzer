"""
AB#17 - Choose extraction approach
Compares 3 ways to pull skills out of resume text
  1. Keyword matching
  2. spaCy PhraseMatcher (+ synonyms)
  3. LLM API (Gemini)

"""

import argparse
import json
import os
import re
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

RESUME_FILE = "sample_resume.txt"
SKILLS_FILE = "skills.txt"
ANSWER_KEY_FILE = "answer_key.txt"


def load_lines(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def load_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()



# 1. Keyword matching

def extract_keyword(resume_text, skills):
    """Exact word match against the master skills list (case-insensitive)."""
    found = []
    text = resume_text.lower()
    for skill in skills:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)
    return found



# 2. spaCy PhraseMatcher with synonyms

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
    "analyze": "Data Analysis",
    "data analysis": "Data Analysis",
}


def extract_spacy(resume_text, skills):
    import spacy
    from spacy.matcher import PhraseMatcher

    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    for skill in skills:
        matcher.add(skill, [nlp.make_doc(skill)])
    for alt, official in SYNONYMS.items():
        if official in skills:
            matcher.add(official, [nlp.make_doc(alt)])

    doc = nlp(resume_text)
    found = set()
    for match_id, start, end in matcher(doc):
        found.add(nlp.vocab.strings[match_id])
    return [s for s in skills if s in found]



# 3. LLM API (Gemini)

def get_gemini_key():
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def extract_llm(resume_text, skills):
    """Asks Gemini to pick skills from our master list. Needs GEMINI_API_KEY."""
    from google import genai

    client = genai.Client(api_key=get_gemini_key())
    model = os.environ.get("LLM_MODEL", "gemini-3.8-flash")
    prompt = (
        "Here is a master list of skills:\n"
        + "\n".join(skills)
        + "\n\nRead the resume below and return ONLY a JSON array of the skills "
        "from the master list that this person has, even if the resume words "
        "them differently. Use the exact names from the master list. "
        "No other text.\n\nRESUME:\n" + resume_text
    )
    # Gemini sometimes returns 503 (server busy), so retry a few times
    for attempt in range(5):
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            break
        except Exception as e:
            busy = "503" in str(e) or "UNAVAILABLE" in str(e) or "overloaded" in str(e).lower()
            if not busy or attempt == 4:
                raise
            wait = 5 * 2 ** attempt
            print(f"Gemini busy, retrying in {wait}s...")
            time.sleep(wait)
    raw = response.text.strip()
    raw = raw[raw.find("["): raw.rfind("]") + 1]  # strip any extra text
    result = json.loads(raw)
    return [s for s in skills if s in result]



# Compare

def score(found, answer_key):
    found_set, key_set = set(found), set(answer_key)
    correct = found_set & key_set
    missed = sorted(key_set - found_set)
    extra = sorted(found_set - key_set)
    return len(correct), missed, extra


def main():
    parser = argparse.ArgumentParser(description="Compare skill extraction methods")
    parser.add_argument("--input", default=RESUME_FILE, help="resume or job description .txt")
    parser.add_argument("--key", default=ANSWER_KEY_FILE, help="answer key .txt (one skill per line)")
    parser.add_argument("--no-llm", action="store_true", help="skip the Gemini test")
    args = parser.parse_args()

    resume = load_text(args.input)
    skills = load_lines(SKILLS_FILE)
    answer_key = load_lines(args.key)
    print(f"Input: {args.input}  Answer key: {args.key}\n")

    methods = [("Keyword", extract_keyword), ("spaCy", extract_spacy)]
    if args.no_llm:
        pass
    elif get_gemini_key():
        methods.append(("LLM (Gemini)", extract_llm))
    else:
        print("NOTE: GEMINI_API_KEY not found, skipping the LLM test.\n")

    rows = []
    for name, func in methods:
        start = time.perf_counter()
        try:
            found = func(resume, skills)
        except Exception as e:
            print(f"{name} failed: {e}\n")
            continue
        seconds = time.perf_counter() - start
        correct, missed, extra = score(found, answer_key)
        rows.append((name, correct, missed, extra, seconds))

        print(f"=== {name} ===")
        print(f"Found ({len(found)}): {found}")
        print(f"Missed: {missed}")
        print(f"Wrong/extra: {extra}")
        print(f"Time: {seconds:.2f}s\n")

    # markdown
    print("| Method | Correct (of %d) | Missed | Wrong/extra | Time |" % len(answer_key))
    print("|---|---|---|---|---|")
    for name, correct, missed, extra, seconds in rows:
        print(f"| {name} | {correct} | {len(missed)} | {len(extra)} | {seconds:.2f}s |")


if __name__ == "__main__":
    main()
