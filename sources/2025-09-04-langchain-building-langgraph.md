---
type: source
title: "Building LangGraph: Designing an Agent Runtime from first principles"
author: "Nuno Campos"
publisher: LangChain
url: https://www.langchain.com/blog/building-langgraph
published: 2025-09-04
ingested: 2026-11-17
kind: article
read: full
concepts: [agents-and-workflows, durable-execution, long-running-agents]
---

# Building LangGraph: Designing an Agent Runtime from first principles

**In one line:** An agent runtime exists to pay for three facts about LLM work (it is slow, it fails midway, it is open-ended), and LangGraph's answer is to cut the agent into discrete steps so that state can be saved, resumed and inspected between them.

## What it says

- Three differences from ordinary backends drive the design: latency measured in seconds to hours, retries that are expensive because a run that dies at minute 9 of 10 should not start over, and non-deterministic behaviour that needs checkpoints, approvals and testing.
- These give six features a production agent needs: parallelization and streaming (real and perceived latency), a task queue and checkpointing (fewer and cheaper retries), human-in-the-loop and tracing (non-determinism). Low added latency is the overall constraint. An agent that needs few of the six may need no framework at all.
- Existing systems were ruled out. DAG schedulers cannot loop. Durable execution engines such as Temporal came closest, but were judged to lack streaming, to add latency between steps, and to slow down as a run's history grows.
- The central idea is the *structured agent*: split the work into discrete steps. One big `while` loop is simpler, but its in-memory execution state cannot be saved in a form that another machine can resume later, so it gives up checkpointing and human-in-the-loop.
- Execution follows the BSP/Pregel model. Nodes subscribe to named, versioned channels. Each step runs the triggered nodes in parallel on isolated copies of the state and applies their writes in a fixed order, so the output never depends on timing.
- A checkpoint stores serialized channel values (MsgPack, optionally encrypted) and their versions. A run can resume on any machine, any time later, with no live process kept.
- Waiting for a person while the process stays up scales neither in time nor in volume. A real interruption (stop, save, resume later) is the only approach that holds for waits of days or for many paused agents.
- Resuming loads only the latest checkpoint. Its cost is constant in the length of the history and in the number of threads, because nothing is replayed.
- The task queue was out of scope for a library and became a separate hosted product, LangGraph Platform.

## What to do with it

- List which of the six features your agent needs before choosing a runtime.
- Give the loop step boundaries where state is saved. That is what later makes pause, resume, approval and rewinding possible.
- Implement long waits as stop-and-resume from a checkpoint, never as a sleeping process.
- Put a queue between the request and the run, so that a retry does not depend on the caller still being connected.

## Terms

- **Structured agent** — an agent expressed as discrete steps with saved state between them.
- **Checkpoint** — the saved state at a step boundary, from which any machine can resume.
- **Thread** — one independent invocation with its own checkpoints.

## Caveats

- Written by the framework's maintainers. The comparison with durable execution engines is theirs and dates from September 2025; those engines have added agent features since.
- The scaling claims are complexity arguments, not measurements.
