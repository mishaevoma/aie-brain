---
type: source
title: "Durable Execution"
author: "Pydantic"
publisher: Pydantic Docs
url: https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/
published: 2026-11-17
ingested: 2026-11-17
kind: docs
read: full
concepts: [agent-platforms, durable-execution]
---

# Durable Execution

**In one line:** Under a durable engine, a Pydantic AI agent's run loop is replayed workflow code and its model, MCP and most tool calls are recorded units, so the engine's size caps and replay rules constrain the agent's design.

## What it says

- **Pages covered.** Overview plus the Temporal, DBOS, Prefect and Restate sub-pages.
- **Durability is not storage.** Saving and resuming a run, or forking it from an earlier step, needs no engine: `StepPersistence` snapshots each settled step into storage you pick, like a checkpointer. An engine adds crash survival mid-step, retries and journaled calls.
- **Mapping.** Only `agent.run()` called inside the engine's workflow, flow or handler is durable.
  - Temporal: the run loop is workflow code; model requests, tool calls and MCP communication are activities, named from the agent `name` and toolset `id`s.
  - DBOS: model requests and MCP communication are steps; function tools stay in workflow code unless decorated with `@DBOS.step`.
  - Prefect: the same three are tasks, cached by input.
  - Restate: the agent runs in an HTTP handler; `RestateAgent` journals model responses, and tools take durable steps through `restate_context()`.
  - An async tool marked `durable=False` runs inside workflow code, so must be deterministic.
- **Temporal limits.** Each recorded payload (activity arguments and results) is capped at 2MB by default, roughly 1.5MB for binary data. An oversized result raises `UserError`; an oversized input, such as message history, fails the workflow task and retries indefinitely. Return references, or use external storage (public preview), which offloads payloads above 256 KiB by default. The history cap is around 50,000 events or 50MB; a `continue_as_new` hook starts a fresh execution carrying the conversation when Temporal suggests it, checked before each model request.
- **DBOS sizes.** Guidance only: inputs and outputs under ~2 MB; Postgres and SQLite accept up to 1 GB per field.
- **Streaming.** On Temporal, DBOS and Prefect, in-workflow streaming is buffered: each part arrives whole after its model request. Live events come through an `event_stream_handler`, which can repeat on retry. Temporal's Workflow Streams let outside clients subscribe and resume by offset, adding roughly 100ms per roundtrip.
- **Changing a deployed agent.** Renaming the agent or a toolset, moving a tool into or out of its durable unit, or adding a workspace alters the recorded sequence, so in-flight runs fail or diverge on replay. Remedies: let them finish, Temporal worker versioning or a patch, a new DBOS application version. On Prefect a changed cache key re-executes the task.
- **Parallel tools on DBOS.** Tools run in parallel, yet steps must start in a deterministic order. A tool making two durable calls in sequence can interleave with its siblings differently on recovery, failing or swapping results. Set `parallel_execution_mode='sequential'` or use child workflows.

## What to do with it

- Decide first: engine or step persistence.
- Freeze agent names and toolset ids before production.
- Keep payloads small and tools idempotent.
- Set the provider client's `max_retries` to 0; let the engine retry.

## Terms

- **Durable unit** — a step, task or activity whose result is recorded and reused on replay.

## Caveats

- Undated documentation, read on 17 November 2026; the date above is the day it was read.
- Vendor documentation without measurements. The other engine pages were not read.
