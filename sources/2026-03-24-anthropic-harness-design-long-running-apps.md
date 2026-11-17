---
type: source
title: "Harness design for long-running application development"
author: "Prithvi Rajasekaran"
publisher: Anthropic
url: https://www.anthropic.com/research/harness-design-long-running-apps
published: 2026-03-24
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, harness, long-running-agents, multi-agent-systems, verification]
---

# Harness design for long-running application development

**In one line:** Separating the agent that builds from a skeptical agent that grades the running product, with explicit criteria, raises quality on multi-hour builds. Every part of the harness is a bet on what the model cannot yet do, so re-test each part when a new model ships.

## What it says

- It builds on the [initializer/coding-agent harness](2025-11-26-anthropic-harnesses-long-running-agents.md) and borrows the GAN idea of a **generator** and an **evaluator**.
- Two failure modes:
  - **Context anxiety:** a model rushes to finish as it nears its believed context limit. Sonnet 4.5 had it badly, so the harness used **context resets** (a fresh agent plus a written handoff) rather than compaction alone. Opus 4.5 largely lost the behavior, so resets were dropped in favour of the Agent SDK's automatic compaction.
  - **Self-praise:** agents rate their own mediocre work highly. A separate evaluator is easier to tune toward strictness than a self-critical generator.
- Frontend design: both agents get four criteria, **design quality, originality, craft, functionality**, with the first two weighted higher to escape safe defaults and "AI slop". The evaluator views the live page via Playwright MCP, is calibrated with few-shot scored examples, and runs 5–15 rounds (up to four hours). Even round one beat an unprompted baseline, and criterion wording visibly steered style.
- Full-stack harness (Opus 4.5): a **planner** expands a 1–4 sentence prompt into an ambitious spec without fixing low-level implementation. A **generator** builds in sprints (React, Vite, FastAPI, SQLite/PostgreSQL, git). An **evaluator** exercises UI, API and database and fails any sprint below hard thresholds. Each sprint starts with a **sprint contract** defining "done". Handoffs go through files.
- Retro game maker: solo took 20 min and $9, and its core play didn't work. The full harness took 6 hr and $200, planned 16 features across ten sprints and produced a working play mode, rough edges aside.
- Out of the box Claude was a lenient QA agent, spotting problems and then approving them anyway. Tuning took several rounds.
- For Opus 4.6, sprints were removed. The planner stayed (without it the generator under-scoped) and the evaluator became one final pass. A browser DAW took about 4 hours and $124.70 over three build/QA rounds, with the builder coherent for over two hours. QA still caught features that only looked done.
- An evaluator is worth its cost only when the task is beyond what the model does reliably on its own.

## What to do with it

- Use a separate, skeptical evaluator that tests the running artifact, not just the code.
- Write subjective quality as weighted criteria, and calibrate the judge with scored examples.
- Agree on "done" between builder and grader before work starts.
- With each model release, remove scaffolding one piece at a time and keep only what still bears load. Read traces to see where the model really fails.

## Terms

- **Context anxiety** — wrapping up early as the context limit nears.
- **Sprint contract** — pre-agreed completion criteria between generator and evaluator.

## Caveats

- The page doesn't say outright which model ran the DAW build; it implies Opus 4.6.
- Single-author demos, not controlled benchmarks. Anthropic sells the models and the Agent SDK.
- Supersedes parts of the [Nov 2025 harness post](2025-11-26-anthropic-harnesses-long-running-agents.md): per-feature chunking and resets proved model-dependent.
