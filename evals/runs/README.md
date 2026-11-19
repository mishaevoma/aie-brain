# Runs

One folder per run of `evals/run.py`. Local paths are replaced with `<work>` (the folder of fixture copies) and `<wiki>`.

| Run | Agent | Started by | What it showed |
|---|---|---|---|
| `2026-11-19-baseline-codex` | Codex, gpt-6-astra, medium | published URL, wiki `49d0c3c` | The review before this work. 3 of 5 planted issues found, no finding with all five parts, control clean. Codex's web tool could not open the site and fell back to `curl`. |
| `2026-11-19-baseline-codex-offline` | same | published URL, sandbox offline | With no network approval nothing loads. Codex says so and gives an unsourced code review. |
| `2026-11-19-baseline-codex-offline-github` | same | the skill's page on GitHub, sandbox offline | The skill page opens, the procedure and the wiki do not. Codex says the comparison is incomplete. |
| `2026-11-19-local-codex` | same | this checkout's skill, wiki `fe44a47` | The rewritten procedure and the upgrade playbook, before publishing. 4 of 5 planted issues, every product fixture has a finding at 2, control clean. |
| `2026-11-19-local-codex-installed` | same | the skill installed in the fixture | Same three leading upgrades as the URL-style run on `03-tool-agent`, and no install offer, as intended. |
| `2026-11-19-published-codex` | same | published URL, wiki `9b70bc0` | **The run behind the scorecard.** 4 of 5 planted issues, every product fixture has a finding at 2, no finding at 0, control clean, slowest review 107 s, every tree untouched. |
| `2026-11-19-published-claude-code` | Claude Code subagent, claude-sonnet-5-5 | published URL, wiki `9b70bc0` | Smoke check on two fixtures. WebFetch returned a summary of the skill, and the agent fetched raw text with `curl` as the skill says. All five planted issues found, control clean. Not a clean paste: the subagent started in another folder and was told the fixture's path, so there is no `meta.json` here. |

## Seen, not yet fixed

- On Claude Code the older sources were labelled as older, but without the reason: the agent did not read the `status` and `reviewed:` lines at the top of the wiki page. Saying where those lines are in the procedure is the next thing to try.
- The prompt kept in code with no version or check (S4) is found by Claude Code and missed by Codex in three runs, where it shows up only as a clause inside the eval finding.
- Codex's own web tool cannot open the site. The review works because Codex falls back to `curl`, which needs network approval.
