from skill_gap.main import welcome_message


def test_welcome_message():
    assert "Skill Gap Analyzer" in welcome_message()