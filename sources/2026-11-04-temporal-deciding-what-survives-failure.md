---
type: source
title: "Durable Execution means deciding what survives failure"
author: "Muhammad Abu Bakkar Bin Akmal"
publisher: Temporal
url: https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure
published: 2026-11-04
ingested: 2026-11-17
kind: article
read: full
concepts: [side-effects]
---

# Durable Execution means deciding what survives failure

**In one line:** A durable engine remembers how far a run got, but neither stops an Activity running twice nor decides what counts as an accepted answer; a review of two Temporal Workflows shows where the application must supply those rules.

## What it says

- Two Workflows on an unnamed Kubernetes analysis platform are reviewed: a cluster scan fanning out to analysers, and a proposer/judge loop recommending a Kubernetes version.
- **Duplicates.** Once an Activity's completion is in Event History, replay reuses its result. If the external write succeeds but the Worker is lost before that completion is written, the Activity runs again; Temporal does not prevent this. Deduplicate at the receiving system on a stable business key. Having a Workflow ID is not enough to make an Activity idempotent.
- **Starting.** Saving the scan record and starting the Workflow are two operations; either can fail alone. The scan ID is the Workflow ID, but handling of an existing ID was left to SDK defaults. The post asks for an explicit conflict and reuse policy, plus reconciliation that starts the Workflow for a record lacking one.
- **Exits.** The loop returns one of four outcomes: consensus; approved score, where the judge approves and the score reaches a configured threshold; repeated concerns; round limit. Only the first two count as accepted. The others are unresolved results, not failures. An exhausted budget and invalid structured output are raised separately as non-retryable errors. The caller receives the exit reason.
- **Cache.** The key combines request fields with source-data, prompt and model versions. Only accepted decisions are written or served, because output can be valid against its schema and still have been rejected.
- **Budget.** The proposer is limited in model requests, tool calls and rounds. Judge calls are not counted, so the budget does not cap total inference spend.
- **Configuration.** Model identifier, round limit and score threshold were read from Worker process state. After a redeploy, a replaying Workflow could meet values different from those it started with, so they move into Workflow input.
- **Joins.** Six analysers run concurrently, each allowed 3 attempts and a 20-minute start-to-close timeout, but the Workflow awaits them in order: a failure in the sixth goes unseen until the first returns. Concurrency, retries and the join are separate policies.

## What to do with it

- For each external effect, ask what happens if it succeeds but its completion is never recorded. If the answer is a duplicate, deduplicate at the receiver on a business key.
- Keep accepted result, unresolved result and execution error apart, and return the exit reason.
- Cache only accepted results, checking on reads as well as writes.
- Put whatever changes workflow decisions (model, limits, thresholds, endpoints) into workflow input.
- Count judge calls if the budget must cap spend.

## Terms

- **Event History** — Temporal's record of a Workflow's execution, replayed to rebuild its state.

## Caveats

- A guest post on Temporal's blog by an Xgrid engineer; it closes by offering Xgrid's Workflow reviews.
- Findings come from reading one implementation, without incident or measured data. Code samples are simplified or corrected for publication, and the review found no tests for the failure scenarios it lists.
