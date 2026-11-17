"""Clean up messy text pulled out of PDF and DOCX resumes."""

import re

# Bullet symbols that show up at the start of a line in extracted resume text.
BULLETS = "•▪●◦–■○‣"
_LEADING_BULLET = re.compile(rf"^[ \t]*[{BULLETS}]")


def clean_text(text: str) -> str:
    """Return a cleaned-up copy of messy resume text.

    In: a string from a PDF or DOCX, with bullet symbols, tabs, runs of spaces
    and blank lines.
    Out: one string where bullets are removed, whitespace is collapsed to single
    spaces, every line is stripped and blank lines are dropped. Capital letters
    are left alone (lowercasing happens later, when skills are compared).
    """
    cleaned_lines = []
    for line in text.splitlines():
        line = _LEADING_BULLET.sub("", line)
        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)
