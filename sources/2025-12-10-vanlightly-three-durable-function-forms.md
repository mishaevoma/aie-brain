---
type: source
title: "The Three Durable Function Forms"
author: "Jack Vanlightly"
publisher: jack-vanlightly.com
url: https://jack-vanlightly.com/blog/2025/12/10/the-three-durable-function-forms
published: 2025-12-10
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms]
---

# The Three Durable Function Forms

**In one line:** Durable code comes in three shapes (a one-shot stateless function, an interactive session that ends, and an actor that lives until it is deleted), and choosing among them means choosing identity, lifetime and how the outside talks to it.

## What it says

- Engines use different words (workflow, activity, virtual object, handler) for the same few patterns. The post orders them from pure behaviour to long-lived state.
- **Stateless function**: runs once from start to end. It has no public address while running, and the caller can only await the result. Its stored state is step results kept for recovery.
- **Session**: a long-running process with a start, an end and an execution id that others can address while it runs, to send it messages or to query it. The example is a loan application that waits for a manual approval and can be queried or cancelled in the meantime.
- **Actor**: a durable object with a permanent identity and state, exposing functions that run one at a time. It exists independently of any execution and must be deleted explicitly. The example is a shopping cart used over weeks.
- Four properties tell the forms apart: addressable while running or not, execution id versus entity id, bounded versus unbounded lifetime, one-shot versus ongoing communication.
- Concurrency differs. A session's main function advances single-threaded and takes outside interactions at its suspension points. An actor processes calls serially, like a mailbox, so each call should be short.
- The forms compose into one tree: a session can call stateless functions and actors.
- Mapping to engines: Temporal workflows are sessions (signals, updates, queries) and activities are close to stateless functions. Restate has all three (basic service, workflow, virtual object). DBOS workflows are sessions. Resonate builds on durable promises and gets sessions by blocking on a promise that someone else resolves.
- In every form the logic is deterministic control flow plus recorded side effects, made reliable by re-execution.
- A session can be made effectively unbounded. Temporal's continue-as-new hands an oversized history over to a fresh workflow that carries on from it.

## What to do with it

- Decide the form before the engine. Work that starts, runs and ends is a session. A thing with an identity that outlives any one task is an actor.
- Give actors short handlers, and move long work into sessions that they start.
- For a session with no natural end, plan how its history is cut.

## Terms

- **Session** — interactive, bounded, addressed by an execution id.
- **Actor** — persistent, addressed by an entity id, one call at a time.

## Caveats

- Conceptual, from December 2025, and not about agents. Mapping one agent run to a session, and a standing per-user agent to an actor, is this brain's reading.
- The engine mapping is the author's, and he notes that real engines blur the lines.
