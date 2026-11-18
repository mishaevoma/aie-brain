---
type: source
title: "How to think about durable execution"
author: "Alexander Belanger"
publisher: Hatchet
url: https://hatchet.run/blog/durable-execution
published: 2025-12-11
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# How to think about durable execution

**In one line:** A task that is easily made idempotent and commits in one database transaction needs only a queue; durable execution earns its overhead when a job chains stateful steps, and it brings a determinism rule and recovers less than its reputation suggests.

## What it says

- **When a queue is enough.** A task queue over a message broker is likely all you need when the task is easily idempotent and updates application state in a single database transaction. Easily idempotent means stateless, or idempotent after a minimal change. Example: process an uploaded file through an external API, then mark it PROCESSED unless it already is; redelivery after a crash or visibility timeout leaves state consistent.
- **When it is not.** The author's example provisions hundreds of AWS resources over up to about an hour, polling and updating a record for each. Three further triggers: one part needs a different machine; a write to an external store cannot easily be made idempotent (a mutating KV cache holding an agent's context); or the job spans many microservices with separate stores.
- **What durable execution adds.** It persists a workflow's intermediate state in a separate store. Workflows are retried until they complete, on a new machine if needed, and skip whatever the event log shows as done. Each subtask is dispatched exactly once under an idempotency key, typically the workflow instance id plus the subtask's index, though a failed subtask may itself be retried.
- **The price is determinism.** It bites three ways: iterating over a collection whose order changes (a Go map); a network or database call in the workflow function itself, where only calls to the engine are allowed; and a code change that reorders steps already in a run's history.
- **What it does not fix.** Progress inside a subtask is not saved; the subtask restarts or raises an error, unless it is itself a durable workflow. A fatal subtask error is logged and thrown again on every retry. It recovers program state, not buggy application state. For transient failures the first fix is to have fewer of them. It should replace at most part of a queueing system, and persisting intermediate state costs developer effort and money.

## What to do with it

- Default to a queue. Move a job to durable execution when it has several stateful steps that cannot cheaply be made idempotent.
- Keep side effects in subtasks, iterate only over stable orderings, and treat reordering steps as a breaking change for in-flight runs.
- Make a long subtask a workflow of its own if losing its progress would hurt.

## Terms

- **Easily idempotent** — stateless, or made idempotent with a minimal change.

## Caveats

- From December 2025, by the co-founder of a durable execution vendor; it ends with a pitch and gives no costs or measurements.
- It covers the workflow-and-subtask form only. For inline steps see [Durable Coroutines](2026-11-03-restate-durable-coroutines.md).
