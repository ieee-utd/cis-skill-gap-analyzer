import json
from pathlib import Path

import pytest

from skill_gap.roles import get_role, list_role_names, load_roles


@pytest.fixture
def roles():
    return [
        {
            "role": "Software Engineer",
            "skills": [{"name": "python", "requirement_type": "Required"}],
        },
        {
            "role": "Data Analyst",
            "skills": [{"name": "sql", "requirement_type": "Preferred"}],
        },
    ]


@pytest.fixture
def roles_path(tmp_path, roles):
    path = tmp_path / "roles.json"
    path.write_text(json.dumps(roles), encoding="utf-8")
    return path


def test_load_roles(roles_path, roles):
    assert load_roles(str(roles_path)) == roles


def test_load_roles_default_path(roles_path, roles, monkeypatch):
    monkeypatch.chdir(roles_path.parent)
    assert load_roles() == roles


@pytest.mark.parametrize("missing_key", ["role", "skills"])
def test_load_roles_missing_key_reports_position(tmp_path, roles, missing_key):
    del roles[1][missing_key]
    path = tmp_path / "broken.json"
    path.write_text(json.dumps(roles), encoding="utf-8")

    with pytest.raises(ValueError, match=f"index 1.*'{missing_key}'"):
        load_roles(str(path))


def test_load_roles_requires_list(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="must be a list"):
        load_roles(str(path))


def test_load_roles_requires_role_object(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text('["Software Engineer"]', encoding="utf-8")
    with pytest.raises(ValueError, match="index 0.*must be an object"):
        load_roles(str(path))


def test_load_roles_empty_list(tmp_path):
    path = tmp_path / "roles.json"
    path.write_text("[]", encoding="utf-8")
    assert load_roles(str(path)) == []


def test_load_roles_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_roles(str(tmp_path / "missing.json"))


def test_load_roles_invalid_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_roles(str(path))


def test_list_role_names_sorted_without_mutation(roles_path):
    roles = load_roles(str(roles_path))
    assert list_role_names(roles) == ["Data Analyst", "Software Engineer"]
    assert roles[0]["role"] == "Software Engineer"


def test_list_role_names_empty():
    assert list_role_names([]) == []


@pytest.mark.parametrize(
    "name",
    [
        "Software Engineer",
        "software engineer",
        "SOFTWARE ENGINEER",
        " software engineer ",
        "\tSoftware   Engineer\n",
    ],
)
def test_get_role_normalizes_name(roles_path, name):
    roles = load_roles(str(roles_path))
    assert get_role(roles, name) is roles[0]


def test_get_role_normalizes_stored_title(roles):
    roles[0]["role"] = " Software   Engineer "
    assert get_role(roles, "software engineer") is roles[0]


def test_get_role_not_found(roles):
    assert get_role(roles, "Astronaut") is None


def test_get_role_empty_list():
    assert get_role([], "Software Engineer") is None


def test_functions_with_real_roles():
    path = Path(__file__).resolve().parents[1] / "roles.json"
    roles = load_roles(str(path))
    assert roles
    assert list_role_names(roles) == sorted(role["role"] for role in roles)
    assert get_role(roles, " software engineer ")["role"] == "Software Engineer"
    for title in ("Machine Learning Engineer", "Embedded Software Engineer"):
        assert get_role(roles, title) in roles
