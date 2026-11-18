---
type: source
title: "Agent checkpointing is far from production-grade resiliency"
author: "Giselle van Dongen"
publisher: Restate
url: https://restate.dev/blog/why-checkpointing-is-not-production-grade-durable-execution
published: 2026-06-15
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Agent checkpointing is far from production-grade resiliency

**In one line:** Saving an agent's state at step boundaries recovers finished work and little else; noticing failures, durable retries, one writer per session, free waits, version pinning and availability are a distributed-systems job that belongs under the agent SDK, not inside it.

## What it says

- What agent frameworks call durable is usually checkpointing: write a snapshot of the state to a database at boundaries, and have the caller restart from the newest one. LangGraph (per node), Google ADK (event persistence) and Mastra (per step) are named. The author's estimate is that this leaves 80% of the hard work with the developer.
- Eight things a checkpoint does not give:
  1. **Recovery to the failing step.** A checkpoint returns to a boundary. A tool that makes three calls and dies after the second runs all three again, because nothing recorded the first two. Parallel subagents that had finished may redo their work. Journaling every model call, tool call, sleep and remote call lets a re-run skip completed steps and continue at the exact one that did not finish.
  2. **Someone to notice.** A library dies with its process. Without a supervisor you need a queue or a retrying client, stable run ids, and code to redispatch.
  3. **Retries that survive.** An attempt counter in a variable, or a backoff written as a sleep, dies with the process. Retry policy and state belong in the durable layer.
  4. **One guarantee for the whole workflow.** Most agents sit inside a deterministic workflow with non-agentic steps (write to a database, send an email) that need the same durability.
  5. **A single writer.** A double click, or a zombie process that was presumed dead, gives two agents writing one session: lost updates, corrupt state, duplicate side effects. Preventing it takes locking and fencing.
  6. **Waits that are durable and free.** The wake-up must survive restarts, timers must remember the time remaining, a wait must hold no resources, and the code that resumes must be the code that suspended.
  7. **Safe upgrades.** Checkpoints carry no application version. Example: a risk-score tool changes its scale from 0–10 to 0–100 and a run resumed on new code misreads an old result, silently. In-flight runs should be pinned to the immutable deployment they started on while new traffic goes to the new version.
  8. **A runtime that does not die.** One Postgres instance in one region is a single point of failure.
- Conclusion: none of this is specific to agents. Durability is distributed-systems work and an agent SDK is an application library, so the SDK should run on top of a durable execution runtime and stay swappable.

## What to do with it

- Check a runtime against the eight items, not against the word "durable".
- Record at the level of each side effect, not each loop iteration, when repeating a side effect would hurt.
- Enforce one active run per session, and reject writes from superseded attempts.
- Pin every in-flight run to the code and tool versions it started with.

## Terms

- **Journal** — a durable record of each completed step, replayed to skip finished work.
- **Fencing** — rejecting writes from an attempt that has been superseded.
- **Version pinning** — resuming a run only on the deployment it started on.

## Caveats

- Written by a vendor of a durable execution runtime, and it ends with a pitch for that product. The 80% figure is rhetorical.
- It disputes the checkpoint design described in [Building LangGraph](2025-09-04-langchain-building-langgraph.md), which had argued that replay engines were a poor fit for agents.
