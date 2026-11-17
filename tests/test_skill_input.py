from skill_gap.skill_input import parse_skill_input


def test_comma_separated():
    assert parse_skill_input("Python, SQL") == ["python", "sql"]


def test_one_per_line():
    assert parse_skill_input("Python\nSQL") == ["python", "sql"]


def test_windows_line_endings():
    assert parse_skill_input("Python\r\nSQL") == ["python", "sql"]


def test_mixed_commas_and_new_lines():
    assert parse_skill_input("Python, SQL\nGit") == ["python", "sql", "git"]


def test_extra_spaces_empty_entries_and_duplicates():
    assert parse_skill_input(" Python ,, python , Git ") == ["python", "git"]


def test_keeps_typed_order():
    assert parse_skill_input("SQL, Python, Git") == ["sql", "python", "git"]


def test_empty_string_returns_empty_list():
    assert parse_skill_input("") == []


def test_only_separators_returns_empty_list():
    assert parse_skill_input(" , \n , ") == []
