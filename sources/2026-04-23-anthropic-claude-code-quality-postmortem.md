---
type: source
title: "An update on recent Claude Code quality reports"
author: "Anthropic"
publisher: Anthropic
url: https://www.anthropic.com/research/april-23-postmortem
published: 2026-04-23
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, eval-validity, evals, harness, production-operations]
---

# An update on recent Claude Code quality reports

**In one line:** three harness-level changes (lower default effort, a caching bug that discarded reasoning, a terse-output system prompt) made Claude Code feel worse in March–April 2026 while the model and API were unchanged.

## What it says

- The causes sat in Claude Code, the Claude Agent SDK and Claude Cowork, not the API. Each hit a different traffic slice on a different schedule, so together they looked like diffuse decline, and internal evals did not reproduce it at first. All fixed by April 20 (v2.1.116); usage limits were reset.
- **Default effort (Mar 4 – Apr 7):** dropped from `high` to `medium` to stop long waits that made the UI seem frozen; evals showed slightly lower intelligence for much less latency. Users preferred smarter defaults, and Anthropic now calls it the wrong tradeoff. Defaults are now `xhigh` for Opus 4.7, `high` elsewhere.
- **Dropped reasoning (Mar 26 – Apr 10, fixed in v2.1.101):** old thinking was meant to be cleared once after an hour idle (`clear_thinking_20251015`, `keep:1`). A bug cleared it every turn thereafter, so Claude grew forgetful and repetitive and picked odd tools; resulting cache misses likely drained usage limits. It passed review, unit and end-to-end tests and dogfooding, masked by unrelated internal changes. In back-testing, Code Review with Opus 4.7 and full repo context caught it; Opus 4.6 did not.
- **Verbosity prompt (Apr 16 – Apr 20):** to rein in the wordier Opus 4.7, a system prompt line capped text between tool calls at 25 words and final answers at 100 unless more detail was needed. The evals run showed no regression; broader ablations later found a 3% drop for Opus 4.6 and 4.7.
- The first two affected Sonnet 4.6 and Opus 4.6; the third also Opus 4.7.
- Commitments: staff use the public build; better Code Review shipped to customers; broad per-model evals and line-by-line ablations for every prompt change; audit tooling for prompts; model-specific changes gated to their model; soak periods and gradual rollout for anything trading off intelligence.

## What to do with it

- Gate harness changes (defaults, context pruning, system prompts) with the same evals as a model swap.
- Use a broad per-model suite for prompt edits; narrow suites miss few-percent drops.
- Let users opt down in reasoning effort rather than lowering the default for latency.
- Test long and resumed sessions whenever you prune context or reasoning.
- Dogfood the exact shipped build and roll out risky changes gradually.

## Terms

- **effort** — the Messages API parameter for how much the model reasons.

## Caveats

- April 2026; versions, defaults and models will move on. Vendor self-report; the 3% figure is from its own evals; no named author.
- Unlike the 2025-09-17 postmortem, causes were in the harness, not serving infrastructure.
