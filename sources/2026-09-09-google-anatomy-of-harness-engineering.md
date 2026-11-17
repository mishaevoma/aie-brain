---
type: source
title: "The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents"
author: "Taylor Mullen, Christian Gunderman"
publisher: "Google Developers Blog"
url: https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/
published: 2026-09-09
ingested: 2026-11-17
kind: article
read: full
concepts: [compounding, evals, harness]
---

# The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents

**In one line:** pair end-to-end benchmarks with small, fast behavioral evals that check what the agent does along the way, so you can tell why a harness change helped or hurt.

## What it says

- Teams run end-to-end benchmarks such as Terminal-Bench and DeepSWE, see a few points of movement, and cannot explain it. These are the standard for comparing models but costly to investigate.
- A pass/fail total is a report card: it can't show whether the agent got overconfident on vague prompts, skipped tests, or made up a CLI flag.
- **Behavioral evals** test discrete observable behaviours, like integration tests for the harness. Examples: asks a clarifying question when the prompt is underspecified; runs the local validator after editing a build file; links canonical repo locations in docs.
- Don't build evals on day one. Start with instinct and dogfooding; evals pay off once the agent can work on its own codebase. Then they keep progress going and catch regressions.
- The goal is not a 2% gain but confidence that a prompt tweak, tool-schema change or model upgrade didn't make the agent worse overall.
- Assert on intermediate steps (tool calls, file changes), not exact final strings. The pytest example with Google's **Antigravity SDK** asks for Mountain View weather and fails unless `SEARCH_WEB` was called.
- Keep checks fast, deterministic and local; the sample command targets a suite under 5 seconds.
- With a rich suite you can automate prompt engineering: an LLM edits its own system prompt until a failing eval passes, with the rest of the suite acting as a CI-style guard.
- Recipe: pick one failure mode; use strict single-turn checks where one right move exists and outcome checks such as **LLM-as-a-judge** for complex tasks; run batches and track pass rates over time instead of blocking PRs on single noisy runs.
- Behavioral evals complement end-to-end benchmarks; they don't replace them.

## What to do with it

- Dogfood first; add evals once the agent works on its own repo.
- Write one eval per observed failure mode, asserting on tool calls or file changes.
- Track aggregate pass rates; don't gate merges on one run.
- Rerun the suite on every prompt, tool-schema or model change.

## Terms

- **harness engineering** — building and tuning the system around the model; "harness" itself is not defined.
- **behavioral eval** — a test of one observable agent behaviour, working like an integration test for the harness.
- **evaluation harness** — the eval setup, to be treated as ordinary software with unit and integration tests.

## Caveats

- No data on eval effectiveness; "under 5 seconds" is a code comment, not a measurement.
- The example uses the authors' employer's own SDK.
- For explicit harness definitions see Loams (2026-10-18) and Theo Browne (2026-10-22).
