"""Entry point for the Skill Gap Analyzer.

Run it from the repo folder with:

    python -m skill_gap.main

To check that your Gemini API key works, add the --test-llm flag:

    python -m skill_gap.main --test-llm
"""

import argparse

from skill_gap.llm_client import ask_llm


def welcome_message():
    """Return the message the app prints when it starts."""
    return "AI Skill Gap Analyzer is set up and running."


def main():
    """Print the welcome message. Only call the LLM if --test-llm is given."""
    parser = argparse.ArgumentParser(description="AI Skill Gap Analyzer")
    parser.add_argument(
        "--test-llm",
        action="store_true",
        help="send a test prompt to Gemini (needs GEMINI_API_KEY in .env)",
    )
    args = parser.parse_args()

    print(welcome_message())
    if args.test_llm:
        print(ask_llm("In one sentence, what is a skill gap?"))


if __name__ == "__main__":
    main()
