# release-crew

A crew of four agents that writes the weekly release notes from the pull requests merged that week.

| Agent | Job |
|---|---|
| Planner | Decides the steps for this week's notes |
| Researcher | Reads every merged pull request and summarises it |
| Writer | Turns the research into release notes for customers |
| Critic | Reviews the notes and sends them back until they are good |

## Run

```sh
pip install anthropic
python3 crew.py prs.json > RELEASE_NOTES.md
python3 -m unittest -v
```

`prs.json` is exported by CI every Friday: title, labels and description of each merged pull request.

## Notes from running it

- Takes four to nine minutes and costs about ten times what the old single-prompt script did.
- Twice it never finished and had to be killed by hand.
- Last month the notes announced a "new export API". The pull request had removed the old export endpoint.
