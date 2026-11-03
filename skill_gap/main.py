"""Entry point for the Skill Gap Analyzer.

Run it from the repo folder with:

    python -m skill_gap.main

Right now it sends a test prompt to the LLM and prints the response.
"""

from skill_gap.llm_client import ask_llm


def welcome_message():
    """Return the message the app prints when it starts."""
    return "AI Skill Gap Analyzer is set up and running."


def main():
    """Print the welcome message, then send a test prompt to the LLM."""
    print(welcome_message())
    print(ask_llm("In one sentence, what is a skill gap?"))


if __name__ == "__main__":
    main()
