---
type: source
title: "Durable Coroutines for TypeScript: Fault-tolerant Agents with millisecond overhead"
author: "Igal Shilman, Stephan Ewen, Giselle van Dongen"
publisher: Restate
url: https://restate.dev/blog/durable_coroutines
published: 2026-11-03
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Durable Coroutines for TypeScript: Fault-tolerant Agents with millisecond overhead

**In one line:** A durable step appended inline to a journal costs a few milliseconds where one dispatched to a worker costs tens, so an agent can record every model call, guardrail and tool call; Restate's coroutines add replayable concurrency to the inline model.

## What it says

- **Dispatched step.** In the workflow-and-activity model each persisted step is an activity scheduled on a worker. In systems like Temporal the workflow task yields to the orchestrator, a worker runs the activity, and the workflow task executes again with the result.
- **Inline step.** In the durable-function model the handler keeps running in one process; each step (`ctx.run`, a timer, a signal, a call) is streamed to the Restate Server and acknowledged. Outside recovery a run is one continuous execution, so steps share local variables, cached files and authenticated connections.
- **Figures.** Restate reports that one durable step inside a coroutine adds P50=2.5ms and P99=9ms in production deployments, at more than 10,000 durable actions per second, on a 3-AZ, synchronously replicated setup on GCP. It contrasts this with the 50-100 milliseconds it says workflow products often incur. The only source for that range is a footnote: Temporal's documentation is cited for a scheduling overhead of about 50 ms for each regular Activity on Temporal Cloud, and a Temporal blog post for Cloud having lower latency than self-hosting.
- A second footnote: Temporal's local activities are persisted only when the workflow yields, so the first of two results is not saved before the second starts.
- **Why agents.** Harnesses record small steps (chunks of model output; intent, guardrail and result chunks per tool call), which strengthens recovery after a failure.
- Larger units (a conversation turn, a long-running tool) still belong in separate durable functions with queueing and flow control.
- **Deterministic concurrency.** Code is written as generators: `run` is a step, `spawn` starts a concurrent task, `select` and `all` combine them. Under async/await the event loop picks the interleaving; a generator stays paused at `yield*` until the SDK's scheduler resumes it. The scheduler advances every coroutine until all wait on a Restate action, then calls `RestatePromise.race` on the pending actions, which journals the winning completion. Replay reproduces that order. One coroutine runs at a time; their steps' I/O overlaps.
- **In production.** Said to run at various companies; the one named is Replit Agent.

## What to do with it

- Ask where a runtime executes a step, on a dispatched worker or inline against a log: that sets how finely you can record.
- Record inside the loop when a step costs milliseconds; dispatch heavy, queued or rate-limited work separately.
- Journal the completion order of parallel branches; do not leave it to the event loop.

## Terms

- **Durable coroutine** — a concurrent routine inside one durable function, with journalled steps and replayed interleaving.

## Caveats

- The figures are the vendor's: one sentence, no payloads, hardware or method. They are added overhead, not the model or tool call. Nothing in the post supports the 100 ms end of the comparison.
- TypeScript SDK only; code must use generators, not async/await.
- Bears on the claim in [Building LangGraph](2025-09-04-langchain-building-langgraph.md) that durable execution engines add latency between steps.
