---
type: concept
title: "Durable execution"
updated: 2026-11-18
reviewed: 2026-11-18
status: contested
---

# Durable execution

**Definition:** Running multi-step work so that it survives crashes, deploys and long waits. Each completed step is recorded outside the process, and any worker can continue a stopped run from that record. For an agent the steps are model calls and tool calls.

## Why it matters

An agent run lasts minutes to days, so a crash, a deploy, a function timeout or a person who takes days to answer will interrupt it. [Deep Agents runtime, Apr 2026](../sources/2026-04-20-langchain-runtime-behind-deep-agents.md) · [Absurd in production, Apr 2026](../sources/2026-04-04-ronacher-absurd-in-production.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md) Starting over pays for the tokens again, and a tool call that runs twice can send a second email or charge a card twice. [Building LangGraph, Sep 2025](../sources/2025-09-04-langchain-building-langgraph.md) · [Determinism, Nov 2025](../sources/2025-11-24-vanlightly-determinism-in-durable-execution.md)

## Four mechanisms

| Mechanism | What is kept | On recovery | The price |
|---|---|---|---|
| Journal and replay | The result of every step | The code reruns, and finished steps return recorded results | Deterministic code between steps. On Temporal, capped history and payloads |
| Checkpoint | State at each step boundary | The latest checkpoint is loaded | Work since the boundary repeats unless an intent record marks it, and you supply the supervisor |
| Session log | Every event of the run | A stateless loop reloads the log | The harness must handle a half-finished call |
| Machine snapshot | The sandbox's disk, sometimes its memory | The machine is restored | Says nothing about which calls completed |

Sources, in row order: [Determinism, Nov 2025](../sources/2025-11-24-vanlightly-determinism-in-durable-execution.md) and [Pydantic AI docs, Nov 2026](../sources/2026-11-17-pydantic-durable-execution.md) · [Building LangGraph, Sep 2025](../sources/2025-09-04-langchain-building-langgraph.md), [Pi Durable, Oct 2026](../sources/2026-10-01-earendil-pi-durable.md) and [Restate, Jun 2026](../sources/2026-06-15-restate-checkpointing-is-not-resiliency.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md), [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) and [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md) · [Code And Let Live, Jan 2026](../sources/2026-01-09-fly-code-and-let-live.md), [E2B docs, Nov 2026](../sources/2026-11-12-e2b-sandbox-persistence.md) and [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md). The grouping into four is this brain's reading.

A log fits the session's history of calls and a snapshot fits the filesystem, so write each snapshot's id into the log at the end of a turn. [Hatchet, Nov 2026](../sources/2026-11-13-hatchet-coordinated-snapshots.md)

## What to do

**Record**

- Record every model response and tool result before acting on it, and write an *intent record* before each call, so that recovery can tell "never started" from "possibly done". [Determinism, Nov 2025](../sources/2025-11-24-vanlightly-determinism-in-durable-execution.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md)
- If recovery reruns your code from the top, keep everything its branching depends on (time, randomness, reads) inside recorded steps. This is the *determinism rule*, and it falls away only where nothing reruns. [Determinism, Nov 2025](../sources/2025-11-24-vanlightly-determinism-in-durable-execution.md) Absurd reruns a task without checking it against the record, and its author says code between steps may therefore read the clock. [Absurd, Nov 2025](../sources/2025-11-03-ronacher-absurd-workflows.md) · [Absurd in production, Apr 2026](../sources/2026-04-04-ronacher-absurd-in-production.md) This brain's reading: that relaxes the rule rather than removing it.
- Record at the level of each side effect when repeating one would hurt. [Restate, Jun 2026](../sources/2026-06-15-restate-checkpointing-is-not-resiliency.md) Inline journaling is cheap: Restate reports a median of 2.5 ms per step inside a coroutine in its production deployments, against tens of milliseconds for a step dispatched to a worker. [Durable coroutines, Nov 2026](../sources/2026-11-03-restate-durable-coroutines.md)
- Put under one durable workflow only the steps that must succeed together. [Function tree, Dec 2025](../sources/2025-12-04-vanlightly-durable-function-tree-part-2.md)

