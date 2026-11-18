---
type: source
title: "Building a durable /goal agent loop that survives crashes"
author: "Mitchell Alderson"
publisher: Inngest
url: https://www.inngest.com/blog/building-a-durable-goal-agent-loop-that-survives-crashes
published: 2026-11-02
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Building a durable /goal agent loop that survives crashes

**In one line:** Killing the worker under an agent loop of memoized steps never repeated finished work, but the run survived only while the next function had retries left: the durability boundary is the retry budget, not stored state.

## What it says

- **The build.** A /goal loop has an agent retry one goal until a check passes. Here the loop is one Inngest function, each attempt a child function (`step.invoke`), and each model turn, tool call and check a step. Loop state comes only from step return values, because the function body re-executes at every step. Every step must be safe to run twice.
- **Kill test.** The author ran `kill -9` mid-attempt. A new worker resumed the run about 15 seconds later, and the trace showed each finished turn once, none re-run or billed again.
- **Where durability ends.** A second kill left the worker down past the loop function's retry window. The run failed, although every finished step was still stored. Saved state lasts indefinitely; a run lasts only while the next function due to execute keeps retrying. By default that window lasts a few minutes; `retries: 20`, the maximum, extends it to hours, cheaply because finished steps are memoized.
- **Two kinds of model step.** `step.ai.infer` sends the request from Inngest's side, so it completes while the worker is down, as it did in the kill test. `step.ai.wrap` runs your client on the worker: you control the timeout, and a worker dying mid-call repeats that turn. The switch to wrap came after an infer turn hung with no timeout to set. Under wrap the SDK's retries are off and malformed requests are not retried.
- **Human review.** After `maxStalls` attempts without progress (5 in the example) the loop parks on `step.waitForEvent` with timeout `"3d"`. A reviewer's note enters the next attempt's brief; no reply, or a stop, ends the loop.
- **A fix reaching a live run.** A cancelled invoke resolved instead of rejecting, crashing the loop on every retry. A fix deployed during the backoff ran against the memoized results on the next retry and finished the goal without a restart.
- **Limits named.** Each step must finish within one request; a shorter host timeout overrides Inngest's step limit. Inngest caps steps per run and the size of step results and run state; no figures are given. One model turn kept a request open for 17 minutes. A dev server started without `--persist` lost a whole run.
- **Sandbox.** Only the grader, which executes model-written code, runs in a sandbox with no network.

## What to do with it

- Raise the orchestrating function's retries for unattended runs, and host the worker where it restarts.
- Give each model call a worker-owned timeout and turn off the SDK's retries.
- Validate what a child invocation returns; a cancelled one may not throw.

## Terms

- **Memoized step** — a step whose stored result is returned on re-execution.
- **Retry window** — how long a failed function keeps being retried, set by its retry count and backoff.

## Caveats

- A vendor-blog build log ending in a sign-up pitch: one developer, one test goal, one observed recovery time.
- Sandboxes are in public beta.
