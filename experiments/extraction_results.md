# AB#17 – Extraction approach comparison

Tested all three approaches against a 40-skill list (`skills.txt`) on three inputs:

1. **Resume 1** (`sample_resume.txt`): the spaCy synonym list was built from this resume, so spaCy scoring 30/30 here doesn't prove much.
2. **Resume 2** (`sample_resume_2.txt`): a held-out resume that was *not* used to build the synonym list. It uses common wordings such as "K8s", "ReactJS", "NodeJS", "Mongo", "Ubuntu" and "statistical analysis", and it includes one trap ("networking events", where Networking isn't a real skill).
3. **Job description** (`examples/job_descriptions/sample_job.txt`): the only posting in that folder so far.

The answer keys list the skills a human would pick out. LLM runs used `gemini-3.5-flash`, because the default `gemini-3.8-flash` was still returning 503 "high demand" errors after 5 retries.

## Results

### Resume 1 (synonym list built from it), 30 skills

| Method | Correct | Missed | Wrong/extra | Time |
|---|---|---|---|---|
| Keyword matching | 19 | 11 | 0 | ~0.00s |
| spaCy + synonyms | 30 | 0 | 0 | ~1s |
| LLM (Gemini 3.5 Flash) | 30 | 0 | 1 (Data Visualization) | ~13s |

### Resume 2 (held out), 22 skills

| Method | Correct | Missed | Wrong/extra | Time |
|---|---|---|---|---|
| Keyword matching | 12 | 10 | 1 (Networking) | ~0.00s |
| spaCy + synonyms | 12 | 10 | 1 (Networking) | ~1s |
| LLM (Gemini 3.5 Flash) | **22** | 0 | 1 (Deep Learning) | ~37s* |

### Job description, 7 skills

| Method | Correct | Missed | Wrong/extra | Time |
|---|---|---|---|---|
| Keyword matching | 7 | 0 | 0 | ~0.00s |
| spaCy + synonyms | 7 | 0 | 0 | ~1s |
| LLM (Gemini 3.5 Flash) | 7 | 0 | 0 | ~11s |

\*LLM times include waiting on Gemini retries when the server was busy, so they vary a lot between runs.

| Method | Cost | Setup |
|---|---|---|
| Keyword matching | Free | Very low |
| spaCy + synonyms | Free | Medium (synonym list has to be maintained) |
| LLM (Gemini) | A few cents per resume | API key + billing, and it can be unavailable (503) |

## What we learned

- **On the held-out resume, spaCy did no better than plain keyword matching (12/22 each).** None of that resume's wordings were in the synonym list, so the synonyms added nothing. It missed: K8s → Kubernetes, ReactJS → React, NodeJS → Node.js, Mongo → MongoDB, RESTful API → REST APIs, Ubuntu → Linux, "statistical analysis" → Data Analysis, charts/dashboards → Data Visualization, text classification → NLP, and fine-tuning a model → Machine Learning.
- **Both keyword matching and spaCy fell for "networking events"** and reported Networking. The LLM didn't.
- **The LLM found every skill on all three inputs.** Its two extras are arguable rather than clearly wrong (Tableau dashboards → Data Visualization; fine-tuning BERT → Deep Learning).
- **The job description was easy for all three methods.** Postings tend to name skills directly ("Python", "Docker", "PyTorch"), while resumes use more varied wording. We have only one posting so far, so we should retest when more are added to `examples/job_descriptions/`.
- The 30/30 spaCy score on resume 1 came from building the synonym list on that resume, so it doesn't predict how spaCy will do on new resumes.

## Suggestion

**Use the LLM (Gemini) as the main extractor for resumes, with spaCy + synonyms as the fallback** for when the API is down, busy or out of quota.

- The LLM is the only method that held up on a resume it hadn't seen (22/22 compared with 12/22). A synonym list will always lag behind the ways people actually write their resumes.
- We still check the LLM output against `skills.txt` (the script already keeps only names from the master list), so it can't make up skills outside the list.
- Because we saw 503 errors from Gemini, the app needs retries plus the spaCy fallback rather than relying on the LLM alone.
- For job descriptions, spaCy or keyword matching may be enough on its own, since postings name skills directly. We should confirm this once we have more postings.
- If cost or the API key setup is a problem, spaCy is still the best free option. But whenever it misses a wording, we would need to add that wording to the synonym list.