A recorded run can still repeat a tool call. Making the repeat harmless is on [side effects and approvals](side-effects.md).

**Supervise**

- Put a queue or supervisor outside the process, so that a dead run is noticed and handed on. Stored steps outlive a worker, but the run still dies when its retries run out. [Restate, Jun 2026](../sources/2026-06-15-restate-checkpointing-is-not-resiliency.md) · [Goal loop, Nov 2026](../sources/2026-11-02-inngest-durable-goal-agent-loop.md)
- Allow one writer per session, and reject writes from an attempt that has been superseded (*fencing*). Fencing stops a stale attempt's writes to the session, not the side effects it already caused. [Restate, Jun 2026](../sources/2026-06-15-restate-checkpointing-is-not-resiliency.md) · [Pi on Temporal, Oct 2026](../sources/2026-10-08-temporal-immortal-life-of-pi.md)
- Use an idle timeout, reset by every sign of progress, to tell slow from stuck. [Fault tolerance, Jun 2026](../sources/2026-06-04-langchain-fault-tolerance-in-langgraph.md)
- Reconcile what you sent against what started. One hosted engine lost runs to a leftover deduplication marker and recorded no failure. [Inngest incident, Nov 2026](../sources/2026-11-17-inngest-incident-missed-function-runs.md)

**Count the cost**

- Count steps per run before choosing a metered engine. An agent picks its own number of steps, and some engines bill every retry. [Diagrid pricing, Sep 2026](../sources/2026-09-17-diagrid-durable-execution-pricing.md) · [Restate funding post, Sep 2026](../sources/2026-09-30-restate-series-a.md)

## Where sources disagree

- **Is a checkpoint enough?** LangGraph's designers chose checkpoints over replay engines. [Building LangGraph, Sep 2025](../sources/2025-09-04-langchain-building-langgraph.md) A replay-engine vendor answers that a checkpoint only recovers finished work, and leaves failure detection, durable retries and single-writer sessions to you. [Restate, Jun 2026](../sources/2026-06-15-restate-checkpointing-is-not-resiliency.md) A team running a checkpoint library on Postgres says the simple model held in production, and that the effort went into leases, watchdogs and races. [Absurd in production, Apr 2026](../sources/2026-04-04-ronacher-absurd-in-production.md)
- **Is an engine needed at all?** An independent analyst says reliable multi-step work does not need one: queues also work, though each consumer must then be safe to repeat as a whole, which is harder. What an engine adds is the workflow as one governable thing. [Function tree, Dec 2025](../sources/2025-12-04-vanlightly-durable-function-tree-part-2.md) One engine vendor agrees for a task that is easily made idempotent and commits in one database transaction. [Hatchet primer, Dec 2025](../sources/2025-12-11-hatchet-how-to-think-about-durable-execution.md) Two projects put the whole engine in the Postgres database you already run. [Absurd, Nov 2025](../sources/2025-11-03-ronacher-absurd-workflows.md) · [DBOS, May 2026](../sources/2026-05-20-dbos-postgres-is-all-you-need.md) Another vendor makes every agent a workflow. [Temporal harness, Aug 2026](../sources/2026-08-20-temporal-agent-harness.md)
- **Where does it live?** Inside the harness [Pi Durable, Oct 2026](../sources/2026-10-01-earendil-pi-durable.md), around an unchanged harness [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md), under the agent SDK [Restate, Jun 2026](../sources/2026-06-15-restate-checkpointing-is-not-resiliency.md), or in a hosted session log [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md). A workflow vendor's reply to the first accepts its model and names what an engine adds: takeover by another machine when the host fails. [Pi on Temporal, Oct 2026](../sources/2026-10-08-temporal-immortal-life-of-pi.md)

This brain's reading: the camps agree on what must hold (recorded steps, a plan for repeated tool calls, an outside supervisor, one writer) and differ on who supplies it. Most of them sell one of the answers. Choose by what a repeated side effect would cost and by who will operate the system.

## Related

[Side effects and approvals](side-effects.md) · [Agent platforms](agent-platforms.md) · [Long-running agents](long-running-agents.md) · [Background agents](background-agents.md) · [Running agents in production](production-operations.md) · [Agents and workflows](agents-and-workflows.md)
