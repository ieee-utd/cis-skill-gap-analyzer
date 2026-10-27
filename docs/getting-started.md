# Getting started

Follow these steps in order. If something does not work, check Common problems at the bottom, then ask in #ai-skill-gap-analyzer.

## 1. Install the tools

You need Python 3.12 or newer, Git, and VS Code. The onboarding document has install steps for Mac and Windows.

Check that they work:

    python --version
    git --version

On Mac, use `python3` instead of `python` in every command on this page.

## 2. Clone the repo

Open a terminal in the folder where you keep your projects and run:

    git clone https://github.com/ieee-utd/cis-skill-gap-analyzer.git
    cd cis-skill-gap-analyzer

Then open the folder in VS Code:

    code .

## 3. Make a virtual environment

A virtual environment keeps this project's libraries separate from everything else on your computer. You only make it once.

    python -m venv .venv

Turn it on every time you open a new terminal to work on the project.

Mac:

    source .venv/bin/activate

Windows:

    .venv\Scripts\activate

You will see `(.venv)` at the start of your terminal line when it is on.

## 4. Install the libraries

    pip install -r requirements.txt

## 5. Set up your API key

Make a copy of `.env.example` and name the copy `.env`. Put your real key in `.env`. Git ignores this file, so your key never gets uploaded.

Never put a real key in `.env.example` or anywhere else in the code.

## 6. Run the app and the tests

    python -m skill_gap.main
    python -m pytest

You should see the welcome message, then `1 passed`.

## 7. Make your first change

    git checkout main
    git pull
    git checkout -b 3-add-my-name

Make your change, then:

    git add .
    git commit -m "docs: add my name to the team"
    git push -u origin 3-add-my-name

Go to the repo on GitHub and click Compare and pull request. Fill out the template and write `Part of #3`. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full workflow.

## Common problems

- **`python` is not recognized (Windows).** Python was installed without the "Add python.exe to PATH" box checked. Run the installer again, choose Modify, and check that box.
- **Push to main was rejected.** That is on purpose. Make a branch and open a pull request instead.
- **`ModuleNotFoundError`.** Your virtual environment is probably off. Turn it on (step 3), then run `pip install -r requirements.txt` again.
- **Tests fail with an import error.** Run `python -m pytest` from the main repo folder, not plain `pytest`.
