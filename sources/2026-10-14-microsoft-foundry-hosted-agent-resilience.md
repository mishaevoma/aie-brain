---
type: source
title: "Resilience for long-running Microsoft Foundry hosted agents"
author: "Microsoft"
publisher: Microsoft Learn
url: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/long-running-agent-resilience
published: 2026-10-14
ingested: 2026-11-17
kind: docs
read: full
concepts: [managed-agent-runtimes]
---

# Resilience for long-running Microsoft Foundry hosted agents

**In one line:** Foundry hosted agents separate three guarantees (outliving the client connection, surviving loss of the process, a stream clients can rejoin), and recovery re-runs the handler from the top, so checkpoints and duplicate-proof side effects stay the application's job.

## What it says

- Covers two Microsoft Learn pages: this one and "What are hosted agents?" (last updated 2026-11-11), the source of the last bullet.
- **Three behaviours.** *Background execution*: work continues after the HTTP connection closes, with clients polling or reconnecting; it dies with the owning process. *Resilient execution*: a durable work identity, persisted input, detection of process loss and handler re-entry. *Stream replay*: retained events a reconnecting client reads from a cursor, not a checkpoint of workflow state.
- **Recovery.** The runtime stores a handler's input before starting it and takes a lease on the work record, renewed while the handler runs. When the process dies and the lease lapses, a later process reclaims the record and calls the handler with the same identities and input.
- **What it is not.** Re-entry starts at the top: no deterministic replay, no restored local variables or call stack. Nor is it a retry, which handles a failure the running handler reported and can use retry budget. Resilient tasks give no workflow orchestration (fan-out, durable timers, child workflows) or bulk storage.
- **Scope.** On the Responses protocol only stored background responses recover, and only when the server opts in; foreground responses are not reinvoked. On Invocations the application defines the contract and uses the AgentServer resilient task primitive.
- **Application's part.** A safe rerun path, or a branch that resumes from durable progress; checkpoint references, idempotency keys and side-effect watermarks; its own storage for history, tool results and artifacts. Task metadata is a checkpoint index, not a checkpoint store.
- **Stream after recovery.** A later `response.in_progress` event is a snapshot reset: the client replaces its accumulated output with the snapshot.
- **Platform.** One VM-isolated sandbox per session. The idle timeout is 2 through 240 minutes per agent version, 15 by default; then compute is deprovisioned, and `$HOME` and `/files` are restored onto new compute at the next request. A session is permanently deleted after 30 days of inactivity. Billing follows CPU and memory consumed during active sessions.

## What to do with it

- Ask which of the three behaviours a "durable" runtime means.
- Design handlers so a kill at any point leads to a safe rerun or a resume from a recorded boundary.
- Persist a watermark before a side effect that must not repeat, clear it after commit, check it on re-entry.
- On a stream reset, replace the client's output; do not append.

## Terms

- **Work identity / input identity** — the logical job or conversation, and one input or turn within it.

## Caveats

- The page shows only a last-updated date, 2026-10-14, used above as the publication date.
- Vendor documentation of a contract: no lease durations, recovery times or failure rates.
- Resume restores files; neither page says process memory returns.
- This brain's reading: a session stays active, hence billed, until its idle timeout elapses.
- [Restate's article](2026-06-15-restate-checkpointing-is-not-resiliency.md) argues that such checkpoint-and-re-enter designs leave most work to the developer.
