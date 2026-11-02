# AI Skill Gap Analyzer Data Format Specification

This document defines the standard data schemas used by both backend and frontend components.

## 1. Input Format
- **Job Description Text**: Raw text of the target job posting.
- **Student Skills**: List of strings representing skills the student already possesses.

## 2. Extracted Skill Schema
Each skill extracted from the job description contains:
- `name` (string): Standardized name of the technical skill.
- `category` (string): Category (e.g., "Programming", "Framework", "Database", "DevOps").
- `importance` (string): "High", "Medium", or "Low".
- `requirement_type` (string): "Required" or "Preferred".

## 3. Final Output Schema
The full application response includes:
- `known_skills` (list of strings): Matching skills between user and job.
- `missing_skills` (list of objects): Skills required/preferred by the job that the user lacks.
- `roadmap_steps` (list of objects): Recommended learning path.
- `resources` (list of objects): Suggested learning materials.