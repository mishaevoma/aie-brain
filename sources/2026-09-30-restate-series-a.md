---
type: source
title: "Restate raises $20M Series A to make Durable Execution a building block for every backend"
author: "Stephan Ewen"
publisher: Restate
url: https://restate.dev/blog/announcing-series-a
published: 2026-09-30
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Restate raises $20M Series A to make Durable Execution a building block for every backend

**In one line:** The price and latency of one durable action decide whether an agent is recorded around its loop or inside it; Restate puts managed durable execution at tens of dollars per million actions against about a dollar per million database writes.

## What it says

- **Price.** Managed durable execution usually costs tens of dollars for every million durable actions, often $25–$50. A database or queue is put at about $1 per million writes or events. The post concedes such an action does more work than a write, but argues the gap shapes design: at such prices developers use durability sparingly and draw coarse activity boundaries.
- **Latency.** A durable action also spends latency budget; taking it from 25+ ms to under 5 ms makes adding a step an easier decision.
- **Around versus inside the loop.** Durability around the agent loop restarts the whole activity after a failure. Durability inside it (persisting inference, tool calls and guardrail evaluations) reuses saved results, retries only the interrupted step and keeps the execution history consistent, which matters for sensitive, costly or long-running tasks.
- **Replit.** Replit moved the Replit Agent's execution to Restate within a wider rework of the agent's architecture. The new design uses more than 10x the durable actions of the previous generation. An agent can then stay in one process while individual inference and tool calls become durable, instead of bouncing between an orchestrator and separate activities.
- **The hot path.** Making a step durable needs only a fast durable append to a log: in Restate a quorum write, one network roundtrip. RocksDB serves reads by materialising state from the log, and object stores hold snapshots. Consensus, failover handling and the replicated log were purpose-built, not assembled from an existing database and queue.
- **Push, not pull.** Workflow engines usually have workers pull from task queues. Restate pushes invocations to function deployments (containers or FaaS) over a bidirectional stream, suspending functions that wait a day. Push lacks the back-pressure of pulling, so the dispatcher does flow control.
- **Operations.** Highly available durable execution runtimes typically consist of several systems plus a database, which is a problem when data must stay inside a network boundary. Restate, one binary without dependencies that forms clusters, is offered as making self-hosting and BYOC viable.
- Virtual Objects hold state that outlives one workflow (agents, sessions) with exactly-once state mutations.

## What to do with it

- Estimate durable actions per agent run, then compare runtimes on price and added latency per action before choosing how finely to record.
- Record around the loop only where repeating a whole activity after a failure is acceptable.
- If data must stay in your network, count the services and databases a runtime needs.

## Terms

- **Durable action** — the unit that is priced and timed: one recorded operation such as an inference or tool call.

## Caveats

- A funding announcement by the vendor. The prices are round and unattributed, Restate's own price is not given, and the latency figures come without conditions.
- The 10x figure for Replit has no baseline, and the previous system is not named.
- Measured overhead is in [Durable Coroutines](2026-11-03-restate-durable-coroutines.md).
