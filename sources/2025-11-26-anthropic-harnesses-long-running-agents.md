---
type: source
title: "Effective harnesses for long-running agents"
author: "Justin Young"
publisher: Anthropic
url: https://www.anthropic.com/research/effective-harnesses-for-long-running-agents
published: 2025-11-26
ingested: 2026-11-17
kind: article
read: full
concepts: [harness, long-running-agents, verification]
---

# Effective harnesses for long-running agents

**In one line:** An agent that works across many context windows needs a handoff written to disk: a feature list, a progress log, git history and a startup script. Each fresh session reads these to rebuild state, does one feature, and leaves the repo clean.

## What it says

- Each session starts with no memory of earlier ones. Compaction in the Claude Agent SDK helps but is not enough.
- Given only a high-level prompt ("build a clone of claude.ai"), Opus 4.5 failed two ways: it built too much at once and ran out of context mid-feature, leaving an undocumented mess; or a later session saw progress and declared the job done.
- The fix is two prompts on one harness (same system prompt and tools):
  - An **initializer agent** runs first and writes `init.sh` (starts the dev server), a `claude-progress.txt` log, an initial git commit, and a feature list expanded from the prompt (over 200 features for the clone), all marked failing.
  - A **coding agent** runs every later session, does one feature, and ends with a descriptive commit and progress note.
- The feature list is JSON; the coding agent may only change each feature's `passes` field. The model was less prone to rewrite JSON than Markdown, and the prompt forbids editing tests in strong terms.
- Each session starts the same way: run `pwd`, read the git log and progress file, pick the highest-priority failing feature, start the server via `init.sh`, and run a basic end-to-end check before new work.
- Claude tended to mark features done after unit tests or `curl` calls. Prompting it to test in the browser like a user, via Puppeteer MCP, caught far more bugs. It cannot see browser-native alert modals that way, so those features stayed buggier.
- Open question: would specialized testing, QA or cleanup agents beat one general coding agent?

## What to do with it

- Give the first session its own setup prompt: run script, progress log, git, machine-readable feature list.
- Keep task status in JSON the agent may only flip, never rewrite.
- One feature per session; open with an orientation routine and smoke test, close with a commit and progress note.
- Count a feature as passing only after end-to-end checks through the real UI.

## Terms

- **Initializer agent / coding agent** — the same harness with different first prompts, one for setup and one for incremental work.
- **Clean state** — code fit to merge to main: no major bugs, orderly, documented.

## Caveats

- Opus 4.5 and one web-app demo only. Anthropic sells Claude and the Agent SDK.
- The page names the feature file inconsistently (`feature_list.json` and `tests.json`).
- Partly superseded by [the March 2026 harness post](2026-03-24-anthropic-harness-design-long-running-apps.md), which adds a planner and separate evaluator, then drops per-feature chunking for Opus 4.6.
