---
type: source
title: "The immortal life of Pi (Running the Pi coding agent on Temporal)"
author: "Moe Abadi"
publisher: Temporal
url: https://temporal.io/blog/the-immortal-life-of-pi-running-the-pi-coding-agent-on-temporal
published: 2026-10-08
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution, side-effects]
---

# The immortal life of Pi (Running the Pi coding agent on Temporal)

**In one line:** Temporal's reply to Pi Durable accepts its programming model and adds one thing with a workflow engine, automatic takeover by another machine; an interrupted tool call is still not rerun, only recorded as outcome unknown.

## What it says

- A reply to [Pi Durable](2026-10-01-earendil-pi-durable.md): `pi-temporal` runs the Pi coding agent on Temporal Workers and keeps Pi's session file, tools and terminal UI.
- **Concession.** Pi Durable has the programming model right: checkpointed tasks, request ids that deduplicate submissions, intent recorded before an effect and outcome after it, write-once memos. The author sees harnesses rediscovering durable execution.
- **What an engine adds:** takeover when the host fails. Pi Durable's shipped persistent backends (custom ones are possible) allow one owning process with no locking across processes, and its README warns that the newest SQLite commits can vanish if power or the host fails. Recovery on another machine needs the storage to survive and a fresh process to reopen it; Temporal supplies automatic failover.
- **Mapping.** One session is one Workflow, and each piece of work in a turn runs as an Activity: `runModelCall`, one `runToolCall` per call, then `sealStep`, the only writer of a step's tool results. The Workflow loops within configured budgets and holds no conversation state. That lives in the transcript, a session file in a shared directory from which each Activity rebuilds the turn. Project files follow as Git bundles.
- **Interrupted tool call.** No command is assumed to carry an idempotency key, so no interrupted call is rerun automatically. A claim is written beside the session file before a tool is invoked, and the result next to it afterwards. A retry that finds a result hands it back. One that finds only a claim does not run the tool: it records the outcome as unknown and asks the model to inspect the current state, which cannot show how far the command got. Temporal's attempt counter cannot decide this, because an attempt can fail before reaching the tool. Model calls are retried on another Worker.
- **Stale worker.** Timing out an attempt is no proof that it stopped. Every write to the session file presents the Worker's lease, and a write guard refuses a Worker whose lease is gone. This blocks the transcript write, not the tool's external effects.

## What to do with it

- Write a claim before invoking a tool and the result after it. A claim without a result means unknown, whatever the retry count says.
- Fence transcript writes with a lease; a stale worker's side effects still happen.

## Terms

- **Claim** — a marker written before a tool runs; a retry reads it as possibly started.

## Caveats

- A vendor's experiment, October 2026, retrofitted with a small fork of Pi; new agents are pointed to the [Temporal Agent Harness](2026-08-20-temporal-agent-harness.md). Evidence: a demo that kills the active one of three Docker Workers every 15 to 40 seconds, successful in the runs tested.
- Handover covers only Worker-run tasks started with `/background` or from the CLI; an interactive turn still runs in the local process.
- The lease assumes exclusive file creation and consistent reads in shared storage, and sets no bound on clock skew.
