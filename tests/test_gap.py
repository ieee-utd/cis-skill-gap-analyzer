from skill_gap.gap import compare_skills

ROLE_SKILLS = [
    {"name": "python", "requirement_type": "Required"},
    {"name": "sql", "requirement_type": "Required"},
    {"name": "docker", "requirement_type": "Preferred"},
]


def test_splits_known_and_missing():
    result = compare_skills(["python", "git"], ROLE_SKILLS)
    assert result["known_skills"] == ["python"]
    assert result["missing_skills"] == [
        {"name": "sql", "requirement_type": "Required"},
        {"name": "docker", "requirement_type": "Preferred"},
    ]


def test_cleans_case_and_spaces():
    result = compare_skills(["Python", " sql "], ROLE_SKILLS)
    assert result["known_skills"] == ["python", "sql"]
    assert result["missing_skills"] == [
        {"name": "docker", "requirement_type": "Preferred"}
    ]


def test_user_has_no_skills():
    result = compare_skills([], ROLE_SKILLS)
    assert result["known_skills"] == []
    assert result["missing_skills"] == ROLE_SKILLS


def test_role_has_no_skills():
    result = compare_skills(["python"], [])
    assert result == {"known_skills": [], "missing_skills": []}


def test_user_has_everything():
    result = compare_skills(["python", "sql", "docker"], ROLE_SKILLS)
    assert result["known_skills"] == ["python", "sql", "docker"]
    assert result["missing_skills"] == []
