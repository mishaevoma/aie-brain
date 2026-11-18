---
type: source
title: "Absurd In Production"
author: "Armin Ronacher"
publisher: lucumr.pocoo.org
url: https://lucumr.pocoo.org/2026/4/4/absurd-in-production/
published: 2026-04-04
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Absurd In Production

**In one line:** Five months of running agents on a Postgres-only durable execution library: the simple model held, checkpointing steps without replaying code removed the determinism burden, and the hard work was in leases, watchdogs and races.

## What it says

- Follows up [Absurd Workflows](2025-11-03-ronacher-absurd-workflows.md). The system runs in production at the author's company, mainly for agent workflows. The core model (tasks, steps, checkpoints, events, suspension) did not need to change.
- What did need work is what real workloads expose: claim handling, leases, deadlocks, races between events, and watchdogs that kill broken workers.
- **Small SDKs.** The logic lives in SQL. The TypeScript SDK is about 1,400 lines and the Python SDK about 1,900, against about 170,000 lines for Temporal's Python SDK. A person can read the whole SDK in an afternoon.
- **No determinism rule outside steps.** The engine loads cached step results and skips finished work. It does not replay and check the function, so code between steps may read the clock or a random number. Only step boundaries matter, which the author finds much easier to reason about.
- An agent maps to it directly: each loop iteration is a step. If the process dies on iteration 7, iterations 1 through 6 come from the store and work continues from 7.
- **Pull-based scheduling.** Workers pull tasks from Postgres when they have capacity. There is no coordinator and nothing pushes to workers, which keeps self-hosting simple and load management out of the infrastructure.
- Additions since launch: steps that can be begun and completed separately, so code can see whether a step already ran; task results that a parent can await; a CLI to inspect and retry stuck tasks; a small dashboard; a skill that lets coding agents debug workflow state.
- Other uses: cron jobs that dispatch workflows with a pre-generated deduplication key, so two cron processes trigger one task, and background work that must survive deploys.
- Still missing: a built-in scheduler, a push model for webhooks (waking a task on an incoming request), and table partitioning for cheap cleanup.
- The author doubts a durable execution library can sustain a company, and sees it as a good fit for non-commercial open source.

## What to do with it

- If you checkpoint at step boundaries and do not replay code, you avoid the determinism rule. Keep every side effect inside a step.
- Give cron-triggered runs a deduplication key derived from the scheduled time.
- Budget for lease handling, watchdogs and races if you build this yourself. They are where the effort went.
- Build an inspection command early: seeing exactly where a task stopped beats reading logs.

## Terms

- **Deduplication key** — an identifier that makes starting the same task twice a no-op.
- **Pull-based scheduling** — workers fetch work when they have capacity.

## Caveats

- One team's experience at unstated scale, with no failure or throughput figures.
- The comparison of SDK sizes is the author's own count.
