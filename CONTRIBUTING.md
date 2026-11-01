# Contributing

## 1. Pick an issue

- Pick an issue from the **To Do** column on **Azure Boards**
- Assign yourself and drag it to **Doing** so nobody else starts the same issue
- Note the work item number on the card (for example, `#7`)
- If there is no issue for what you want to do, tell Aparna, then make one

## 2. Make a branch

Never work directly on main. Name the branch `feature/<short-issue-name>`.

    git checkout main
    git pull
    git checkout -b feature/pdf-text-extraction

## 3. Commit small and often

Start each commit message with the type of change ([Conventional Commits](https://www.conventionalcommits.org)).

- `feat:` new code that adds something
- `fix:` fixes a bug
- `test:` adds or changes tests
- `docs:` README, guides, comments
- `chore:` setup and cleanup

## 4. Keep API keys out of the repo

- Your API key goes in your own `.env` file. Git ignores that file
- Never paste a key into code, a prompt file, an issue, or Discord
- Tests must not call the real LLM. Use a fake response instead, so the build check stays free and fast
- If you ever commit a key by accident, tell Aparna right away so the key can be deleted and replaced

## 5. Open a pull request

- Push your branch (`git push -u origin feature/short-issue-name`) and open a pull request into main on GitHub
- Write `Fixes AB#7` (replace `7` with your Azure Boards issue number) in the PR description so the Azure ticket automatically moves to **Done** when it merges
- Fill out the testing checklist

## 6. Review

- Check that the code does what the issue says and that it was tested
- Leave comments as questions or suggestions
- The author fixes things and pushes again on the same branch
- Aparna merges once it is approved

## Using AI tools

AI tools are okay to use. You are still responsible for the code. Before opening a pull request, make sure you tested it and can explain every part. Keep pull requests small and add screenshots when they help.
