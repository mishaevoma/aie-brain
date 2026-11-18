---
type: source
title: "Postgres is All You Need for Durable Workflows"
author: "Peter Kraft"
publisher: DBOS
url: https://www.dbos.dev/blog/postgres-is-all-you-need-for-durable-execution
published: 2026-05-20
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Postgres is All You Need for Durable Workflows

**In one line:** If a durable workflow is a program that checkpoints to a database, the database can also be the orchestrator, and a separate orchestration server is unnecessary.

## What it says

- **The claim.** External orchestration (Temporal, Airflow, AWS Step Functions) puts a central server with its own data store between clients and workers, to dispatch each step and checkpoint its outcome. The article calls this overcomplicated: the core of the idea is only a checkpoint in a database.
- **State, queue and recovery in Postgres.** Submitting a workflow adds a row to a workflows table. Application servers poll it, dequeue with locking clauses so that exactly one worker takes each workflow, and checkpoint every step's output themselves. Integrity constraints expose a second worker running the same workflow when it checkpoints, and it backs off. When a server dies, another recovers its workflows from their checkpoints.
- **Scaling.** Workers are added freely, so the database sets the ceiling. One vertically scaled Postgres server is said to process tens of thousands of workflows per second, and DBOS reports over 1M per second sharded across several servers, with throughput growing linearly.
- **Failure modes.** An external orchestrator and its data store are both single points of failure, and both hold application data that must be secured. Here the only point of failure is Postgres, which adds nothing new for an application that already depends on it. Workers are interchangeable, and availability comes from streaming replication with automatic failover or a managed multi-AZ deployment.
- **Observability.** Checkpoints are rows, so any question about workflows is a SQL query.

## What to do with it

- Before adding an orchestration service, check whether the Postgres you already run can be the queue and the checkpoint store.
- Dequeue with a locking clause, and let an integrity constraint on the checkpoint stop a second executor.
- Plan the database's replication and failover as the workflow system's availability.

## Terms

- **External orchestration** — a central server that dispatches workflow steps to workers and stores their checkpoints.

## Caveats

- Written by a vendor of a Postgres-backed durable execution library, published May 20, 2026 and updated November 12, 2026. The throughput figures are its own, with no hardware, workload or latency given here.
- It argues in general terms: nothing on replay, on versioning workflows in flight, or on side effects that run twice.
- Compare [Absurd In Production](2026-04-04-ronacher-absurd-in-production.md), the practitioner's version of this argument, and [Restate](2026-06-15-restate-checkpointing-is-not-resiliency.md), which counts one Postgres instance in one region as a single point of failure.
