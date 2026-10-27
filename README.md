# AI-Powered Skill Gap Analyzer

An IEEE UTD CIS project that compares a student's skills to a job posting and builds a personalized learning roadmap using an LLM.

## Description

Job postings list a lot of languages, frameworks, tools, and preferred qualifications. Students often do not know which ones matter most or what to learn first.

This app takes a job or internship description and the student's current skills. It uses a Large Language Model (LLM) to pull out the skills the job asks for and sorts them by category and by required or preferred. Then it compares them to what the student already knows. The output shows which skills the student has, which skills are missing, why the important ones matter, what order to learn them in, and resources for each one.

How the app works

    Job description + current skills
      - Extract job requirements (LLM)
      - Organize and categorize skills
      - Compare with the student's skills
      - Identify missing skills
      - Prioritize missing skills
      - Generate a learning roadmap
      - Recommend learning resources

## Getting started

Start with the [setup guide](docs/getting-started.md).

## Targets

- Fall Show and Tell demo
- LLM budget of about $50 to $75 for the semester. Keep test runs small

## Repo layout

- `skill_gap/` the app code. Each step of the flow gets its own file
- `prompts/` the text prompts we send to the LLM
- `examples/job_descriptions/` real job postings we test with
- `examples/outputs/` saved results from running the app
- `tests/` automated tests that run on every pull request
- `docs/` setup guide and design notes

## Team

- Shradha Gupta, CIS Society Director
- Aparna Balaji, Project Supervisor

## Workflow

Every change starts from an issue, goes on its own branch, and gets merged through a pull request after one review. See [CONTRIBUTING.md](CONTRIBUTING.md).
