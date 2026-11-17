---
type: source
title: "Designing AI-resistant technical evaluations"
author: "Tristan Hume"
publisher: Anthropic
url: https://www.anthropic.com/research/AI-resistant-technical-evaluations
published: 2026-01-21
ingested: 2026-11-17
kind: article
read: full
concepts: [eval-validity]
---

# Designing AI-resistant technical evaluations

**In one line:** each new Claude model broke Anthropic's performance-engineering take-home, and the version that still separates humans from the model works by being out of distribution rather than by resembling real work.

## What it says

- Since early 2024 candidates have optimised code for a Python simulator of a TPU-like accelerator (scratchpad memory, VLIW, SIMD, multicore) using a Perfetto trace. Over 1,000 took it; it helped hire most of the team, including people straight from undergrad. AI use was allowed.
- Goals: resemble real work, give many independent chances to show skill, need no niche knowledge, be fun.
- By May 2025, over 50% of candidates would have done better delegating fully to Claude Code with Claude 3.7 Sonnet. A pre-release Claude Opus 4 beat almost all humans in the 4-hour limit.
- Version 2 started where Opus 4 struggled, dropped multicore and cut the limit to 2 hours. A pre-release Claude Opus 4.5 passed the threshold in under an hour and, once told the achievable cycle count, matched the best 2-hour human.
- Rejected options: banning AI (hard to enforce, unrealistic) and requiring humans to clearly beat Claude Code (they spend much of the time reading).
- A new realistic problem (register transposition with bank conflicts) failed because it is well documented; Opus 4.5 found an unexpected rewrite and "ultrathink" mode solved the rest.
- Version 3 uses Zachtronics-style puzzles: a tiny constrained instruction set, scored on minimal instruction count, with no debugging tools supplied, so judging how much tooling to build is part of the signal. Early scores track past work; the author misses the realism.
- The original is now an open GitHub challenge. Cycle counts: Claude Opus 4 2164; Opus 4.5 casual session 1790, 2 hours in harness 1579, 11.5 hours 1487, improved harness 1363; Claude Sonnet 4.5 1548. Anyone who gets below 1487 is invited to email recruiting. The fastest human solution ever submitted substantially beats Claude's best.

## What to do with it

- Re-run current models on any fixed assessment at each release; assume discriminating tests expire.
- Prefer novel, out-of-distribution problems; well-documented topics are in training data.
- Favour many independent sub-problems and a wide score range over single-insight puzzles.
- If AI is allowed, measure what the human adds on top of it.

## Terms

- **AI-resistant evaluation** — an assessment where delegating to a model is not the winning strategy.

## Caveats

- January 2026; models and cycle counts will be superseded, and the author is unsure how long version 3 will last.
- Anthropic writing about its own hiring and products; candidate-quality claims are unverified.
- About hiring tests, not product evals, though the saturation lesson matches the evals guide (2026-01-09).
