"""Turn the skills a student types by hand into a clean list."""


def parse_skill_input(text: str) -> list:
    """Parse typed skills into a clean list.

    In: a string with skills separated by commas, new lines, or both.
    Out: a list of lowercase skills with extra spaces, empty entries and
    duplicates removed. The order the student typed them in is kept.
    """
    pieces = text.replace("\r", "").replace("\n", ",").split(",")
    skills = []
    for piece in pieces:
        skill = piece.strip().lower()
        if skill and skill not in skills:
            skills.append(skill)
    return skills
