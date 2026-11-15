"""Run the real extractors on the sample resumes in examples/resumes/."""

from pathlib import Path

from skill_gap.docx_extractor import extract_text_from_docx
from skill_gap.pdf_extractor import extract_text_from_pdf

RESUMES = Path(__file__).resolve().parent.parent / "examples" / "resumes"


def path(name):
    return str(RESUMES / name)


def assert_skills_in(text, skills):
    for skill in skills:
        assert skill in text, f"{skill!r} not found in extracted text"


def test_plain_pdf():
    text = extract_text_from_pdf(path("plain_resume.pdf"))
    assert_skills_in(text, ["Python", "SQL", "Git"])


def test_plain_docx():
    text = extract_text_from_docx(path("plain_resume.docx"))
    assert_skills_in(text, ["Python", "SQL", "Git"])


def test_two_column_pdf():
    text = extract_text_from_pdf(path("two_column_resume.pdf"))
    assert_skills_in(text, ["Java", "Docker", "Linux"])


def test_skills_table_pdf():
    text = extract_text_from_pdf(path("skills_table_resume.pdf"))
    assert_skills_in(text, ["Python", "Docker", "AWS"])


def test_skills_table_docx():
    text = extract_text_from_docx(path("skills_table_resume.docx"))
    assert_skills_in(text, ["Python", "Docker", "AWS"])
