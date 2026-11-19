# Scorecard

Run `2026-11-19-published-codex`: codex with gpt-6-astra at medium effort, review started by the published URL, wiki revision `9b70bc0 2026-11-19`, 2026-11-19. Written by `evals/score.py`; grades are in [`runs/2026-11-19-published-codex/scores.csv`](runs/2026-11-19-published-codex/scores.csv) and each review beside it.

## Stop rule

| Condition | Result | Met |
|---|---|---|
| Planted issues found on the seeded fixture, at least 4 of 5 | 4 of 5 (S1 S2 S3 S5) | yes |
| Invented findings on the no-AI control | 0 | yes |
| Every product fixture has a finding scoring 2 on all six dimensions | 5 of 5 | yes |
| No finding scores 0 | 0 at 0 | yes |
| One-paste smoke check on other agents | 2 run on Claude Code (subagent); not run: Cursor, Web-only agent | **no** |
| Links to the wiki resolve | 0 broken | yes |
| Sources older than 365 days are labelled as older | 0 unlabelled | yes |
| Review arrives in about 3 minutes | slowest 107s | yes |
| Fixture tree left untouched | 7 of 7 | yes |

`python3 tools/lint.py` has to be clean as well; CI runs it on every push.

## Reviews

| Fixture | Agent, model | Seconds to review | Findings | Best | At 0 | Sources cited | Older, labelled | Tree |
|---|---|---|---|---|---|---|---|---|
| [01-llm-wrapper](runs/2026-11-19-published-codex/01-llm-wrapper/review.md) | codex, gpt-6-astra | 74.8 | 2 | 2 | 0 | 2 | 1 of 1 | untouched |
| [02-rag-app](runs/2026-11-19-published-codex/02-rag-app/review.md) | codex, gpt-6-astra | 79.8 | 4 | 2 | 0 | 3 | 2 of 2 | untouched |
| [03-tool-agent](runs/2026-11-19-published-codex/03-tool-agent/review.md) | codex, gpt-6-astra | 100.8 | 4 | 2 | 0 | 3 | 1 of 1 | untouched |
| [04-multi-agent](runs/2026-11-19-published-codex/04-multi-agent/review.md) | codex, gpt-6-astra | 87.9 | 4 | 2 | 0 | 4 | 1 of 1 | untouched |
| [05-plain-app](runs/2026-11-19-published-codex/05-plain-app/review.md) | codex, gpt-6-astra | 60.5 | 2 | 2 | 0 | 2 | 1 of 1 | untouched |
| [06-no-ai-control](runs/2026-11-19-published-codex/06-no-ai-control/review.md) | codex, gpt-6-astra | 44.8 | 0 | - | 0 | 2 | 0 of 0 | untouched |
| [07-seeded](runs/2026-11-19-published-codex/07-seeded/review.md) | codex, gpt-6-astra | 107.2 | 6 | 2 | 0 | 5 | 1 of 1 | untouched |

## Findings

| Fixture | Finding | Matches | Specific | Correct | Cited | Fresh | Verifiable | Actionable | Score | Note |
|---|---|---|---|---|---|---|---|---|---|---|
| 01-llm-wrapper | Turn the examples into a repeatable quality check | W1 W2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Tests pass with the real diff discarded. Also finds a reference message that states facts the diff lacks. |
| 01-llm-wrapper | Validate the message before printing it | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 | True and unplanned. Pasted command reproduces. Labels the 2025 source as older and its use here as inference. The unbounded diff (W3) is not raised. |
| 02-rag-app | Exclude archived policies from current answers | R4 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | Probe output is given but the probe is not pasted. |
| 02-rag-app | Turn the asked questions into an evaluation | R1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 02-rag-app | Keep policy statements whole and with their source | R3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Pasted command reproduces the split at 240 EU / R in London. |
| 02-rag-app | Add keyword search for form identifiers | R2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Says the reported miss was not reproduced with live embeddings. |
| 03-tool-agent | Prevent duplicate payments after a timeout | T1 T2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Pasted script reproduces: retry: error 3. |
| 03-tool-agent | Enforce refund policy across the request | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 | True and unplanned. Reproduces: 30000 cents with no approval. |
| 03-tool-agent | Bind data access and email delivery to the customer | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 | True and unplanned. Labels the 2025 source as older with the reason. |
| 03-tool-agent | Distinguish unfinished runs from completion | T3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Reproduces: status done after the step limit. The source note says what the review says it does. |
| 04-multi-agent | Make the approval gate reject negative verdicts | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 | True and unplanned. Pasted command reproduces. |
| 04-multi-agent | Bound the revision loop | M3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Pasted command reproduces: stops only on IndexError from the fake. |
| 04-multi-agent | Give writer and critic the pull requests and simplify the chain | M1 M2 M4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Labels the 2024 source as older with the reason and adds a 16-day-old one. |
| 04-multi-agent | Test release-note correctness | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 05-plain-app | Stop unexpected replies hiding tickets from category lists | P2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Reproduction output shown. Evidence age sits in the Why part. |
| 05-plain-app | Measure tagging on the labelled tickets | P1 P3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 07-seeded | Bind tool permissions to the current customer | - | 2 | 2 | 2 | 2 | 1 | 2 | 1 | True and unplanned. Probe output given but the probe is not pasted. |
| 07-seeded | Make sending idempotent | S2 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | Probe output given but the probe is not pasted. |
| 07-seeded | Return delivery outcomes and isolate failures | - | 2 | 2 | 2 | 2 | 1 | 2 | 1 | True and unplanned. Probe not pasted. |
| 07-seeded | Make the mandatory test command run behaviour | S1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Ran make test: 5 tests and 4 skipped. |
| 07-seeded | Evaluate the outgoing message before changing prompts | S3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Names the complaint-driven review in the README. Does not name the prompt kept in agent.py (S4). |
| 07-seeded | Bound customer history | S5 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | Probe not pasted. Labels the 2025 source as older with the reason. |

## Other agents

| Agent, model | Fixture | Started without questions | Seconds to first finding | Note |
|---|---|---|---|---|
| Claude Code (subagent), claude-sonnet-5-5 | 07-seeded | yes | 55 | WebFetch returned a summary and the agent fetched raw text with curl as the skill says. Found S1 S2 S3 S4 S5. Tree untouched. Not a clean paste: started in another folder and told the fixture's path. Review in runs/2026-11-19-published-claude-code. |
| Claude Code (subagent), claude-sonnet-5-5 | 06-no-ai-control | yes | 34 | Says there is no AI feature and nothing to upgrade and offers one question. Tree untouched. Same caveat. |
| Cursor,  |  | not run |  | No command-line agent on this machine. Needs a person to paste the line. |
| Web-only agent,  |  | not run |  | Needs a person's go-ahead to send the prompt in a chat product. |

## Mechanical checks that did not pass

- 05-plain-app: part missing: evidence age
