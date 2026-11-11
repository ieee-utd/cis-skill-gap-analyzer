# AI Skill Gap Analyzer Data Format Specification

This document defines the standard data schemas used by both backend and frontend components.

## 1. Input Format
- **Job Description Text**: Raw text of the target job posting.
- **Student Skills**: List of strings representing skills the student already possesses.

## 2. Extracted Skill Schema
Each missing skill object contains:
- `name` (string): Standardized name of the technical skill.
- `category` (string): Category (e.g., "Machine Learning", "DevOps", "Programming").
- `priority` (string): Priority level ("High", "Medium", or "Low").
- `why_it_matters` (string): Explanation of why this skill is needed for the role.

## 3. Final Output Schema
The full application response includes:
- `known_skills` (list of strings): Matching skills between user and job.
- `missing_skills` (list of objects): Skills required/preferred by the job that the user lacks.
  - Contains: `name`, `category`, `priority`, `why_it_matters`.
- `roadmap_steps` (list of objects): Recommended learning path.
  - Contains: `step` (number), `action` (string), `target_skill` (string).
- `resources` (list of objects): Suggested learning materials.
  - Contains: `skill` (string), `resource_name` (string), `url` (string).
 
## 4. Target Roles Format
Target roles are stored in `roles.json` as a list of role objects. JSON was chosen over CSV because it loads directly with Python's built-in `json` module and supports a list of skills per role without awkward cell parsing.

- `role` (string): Standard job title that matches job postings (e.g., "Machine Learning Engineer").
- `skills` (list of objects): Skills the role needs.
  - `name` (string): Lowercase, trimmed skill name, no duplicates within a role.
  - `requirement_type` (string): Either `"Required"` or `"Preferred"`.

### Sample
```json
[
  {
    "role": "Machine Learning Engineer",
    "skills": [
      {"name": "python", "requirement_type": "Required"},
      {"name": "git", "requirement_type": "Required"},
      {"name": "sql", "requirement_type": "Required"},
      {"name": "pytorch", "requirement_type": "Required"},
      {"name": "docker", "requirement_type": "Preferred"}
    ]
  }
]
```

### Loading
```python
import json

with open("roles.json") as f:
    roles = json.load(f)
```
