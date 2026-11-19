# Scorecard

Run `2026-11-19-local-codex`: codex with gpt-6-astra at medium effort, review started by the skill path, wiki revision `fe44a47 2026-11-19`, 2026-11-19. Written by `evals/score.py`; grades are in [`runs/2026-11-19-local-codex/scores.csv`](runs/2026-11-19-local-codex/scores.csv) and each review beside it.

## Stop rule

| Condition | Result | Met |
|---|---|---|
| Planted issues found on the seeded fixture, at least 4 of 5 | 4 of 5 (S1 S2 S3 S5) | yes |
| Invented findings on the no-AI control | 0 | yes |
| Every product fixture has a finding scoring 2 on all six dimensions | 5 of 5 | yes |
| No finding scores 0 | 0 at 0 | yes |
| One-paste smoke check on other agents | 0 run on none | **no** |
| Links to the wiki resolve | 0 broken | yes |
| Sources older than 365 days are labelled as older | 0 unlabelled | yes |
| Review arrives in about 3 minutes | slowest 90s | yes |
| Fixture tree left untouched | 7 of 7 | yes |

`python3 tools/lint.py` has to be clean as well; CI runs it on every push.

## Reviews

| Fixture | Agent, model | Seconds to review | Findings | Best | At 0 | Sources cited | Older, labelled | Tree |
|---|---|---|---|---|---|---|---|---|
| [01-llm-wrapper](runs/2026-11-19-local-codex/01-llm-wrapper/review.md) | codex, gpt-6-astra | 50.9 | 1 | 2 | 0 | 1 | 0 of 0 | untouched |
| [02-rag-app](runs/2026-11-19-local-codex/02-rag-app/review.md) | codex, gpt-6-astra | 81.3 | 4 | 2 | 0 | 3 | 2 of 2 | untouched |
| [03-tool-agent](runs/2026-11-19-local-codex/03-tool-agent/review.md) | codex, gpt-6-astra | 89.8 | 4 | 2 | 0 | 4 | 1 of 1 | untouched |
| [04-multi-agent](runs/2026-11-19-local-codex/04-multi-agent/review.md) | codex, gpt-6-astra | 75.9 | 3 | 2 | 0 | 4 | 0 of 0 | untouched |
| [05-plain-app](runs/2026-11-19-local-codex/05-plain-app/review.md) | codex, gpt-6-astra | 57.9 | 2 | 2 | 0 | 2 | 1 of 1 | untouched |
| [06-no-ai-control](runs/2026-11-19-local-codex/06-no-ai-control/review.md) | codex, gpt-6-astra | 34.7 | 0 | - | 0 | 2 | 0 of 0 | untouched |
| [07-seeded](runs/2026-11-19-local-codex/07-seeded/review.md) | codex, gpt-6-astra | 82.4 | 5 | 2 | 0 | 5 | 0 of 0 | untouched |

## Findings

| Fixture | Finding | Matches | Specific | Correct | Cited | Fresh | Verifiable | Actionable | Score | Note |
|---|---|---|---|---|---|---|---|---|---|---|
| 01-llm-wrapper | Turn the three examples into a regression eval | W1 W2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Its mutation check reproduces: all three tests pass with the prompt replaced. The unbounded diff (W3) is not raised. |
| 02-rag-app | Keep the superseded policy out of the index | R4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Labels the 2025 source as older and gives the reason. Diagnostic reproduces. |
| 02-rag-app | Turn the 16 asked questions into an evaluation | R1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 02-rag-app | Chunk on sections and keep their context | R3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Labels the 2024 source as older and says it is an experiment here. |
| 02-rag-app | Add keyword search for form identifiers | R2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Its demonstration is contrived and says so. |
| 03-tool-agent | Make refunds and emails safe to retry | T1 T2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Describes its probe and names the tests to add; the probe itself is not pasted. |
| 03-tool-agent | Enforce refund and recipient rules in code | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 | True and unplanned. Reproduces: 4 unchecked writes. |
| 03-tool-agent | Report failed and incomplete runs accurately | T3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 03-tool-agent | Test the customer outcome through the agent loop | T4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 04-multi-agent | Bound the review loop and reject false approvals | M3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Command reproduces: NOT APPROVED returns notes. |
| 04-multi-agent | Give writer and critic the pull requests and simplify the chain | M1 M2 M4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Command reproduces: 4 [True True False False]. |
| 04-multi-agent | Turn the export incident into an evaluation | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 05-plain-app | Reject categories outside the four before saving | P2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Reproduces: stored other and filtered lists show 0. |
| 05-plain-app | Measure tagging on the 40 labelled tickets | P1 P3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 07-seeded | Bind recipient and order access in code | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 | True and unplanned. |
| 07-seeded | Make sending idempotent | S2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  |
| 07-seeded | Make the test gate run behaviour and measure reply quality | S1 S3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Ran make test and reported OK (skipped=4). |
| 07-seeded | Return usable failures and keep processing | - | 2 | 2 | 2 | 2 | 2 | 2 | 2 | True and unplanned. |
| 07-seeded | Bound customer history | S5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | The prompt in code (S4) appears only as a clause about prompt changes. |

## Other agents

No smoke check recorded for this run.

## Mechanical checks that did not pass

None.
