# AB#17 – Extraction approach comparison

Tested all three approaches on the same sample resume  against a 40-skill list. The answer key has 30 skills a human would pick out.

| Method | Correct (out of 30) | Missed | Wrong/extra | Time | Cost | Setup |
|---|---|---|---|---|---|---|
| Keyword matching | 19 | 11 | 0 | around 0.00s | Free | Very low |
| spaCy PhraseMatcher + synonyms | 30 | 0 | 0 | 1s | Free | Medium (needs synonym list) |
| LLM API (Gemini) | ran(503 error busy server)| | | | around some cents per resume | API key + billing |

## What keyword matching missed
Different wordings: "ML", "NLP", "JS", "Postgres", "scikit learn", "Amazon Web Services", "REST endpoints", "deep-learning", "computer-vision", "scrum", "analyze".

## Notes
 spaCy only caught these because we added a synonym list. On a new resume with wording that isn't in the list, it could miss things, so the list has to be maintained. The LLM handles new wordings without a synonym list, but costs money per call, needs an API key, and could return a skill that isn't there.

## Suggestion
Use spaCy + synonym list as the main extractor because it is free and fast and it returns a list of strings. 
