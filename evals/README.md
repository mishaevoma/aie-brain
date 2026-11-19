# Review evals

The wiki promises this: your coding agent reviews your app against a dated, cited knowledge base and shows what to upgrade. This folder tests that promise on eight small projects and keeps the result.

| Path | Holds |
|---|---|
| `fixtures/` | Eight small projects: six AI apps, one with no AI, one with planted issues |
| [`expected.md`](expected.md) | The answer key: upgrades a maintainer would accept, per fixture, with IDs |
| `run.py` | Runs the review on the fixtures with a headless agent |
| `score.py` | Checks what a machine can check and writes the scorecard |
| [`scorecard.md`](scorecard.md) | The latest full run |
| `runs/` | One folder per run: each review, a trace of the agent's steps, timings, grades |
| `demo/` | Builds the GIF in the README: three upgrades named by primitive (harness, tools, memory), with evidence from real reviews |

## Run it

You need a coding agent's command-line tool that is logged in on this machine. `run.py` drives Codex (`codex exec`) or Claude Code (`claude -p`). Python is standard library only.

```sh
python3 evals/run.py --label full                        # all fixtures, Codex, the published URL
python3 evals/score.py evals/runs/<date>-full            # mechanical checks
# grade the findings in evals/runs/<date>-full/scores.csv (see "Grade" below)
python3 evals/score.py evals/runs/<date>-full --write    # writes evals/scorecard.md
```

`run.py` copies each fixture to a fresh folder outside this repository and commits it there, so the agent sees an ordinary project with no wiki above it. The agent gets the line a person would paste:

```text
Review this project using
https://mishaevoma.github.io/aie-brain/review.md
```

Options that matter:

- `--via url` (default) tests what is published. A change to the skill or the wiki is not in it until `main` is deployed.
- `--via skill` tests this checkout before you publish. The agent reads a clone of the last commit with `evals/` removed, so commit first, and it cannot open the answer key.
- `--via installed` copies the skill into the fixture as `npx skills add` would, and asks "Use brain-consult to review this project."
- `--agent claude --model sonnet` runs Claude Code. `--model` and `--effort` set the Codex model and reasoning effort.
- `--no-network` keeps the Codex sandbox offline, which is what happens when nobody approves a network command.
- `--fixtures 03 07` runs a subset. Use it to rerun what a fix touched.

Each review folder gets `review.md` (what the person would read), `trace.txt` (every step with its arrival time), and `meta.json` (agent, model, prompt, wiki and fixture revisions, seconds to the review, and whether the fixture's tree was left untouched, by `git status` including ignored files).

## Grade

Read each review against the fixture and [`expected.md`](expected.md). Add one row per finding to `scores.csv` in the run folder:

```csv
fixture,finding,ids,specific,correct,cited,fresh,verifiable,actionable,note
03-tool-agent,Refund retried without a key,T1 T2,2,2,2,2,2,2,ran the check
```

`ids` holds the IDs from `expected.md` that the finding matches. Grade each dimension 0, 1 or 2.

| Dimension | 2 | 1 | 0 |
|---|---|---|---|
| Specific | Names the file and line or section, and the smallest change | Names the file or area, not the place or the change | No location in the project |
| Correct | True of the code, and what the cited page says | True, with an overstated or wrong detail | False about the code, or not what the source says |
| Cited | Wiki page, dated source note and original publication, all resolving | One of the three missing | No citation, or one that does not support the advice |
| Fresh | Gives the source's date or age, which is under 12 months, or labels it older with the reason it still holds | Gives the date, without labelling an older source | No date, or older evidence presented as current |
| Verifiable | A command or exact test with the result to expect, and whether it was run | A check with no expected result, or not runnable as written | No check |
| Actionable | States effort and impact, and the maintainer could start from the chat | Clear change, effort or impact missing | Advice with no action |

A finding scores 2 only when every dimension is 2, and 0 when any dimension is 0. A finding at 0 is never removed from the table. Fix the wiki or the instructions and run again.

Before grading correctness, run the finding's check in a copy of the fixture, and open the page it cites. Advice that the reviewer labels as its own judgment is graded on what it claims. It can be correct, and it scores 1 on "cited" and "fresh", because no source stands behind it.

One-paste checks on other agents go in `smoke.csv` in the same folder:

```csv
agent,model,fixture,started_without_questions,first_finding_seconds,note
Cursor,its default,07-seeded,yes,95,found S1 S2 S5
```

A permission prompt to fetch the URL is not a question. A question about setup, paths or what to review is.

A smoke check that could not be a clean paste says so in its note. Use `not run` in `started_without_questions` for an agent that is still owed, so the scorecard keeps showing it.

## When to stop

One full run has to show all of these. `score.py --write` works them out and prints them at the top of the scorecard.

- At least 4 of the 5 planted issues on `07-seeded` are found, with the right file and the right problem.
- No finding on `06-no-ai-control`.
- Every product fixture, which is every fixture but the control and the seeded one, has a finding that scores 2.
- No finding scores 0.
- The one-paste smoke check passes on Claude Code, Codex, Cursor and one web-only agent.
- `python3 tools/lint.py` is clean, every wiki link in a review resolves, and every source older than 365 days is labelled as older where it is cited. `python3 tools/lint.py --ages` shows the same ages per page.
- The review arrives in about three minutes and leaves the fixture's tree untouched.

## When a review misses

Give each miss one cause, and fix only that.

| Cause | Fix |
|---|---|
| The wiki does not cover it | Ingest a source with `brain-ingest`, or add to a concept page or playbook |
| The instructions do not ask for it | Edit `.agents/skills/brain-consult/references/project-review.md` or `SKILL.md` |
| The agent could not load the skill or the wiki | Fix the published files or the fallback, and record which agent and tool failed |
| The source is stale or weakly cited | Refresh the source, or label the page |

Never name a fixture, its files or a planted string in the skill or the wiki. After a fix, rerun the fixtures it touched, then the full set. Keep `python3 tools/lint.py --sync --log "edit | …"` and `python3 site/test_review_publication.py` green.

## Add a fixture

Keep it under about ten files, runnable with the standard library, with no secrets and no comment that gives a planted issue away. Add its upgrades to `expected.md` with IDs, and say what is already right, so a review that invents a problem can be caught.
