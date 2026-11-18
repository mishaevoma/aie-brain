---
type: source
title: "The runtime behind production deep agents"
author: "Sydney Runkle, Vivek Trivedy"
publisher: LangChain
url: https://www.langchain.com/blog/runtime-behind-production-deep-agents
published: 2026-04-20
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms, durable-execution, harness]
---

# The runtime behind production deep agents

**In one line:** A harness makes an agent good and a runtime makes it deployable, and the runtime is a fixed list of capabilities under the harness, with durable execution as the one the others depend on.

## What it says

- The split: the harness is prompts, tools, skills and whatever else supports the loop. The runtime is everything underneath that keeps the agent running in production.
- Ten requirements, each with a runtime capability: reliability (durable execution), memory (checkpoints and a store), guardrails (middleware), multi-tenancy (authentication, authorization, delegated credentials, operator roles), human oversight (interrupt and resume), real-time interaction (streaming, concurrency control), observability (tracing, time travel), code execution (sandboxes), integrations (MCP, A2A, webhooks), scheduled jobs (cron).
- **Durable execution.** Runs sit on a task queue. Each step writes a checkpoint, to PostgreSQL by default, keyed by a thread id. When a worker dies its lease is released and another worker continues from the latest checkpoint. When a run waits for a person it gives up its worker slot and sleeps for as long as needed. Streaming, approvals, cron and concurrent input all build on this.
- **Memory.** Short-term state lives in the thread's checkpoints. Long-term memory needs a separate store organised by namespace (user, assistant, organisation), because checkpoints are scoped to one thread. Memory gathered over months is among the most valuable data the system produces, so it should sit in storage you control.
- **Multi-tenancy** is three separate problems: keeping one user's threads and memories from another (ownership tags on write, filters on read), letting the agent act with a user's own credentials (an OAuth flow and token store handled by the runtime), and deciding which team members may operate the deployment.
- **Human-in-the-loop** has two cases: approving, editing or rejecting a proposed tool call, and answering a question the agent cannot settle. The pause writes state, frees resources and can last days. The resume value can be any data, not only yes or no.
- **A new message during a run** ("double-texting") needs a policy: enqueue (the default and the safest), reject, interrupt and continue from the current state, or roll back and start fresh. Interrupting feels fastest but leaves half-finished tool calls to clean up.
- Streams should be resumable from the last event received.
- **Guardrails** that must always hold (redacting personal data before the model sees it, capping calls to a paid API) belong in code that wraps every model and tool call, not in the prompt.
- **Sandboxes** protect the host, not what is inside them. Credentials are injected by a proxy outside the sandbox. Warm pools remove cold starts.
- **Cron** comes in two forms: tied to one thread, so runs see their own history, or a fresh thread per run. Scheduled runs get the same retries, tracing and auth. Forgotten schedules keep running and billing.
- A closing argument against closed managed harnesses: lock-in to one model provider, and features such as server-side compaction whose output cannot be used elsewhere.

## What to do with it

- Use the ten rows as a checklist when choosing or building a runtime.
- Decide the concurrent-message policy on purpose.
- Keep long-term memory in a store and format you own.
- Treat tenant isolation, delegated user credentials and operator access as three designs, not one.

## Terms

- **Double-texting** — a user's next message arriving before the agent has finished with the previous one.
- **Time travel** — resuming from an earlier checkpoint, optionally edited, as a fork.

## Caveats

- A vendor's guide to its own hosted runtime, from April 2026. The capability list matches its product's features, and the lock-in argument favours its open-source position.
- One figure is given in passing: changing only the harness raised the Deep Agents score on Terminal Bench 2.0 by 13.7 points.
