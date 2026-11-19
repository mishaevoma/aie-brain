# Runs

One folder per run of `evals/run.py`. Local paths are replaced with `<work>` (the folder of fixture copies) and `<wiki>`.

| Run | Agent | Started by | What it showed |
|---|---|---|---|
| `2026-11-19-baseline-codex` | Codex, gpt-6-astra, medium | published URL, wiki `49d0c3c` | The review before this work. 3 of 5 planted issues found, no finding with all five parts, control clean. Codex's web tool could not open the site and fell back to `curl`. |
| `2026-11-19-baseline-codex-offline` | same | published URL, sandbox offline | With no network approval nothing loads. Codex says so and gives an unsourced code review. |
| `2026-11-19-baseline-codex-offline-github` | same | the skill's page on GitHub, sandbox offline | The skill page opens, the procedure and the wiki do not. Codex says the comparison is incomplete. |
| `2026-11-19-local-codex` | same | this checkout's skill, wiki `fe44a47` | The rewritten procedure and the upgrade playbook, before publishing. 4 of 5 planted issues, every product fixture has a finding at 2, control clean. |
| `2026-11-19-local-codex-installed` | same | the skill installed in the fixture | Same three leading upgrades as the URL-style run on `03-tool-agent`, and no install offer, as intended. |
