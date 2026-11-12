# Experiments

Scripts for comparing skill extraction approaches (AB#17). Results are in [extraction_results.md](extraction_results.md).

## Setup

Run these commands from inside this folder, because the script finds `skills.txt` and the sample files by their relative paths.

```bash
cd experiments
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

You have to run `python -m spacy download en_core_web_sm` first, or the spaCy test fails with "Can't find model 'en_core_web_sm'".

For the LLM test, put `GEMINI_API_KEY=...` in a `.env` file (see `../.env.example`). Without a key, the script skips the LLM test.

## Running

```bash
# Default: sample_resume.txt checked against answer_key.txt
python extraction_comparison.py

# Any other resume or job description, with its own answer key
python extraction_comparison.py --input sample_resume_2.txt --key answer_key_2.txt
python extraction_comparison.py --input ../examples/job_descriptions/sample_job.txt --key answer_key_sample_job.txt

# Skip the LLM test
python extraction_comparison.py --no-llm

# Use a different Gemini model (for example, when the default one is returning 503 busy errors)
LLM_MODEL=gemini-3.5-flash python extraction_comparison.py
```

## Files

| File | What it is |
|---|---|
| `skills.txt` | Master list of 40 skills |
| `sample_resume.txt` / `answer_key.txt` | First test resume. The spaCy synonym list was built from this one. |
| `sample_resume_2.txt` / `answer_key_2.txt` | Second resume, held out. It was not used to build the synonym list. |
| `answer_key_sample_job.txt` | Answer key for `../examples/job_descriptions/sample_job.txt` |
