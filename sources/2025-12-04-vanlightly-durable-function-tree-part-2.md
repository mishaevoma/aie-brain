---
type: source
title: "The Durable Function Tree - Part 2"
author: "Jack Vanlightly"
publisher: jack-vanlightly.com
url: https://jack-vanlightly.com/blog/2025/12/4/the-durable-function-tree-part-2
published: 2025-12-04
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# The Durable Function Tree - Part 2

**In one line:** You do not need durable execution to get reliable multi-step work. What it adds is the workflow as one visible, governable thing, at the price of coupling and the determinism rule, so keep it to the critical path.

## What it says

- A *reliable trigger* is whatever guarantees that work is run again if it fails: a queue message, or a function that a durable execution engine stands behind. Each reliable trigger draws a *responsibility boundary* around the work downstream of it.
- In a tree of durable functions every function has its own trigger, so a failure retries one branch only. Completed siblings keep their results and parents stay suspended. Errors travel up when a branch runs out of retries. Cancellations travel down.
- Event-driven choreography draws the boundaries differently. Every consumer owns its own recovery, and the producer has no responsibility for what consumers do. Without stored step results, everything inside one consumer must be safe to repeat as a whole, which is harder than making single side effects idempotent.
- Large function trees are an anti-pattern. The more a workflow encloses, the more reasons it has to change, the more often it must be versioned, and the more room there is for non-determinism.
- Both styles produce reliable workflows. Choreography gives decoupling and fragmented visibility. Orchestration gives an explicit workflow, observable as a whole, with policies and timeouts that span steps. It also brings coupling and what the author calls the curse of determinism, which stays as long as progress comes from re-executing with stored results.
- If the only goal is procedural code that survives failures, the author calls the case for durable execution weak.
- The recommended hybrid: orchestrate the direct edges (the steps that must all succeed for the business goal) and emit events for everything else, instead of having workflows call workflows.

## What to do with it

- Put under durable orchestration only the steps that must succeed together. Announce the result as an event and let other systems react.
- Keep each durable workflow small enough to version and to reason about.
- Choose durable execution for visibility and control over a process, not only for crash recovery.

## Terms

- **Reliable trigger** — whatever ensures a unit of work is run again if it fails.
- **Responsibility boundary** — the work a reliable trigger answers for.

## Caveats

- A conceptual essay about business workflows in general, from December 2025. Agents are not discussed.
- Part 1 covers the mechanics (durable promises, suspension) and is not summarised here.
