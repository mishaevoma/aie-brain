---
type: source
title: "Pi Durable"
author: "Earendil Engineering"
publisher: Earendil
url: https://earendil.com/posts/pi-durable/
published: 2026-10-01
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution, side-effects]
---

# Pi Durable

**In one line:** Durability can live inside the harness: every model request, tool call and compaction is a task that checkpoints to the harness's own storage, and a new process that opens it resumes the work.

## What it says

- An experimental package released with Pi 1.0. The Pi coding agent stays a one-person terminal tool, resumed by hand after a crash; this is a separate framework for long-running agents that outlive failures.
- **Where durability sits.** The harness opens on a storage backend (memory, SQLite and JSONL ship). Every step in a run is a task, which saves a checkpoint before going further. After a crash, whichever process next opens that storage resumes each unfinished task at its latest checkpoint.
- **Interrupted model request:** resent. The partial answer is kept in the transcript, flagged as aborted.
- **Interrupted tool call:** the intent of each call is written to storage before it runs. A tool declared `replay: "safe"` runs again. Any other tool is never repeated: the model gets an interruption notice with the output saved so far, and chooses the next step.
- **Exactly-once submission:** a submission carries a `requestId`, and a retry with the same id returns the first submission. A crash can rerun a hook, so a hook records its decision in a memo, a stored value that only the first write sets.
- **Application state** (a to-do list, a plan) lives in documents: typed JSON changed in the same atomic commit as the transcript, so the two cannot disagree.
- Subagents are not built in; a tool makes one as a conversation it owns. An abort reaches owned work first, and every task cleans up its own effects.
- A conversation records its extensions and tools by name, never as code, and after a restart runs whatever the new process has installed.
- **Size:** about 15,000 lines without tests (3,000 are storage backends), roughly 150,000 tokens for GPT and 250,000 for Claude, so a coding agent can read it.

## What to do with it

- Store a tool call's intent before it runs, make each tool declare whether a rerun is safe, and report an interrupted unsafe call to the model without repeating it.
- Give each submission a client-chosen id, so a retry returns the first one.
- Commit application state in the same transaction as the transcript entry that caused it.

## Terms

- **Harness** — storage plus the machinery that runs model conversations in parallel; it supplies the tools the models call and the execution environments those tools run in.

## Caveats

- The authors' launch post, October 2026: a tour and a demo, no production figures. The API may change.
- Stated limits: it needs a JavaScript runtime, and a storage has one owning process at a time. Loss of the machine or the storage is not discussed; [Temporal's reply](2026-10-08-temporal-immortal-life-of-pi.md) starts there.
- It never discusses workflow engines or deterministic replay (`replay` is only a tool's rerun flag). That it needs neither is this brain's reading, not the authors' argument. [Restate](2026-06-15-restate-checkpointing-is-not-resiliency.md) puts this work under the SDK, and [Vercel](2026-10-19-vercel-making-every-harness-durable.md) adds a similar intent record and replay policy from outside.
- Running new code after a restart is the opposite of the version pinning Restate asks for.
