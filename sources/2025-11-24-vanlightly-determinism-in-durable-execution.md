---
type: source
title: "Demystifying Determinism in Durable Execution"
author: "Jack Vanlightly"
publisher: jack-vanlightly.com
url: https://jack-vanlightly.com/blog/2025/11/24/demystifying-determinism-in-durable-execution
published: 2025-11-24
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution, side-effects]
---

# Demystifying Determinism in Durable Execution

**In one line:** A durable function recovers by running again from the top and reusing stored results, so its control flow must make the same decisions every time, while its side effects only need to be safe to run twice.

## What it says

- An engine-neutral model, meant to cover Temporal, Restate, DBOS and Resonate, in four parts.
- **Recovery is re-execution.** After a failure the function starts again from its first line. Each side effect that already completed returns its stored result instead of running. The outcome is the same as jumping to the first unfinished step.
- **Control flow and side effects are different things.** Control flow is the branching and looping that decides which side effects run. Temporal makes the split explicit (workflow versus activity). Restate and Resonate wrap side effects inside ordinary functions.
- **Control flow must be deterministic**, because it is re-executed in full. Two worked bugs, both double charges: a branch on the current time that flips between attempts, and a branch on a database record that the first attempt itself changed. The fix in both is to record the value as a durable step, so every replay sees the first answer. SDKs supply recorded clocks, random numbers and UUIDs for this.
- **Side effects need not be deterministic. They need idempotency or tolerance of duplicates.** A side effect can finish and the engine can fail before storing its result, and then it runs again. A repeated email may be acceptable. A repeated card charge is not.
- A durable function is not an atomic transaction. It guarantees progress to completion, not one all-or-nothing change across systems.
- The determinism rule exists only because recovery is replay. An engine that could resume at the exact line, with local state rebuilt, would not need it.
- Engines differ in detail. Some of the examples would raise a non-determinism error in Temporal, which checks each replay against the recorded history.

## What to do with it

- Treat every value your branching depends on (time, randomness, a database row) as a recorded step.
- For each side effect ask what happens if it runs twice. Add an idempotency key where the answer is harm.
- Do not expect rollback. Plan compensation for changes that span several systems.

## Terms

- **Control flow / side effect** — the deciding code that is replayed, and the outside action whose result is recorded.
- **Memoization** — reusing a stored step result on replay.
- **Duplication tolerance** — a side effect that may run more than once without harm.

## Caveats

- First post of the series "The Theory of Durable Execution". The author works at Confluent and is independent of the engines he describes.
- It does not mention LLMs. Applying it to agents (a model's answer is a non-deterministic value to record, a tool call is a side effect) is this brain's reading.
