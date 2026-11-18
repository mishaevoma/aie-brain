---
type: source
title: "Long-running agents"
author: "Cloudflare"
publisher: Cloudflare Agents docs
url: https://developers.cloudflare.com/agents/concepts/agentic-patterns/long-running-agents/
published: 2026-10-27
ingested: 2026-11-17
kind: docs
read: full
concepts: [agent-platforms]
---

# Long-running agents

**In one line:** On Cloudflare an agent is a Durable Object, a durable identity whose process can vanish at any moment: only what reached SQLite survives, a heartbeat merely postpones idle eviction, and resuming interrupted work is a hook the developer writes.

## What it says

- Covers this page and its sub-page [Durable execution with fibers](https://developers.cloudflare.com/agents/agent-class/durable-execution/), the reference for `keepAlive()`, `runFiber()` and `startFiber()`.
- **Survives eviction:** `this.state` (written to SQLite on every `setState()`), `this.sql` tables, schedules, per-connection state, fiber checkpoints and status rows.
- **Does not survive:** in-memory fields, `setTimeout` and `setInterval` timers, in-flight fetches, closures and promise chains.
- **Causes of eviction:** inactivity, after roughly 70–140 seconds without a request or open WebSocket; code updates and runtime restarts, 1–2 times a day, unpredictably; the 15-minute limit on an alarm handler.
- **Keep-alive.** `keepAlive()` schedules a 30-second alarm heartbeat, and each beat resets the inactivity timer. It stops idle eviction only: a code update, alarm timeout or resource limit still ends the work, and nothing is recovered.
- **Fibers.** `runFiber()` records the task in SQLite before it starts and holds a keep-alive. `stash()` writes a checkpoint synchronously, replacing the last. After an eviction the next activation, a request or a persisted alarm, calls `onFiberRecovered()` with the fiber's name and last snapshot. The original closure is gone and nothing is replayed or retried automatically; the default hook logs a warning and deletes the row. A caller awaiting the fiber never gets its result.
- `startFiber()` adds an idempotency key, a retained status row, inspection and cooperative cancellation, for webhooks a provider may redeliver.
- **By duration.** Seconds: ordinary requests. Minutes: keep-alive, or `startFiber()` if acceptance must be safe to retry. Minutes to hours: Workflows. Hours to days: start the job, store its id, hibernate, and wake on a callback, scheduled poll or workflow completion.
- **Workflows or agent-internal.** Schedules and fibers suit the agent's own rhythms, at minutes per activation. A Workflow suits an independent pipeline: per-step retries with backoff, 30 minutes per step, unlimited steps.
- **Approvals.** Inside the agent, approval is built by hand from state and a WebSocket; Workflows provide `waitForApproval()`. A plan kept in state is suggested as the checkpoint to show a person.

## What to do with it

- Checkpoint before each expensive step, stash the whole recovery state, and write the recovery hook, because the default discards the work.
- Do not hold an agent awake for hours: store the job id and hibernate.
- Keep the plan and current step in state, so recovery and context rebuilding read one record.

## Terms

- **Eviction** — removal of the actor from memory by idleness, a code update or a limit.
- **Fiber** — a task registered in SQLite with checkpoints and a recovery hook.

## Caveats

- Vendor documentation with no publication date; the date above is the "Last updated" on both pages, Oct 27, 2026.
- The idle window is ~70–140 seconds in the text but about 2 minutes in the lifecycle diagram.
- Three days later [code updates became deferred by default](2026-10-30-cloudflare-durable-objects-defer-code-updates.md), best effort only; that note also covers a change to idle eviction that these pages do not mention.
- `waitForApproval()` is only named; the human-in-the-loop page was not read.
