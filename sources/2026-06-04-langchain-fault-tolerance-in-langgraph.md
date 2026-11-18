---
type: source
title: "Fault Tolerance in LangGraph: Retries, Timeouts, and Error Handlers"
author: "Quanzheng Long, Sydney Runkle"
publisher: LangChain
url: https://www.langchain.com/blog/fault-tolerance-in-langgraph
published: 2026-06-04
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution, side-effects]
---

# Fault Tolerance in LangGraph: Retries, Timeouts, and Error Handlers

**In one line:** Give each step of an agent three things from the runtime: a retry policy for transient errors, a timeout that tells slow from stuck, and a handler that runs once retries are spent, which is where compensation goes.

## What it says

- The error handling that production needs (retries, timeouts, fallbacks) is often longer than the logic it protects. So it belongs in the runtime, attached to each step.
- **Retry policy.** Exponential backoff, optional jitter, a cap on attempts and a rule for which errors count. The default retries connection errors and 5xx responses. It does not retry value, type or runtime errors, which are almost always programming bugs.
- **Timeout policy.** Two kinds. A run timeout limits the total wall-clock time of one attempt. An idle timeout resets on every sign of progress (state writes, streamed chunks, child events, or an explicit heartbeat), so long work that is still streaming survives and a hung call does not.
- **Error handler.** A function that runs only after retries are exhausted, with the failing step's name and its exception. Uses: cleanup, alerts, dead-letter writes, falling back to a cheaper model, an apology message.
- The switch into the handler is committed to the checkpoint. If the process crashes during the handler, the resumed run schedules the handler again, not the step that failed.
- **Saga.** For a sequence of real-world changes (reserve a seat, take payment, issue a ticket), retry each step on its own. When one gives up, undo the steps that ran, in reverse order. Include the failed step in the undo, because whether it took effect is unknown. Saved state records which steps completed.
- A 1% transient failure rate is a small nuisance in a demo and compounds across an agent with dozens of steps.

## What to do with it

- Classify errors: retry the transient ones and fail fast on bugs.
- For long tool calls use an idle timeout with heartbeats, not only a wall-clock cap.
- Write the undo for every step that changes the outside world, and treat a failed step as possibly done.

## Terms

- **Saga** — a multi-step change with a compensating action for each step instead of one transaction.
- **Idle timeout** — a limit on time without progress.

## Caveats

- Describes features of one framework, by its maintainers, in June 2026.
- The example is a fixed workflow. How a sequence of tool calls chosen by a model gets its compensations is not addressed.
