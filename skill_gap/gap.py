def compare_skills(user_skills: list, role_skills: list) -> dict:
    """Split a role's skills into ones the user has and ones they are missing."""
    user_set = {skill.strip().lower() for skill in user_skills}

    known_skills = []
    missing_skills = []

    for item in role_skills:
        name = item["name"].strip().lower()
        if name in user_set:
            known_skills.append(name)
        else:
            missing_skills.append(item)

    return {"known_skills": known_skills, "missing_skills": missing_skills}
