"""Load target roles and find their titles and skill requirements."""

import json


def load_roles(path: str = "roles.json") -> list:
    """Read roles from JSON, requiring a title and skills for every entry."""
    with open(path) as f:
        roles = json.load(f)

    if not isinstance(roles, list):
        raise ValueError("Role data must be a list.")

    for position, role in enumerate(roles):
        if not isinstance(role, dict):
            raise ValueError(f"Role at index {position} must be an object.")
        for key in ("role", "skills"):
            if key not in role:
                raise ValueError(f"Role at index {position} is missing '{key}'.")

    return roles


def list_role_names(roles: list) -> list:
    """Return role titles in alphabetical order without changing the input."""
    return sorted(role["role"] for role in roles)


def get_role(roles: list, name: str) -> dict | None:
    """Find a role ignoring case and extra whitespace, or return None."""
    normalized_name = " ".join(name.split()).casefold()
    for role in roles:
        if " ".join(role["role"].split()).casefold() == normalized_name:
            return role
    return None
