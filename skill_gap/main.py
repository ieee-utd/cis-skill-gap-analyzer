"""Entry point for the Skill Gap Analyzer.

Run it from the repo folder with:

    python -m skill_gap.main

Right now it only prints a welcome message, so make sure you are able to see that.
"""


def welcome_message():
    """Return the message the app prints when it starts."""
    return "AI Skill Gap Analyzer is set up and running."


def main():
    """Print the welcome message. Later this will run the full analysis."""
    print(welcome_message())


if __name__ == "__main__":
    main()