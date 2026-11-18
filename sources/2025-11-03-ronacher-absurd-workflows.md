---
type: source
title: "Absurd Workflows: Durable Execution With Just Postgres"
author: "Armin Ronacher"
publisher: lucumr.pocoo.org
url: https://lucumr.pocoo.org/2025/11/3/absurd-workflows/
published: 2025-11-03
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Absurd Workflows: Durable Execution With Just Postgres

**In one line:** Durable execution is a queue plus a store of step results, and for an agent both fit in one Postgres database with no separate service.

## What it says

- Durable execution means long-lived functions that keep their state and do not repeat finished work when a process crashes, a machine restarts or the network fails. The author reduces it to two parts: a queue, and a state store that remembers each completed step.
- Postgres does both. `SELECT ... FOR UPDATE SKIP LOCKED` makes a good queue, and the same database holds the state.
- Absurd is the author's implementation: one SQL file that moves the logic into the database, with thin SDKs on top. No extension and no extra service.
- The model: a *task* is put on a queue and picked up by a worker. A task is split into *steps*. Each step's result is stored as a *checkpoint*. A task that fails or suspends runs again, and completed steps are loaded from storage instead of being executed again. Only tasks are retried, never single steps.
- Tasks can sleep (the example sleeps for 7 days) or wait for a named event with a timeout. Events are cached, so one emitted before the wait begins is not lost.
- An agent is a workflow whose shape is not known in advance: one step repeated until the model stops calling tools. The engine numbers repeated steps automatically. Each checkpoint stores only the messages that iteration produced, not the whole history.
- The author's position: the existing durable execution systems are good but heavy, many problems do not need that scale, and a Postgres-only design suits software that other people must host themselves.

## What to do with it

- Before adopting a durable execution service, check whether the database you already run can hold the queue and the step results.
- Make one loop iteration the unit you checkpoint, and store only what it added.
- Use sleep and wait-for-event primitives for anything that waits on time or on a person.

## Terms

- **Task / step / checkpoint** — a queued unit of work, one recorded piece of it, and the stored result of that piece.

## Caveats

- Announces the author's own small library, in November 2025, with no production figures.
- Says nothing about versioning tasks that are in flight, or about side effects that run twice. In the example one step covers a model call and its tool calls, so a crash midway repeats those tool calls on retry. That last point is this brain's reading of the code shown.
