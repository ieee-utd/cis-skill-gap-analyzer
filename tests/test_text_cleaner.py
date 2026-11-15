from skill_gap.text_cleaner import clean_text


def test_removes_bullets_and_extra_spaces():
    messy = "• Python   and\tSQL\n▪  Built   a   tool\n●Led team\n◦ Git\n– Docker"
    assert clean_text(messy) == "Python and SQL\nBuilt a tool\nLed team\nGit\nDocker"


def test_removes_blank_lines():
    messy = "Python\n\n   \n\t\nSQL\n\n"
    assert clean_text(messy) == "Python\nSQL"


def test_empty_string_returns_empty_string():
    assert clean_text("") == ""


def test_whitespace_only_returns_empty_string():
    assert clean_text("  \n\t \n") == ""


def test_keeps_capital_letters_and_normal_words():
    text = "Skills: Python, SQL, AWS\nMicrosoft Excel"
    assert clean_text(text) == text


def test_strips_each_line():
    assert clean_text("   Python   \n   SQL") == "Python\nSQL"


def test_bullet_in_middle_of_line_is_kept():
    assert clean_text("Python • SQL") == "Python • SQL"
