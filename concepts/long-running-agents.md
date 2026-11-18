---
type: concept
title: "Long-running agents"
updated: 2026-11-17
reviewed: 2026-11-17
status: evolving
---

# Long-running agents

**Definition:** Agents that work for hours, or across many context windows, on one task. They need state kept outside the model and a way to tell real progress from the appearance of it.

## Why it matters

Given only a high-level goal, a strong model fails in predictable ways over long runs. It builds too much at once and runs out of context mid-feature, or a later session sees partial progress and declares the job done. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md) It also rates its own mediocre work highly, and passing tests can pass for finished work. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md) · [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)

## What to do

**Keep state on disk**

- Start with a setup session (the *initializer agent*) that writes a run script, a progress log, an initial commit and a machine-readable feature list with everything marked failing. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)
- Let the agent change only the pass/fail field of each item, never rewrite the list or the tests. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)
- Open every session the same way: read the log and history, pick the next failing item, start the app, run a smoke test. Close it with a commit and a progress note. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)
- Write for a reader with no memory: progress files, terse console output with detail in logs, one-line errors that can be searched. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)

**Check the real thing**

- Count something as done only after exercising it like a user, through the running interface. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)
- Use a separate, sceptical evaluator, agree on "done" with it before each stage (a *sprint contract*), and calibrate it with scored examples. Out of the box a model is a lenient tester. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- Give agents a fast test mode. They have no sense of time, so offer a sampled run (1% or 10% of the tests) for quick feedback. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)

**Build for interruption**

- Keep the full session log outside both the context window and the sandbox, make the loop stateless, and resume from the log. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Make waiting an ordinary state. Give the model outputs for asking a person and for declaring itself done, store the run as one serialisable thread of events, and resume it from a webhook when the answer comes. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Treat sandboxes as disposable. A dead container should be a tool error the agent can work around. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Cap loops: stop after repeated identical calls, and hand back to a person after a set number of denials. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)

## Scaffolding expires

- Per-feature chunking and context resets (a fresh agent plus a written handoff) were needed for one model generation, partly to counter context anxiety, and were removed for the next. A planner and a final evaluation pass stayed. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md) · [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- An evaluator earns its cost only when the task is beyond what the model does reliably alone. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- So at each model release, remove one piece of scaffolding at a time and keep what still carries load. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)

## What it costs

- One game-maker build took 20 minutes and $9 solo and did not work at its core. With a planner, generator and evaluator it took 6 hours and $200 and did. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- A compiler built by 16 parallel agents took nearly 2,000 sessions and just under $20,000. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)

## Related

[Harness](harness.md) · [Verification](verification.md) · [Context engineering](context-engineering.md) · [Multi-agent systems](multi-agent-systems.md) · [Running agents in production](production-operations.md)
