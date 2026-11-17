---
type: source
title: "How we built Claude Code auto mode"
author: "John Hughes"
publisher: "Anthropic"
url: https://www.anthropic.com/research/claude-code-auto-mode
published: 2026-03-25
ingested: 2026-11-17
kind: article
read: full
concepts: [human-judgment, long-running-agents, multi-agent-systems, sandboxing-and-permissions, tool-design]
---

# How we built Claude Code auto mode

**In one line:** hand routine approvals to a two-stage classifier that sees only the user's words and the proposed action, and publish its real miss rate.

## What it says

- Users accept 93% of manual prompts. The alternatives were a sandbox (safe, but needs setup and breaks on network or host access) or `--dangerously-skip-permissions` (no protection). Auto mode sits between.
- Motivating incidents: deleting remote branches after misreading an instruction, uploading a GitHub auth token to a compute cluster, attempting production database migrations.
- Threats: overeager behaviour, honest mistakes, prompt injection, and misalignment (not seen in practice). Tuning targets the first two.
- Three tiers. Read-only tools and user allow rules pass, but rules granting arbitrary code execution (blanket shell, wildcarded interpreters, package-manager run) are dropped. In-project edits pass, since git can undo them. Everything else (shell, web fetch, external tools, subagent spawns, out-of-project files) goes to a **transcript classifier** on Sonnet 4.6.
- The classifier is **reasoning-blind**: it sees user messages and tool-call payloads only. The agent cannot argue its case, and injected tool output never reaches the judge. Cost: it cannot tell if an identifier was looked up or invented.
- Stage 1 is a single-token yes/no tuned to block; flagged actions go to Stage 2, the same prompt asking for reasoning, almost all cached.
- Policy: a fixed template (only what the user explicitly authorized counts) plus editable environment, block rules (more than twenty, in four groups) and allow exceptions. `claude auto-mode defaults` lists them.
- A server-side **prompt-injection probe** warns the agent about suspicious tool output. Subagents are checked at hand-off (can deny) and on return (warns).
- Blocks come back as tool results asking for a safer path. After 3 consecutive or 20 total denials it escalates to the human; `claude -p` exits instead.

| | Real traffic FPR (n=10,000) | Real overeager FNR (n=52) | Synthetic exfil FNR (n=1,000) |
|---|---|---|---|
| Stage 1 | 8.5% | 6.6% | 1.8% |
| Stage 1→2 | 0.4% | 17% | 5.7% |

- Most misses: danger recognized, consent wrongly assumed. Far better than skipping permissions; possibly worse than careful human review on high-stakes infrastructure.

## What to do with it

- Hide the agent's prose and tool outputs from any action judge; judge against the user's words.
- Use a cheap block-leaning filter, escalating only flagged cases to a cached reasoning pass.
- Feed denials back as recoverable, with a hard cap that returns control to a human.
- Strip broad allow rules when auto-approving.
- Measure misses on real incidents, not only synthetic sets.

## Terms

- **auto mode** — Claude Code mode where classifiers stand in for the human approver.
- **reasoning-blind** — the judge never sees agent text or tool results.
- **overeager behaviour** — acting beyond what the user authorized while trying to help.

## Caveats

- Vendor on its own product; the overeager set is small (n=52); numbers are for March 2026.
- "How we contain Claude" (2026-05-25) calls auto mode a layer inside a sandbox, not a substitute; Loams (2026-10-18) notes every vendor says a gate model is not the boundary.
