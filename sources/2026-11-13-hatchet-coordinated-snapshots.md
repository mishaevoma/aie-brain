---
type: source
title: "Coordinated snapshots of agent state"
author: "Alexander Belanger"
publisher: Hatchet
url: https://hatchet.run/blog/agent-statefulness
published: 2026-11-13
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Coordinated snapshots of agent state

**In one line:** Keep an agent's filesystem in sandbox snapshots and its session in a durable workflow, and tie them together by writing each snapshot's id into the workflow's event log, at turn boundaries, not every write.

## What it says

- A coding agent such as Claude Code has at least three kinds of state: the filesystem it edits, the context (the tokens fed to the model) and the session (tool-call history plus status such as paused). In the cloud each must move between disposable machines and survive a pause, because idle compute is too costly to keep.
- **Filesystem.** A persistent VM or block-disk snapshots per agent get expensive quickly. Archiving the workspace after each turn, by git commit or `tar` to S3, suits an MVP but is slow and costly at scale, with restores taking tens of seconds. Sandbox providers (Archil, E2B, Freestyle) offer snapshot and restore as a primitive. Isolation and filesystem durability need not be coupled, though they often are.
- **Session.** Long sessions fit durable execution: each tool call goes to a durable event log and is replayed elsewhere when a machine dies. An agent with no filesystem needs only this. Hatchet and Temporal evict idle workflows from workers, which keeps thousands or hundreds of thousands of such agents efficient in compute. The post's rule: millions of agents paused awaiting feedback should be durable workflows.
- **Coordination.** Each store has its own snapshot: event log and disk image. The workflow listens for user events and calls the agent; when the sandbox work completes, the new disk snapshot's id is recorded in the workflow's log. The harness may run inside the sandbox, outside it (the workflow is then the agent loop), or both, a dual harness.
- **Checkpoint frequency.** Databases default to point-in-time restore because their writes are critical. Most agent writes are not: a turn can be redone. Keep each turn's output, not each incremental write; a machine failure then costs, in rare cases, a user waiting twice as long.
- **Defaults.** With `@hatchet-dev/sandbox` each provider call can record a snapshot in the durable task's event log. `snapshotEveryTurn` is off by default: snapshots are taken only on `kill`. The knob exists because strongly consistent durable filesystems add latency and cost. Sessions resume from the latest snapshot or fork from a chosen one.

## What to do with it

- Model paused sessions as durable workflows, so waiting holds no compute.
- Record the filesystem snapshot id in the session log at each turn boundary; go finer only where redoing a turn is unacceptable.
- Start with git or `tar` to S3 per turn; move to provider snapshots when restore time or forking hurts.

## Terms

- **Coordinated snapshot** — a filesystem snapshot whose id is recorded in the durable workflow's log.
- **Checkpoint frequency** — how often state is saved, which bounds the work a failure loses.

## Caveats

- Vendor post ending in a product pitch; cost and latency claims are qualitative.
- Context is named as state but given no store; by implication it travels in the event log.
- The default (snapshot only on `kill`) is coarser than the advice to keep every turn's output; what a crash before `kill` loses is not stated.
