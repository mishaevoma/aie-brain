---
type: source
title: "Project Think: building the next generation of AI agents on Cloudflare"
author: "Sunil Pai, Kate Reznykova"
publisher: Cloudflare
url: https://blog.cloudflare.com/project-think/
published: 2026-04-15
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, long-running-agents, multi-agent-systems, sandboxing-and-permissions]
---

# Project Think: building the next generation of AI agents on Cloudflare

**In one line:** Run each agent as its own durable actor that costs nothing while asleep and wakes on an event, checkpoint long work inside it, and give it a ladder of sandboxes from a virtual filesystem up to a full machine.

## What it says

- Premise: agents are one-to-one. Each instance serves one user or one task, so a product needs capacity per session, not per shared server. A coding agent on a laptop or an always-on virtual server costs the same idle or busy, and cannot be shared or handed over.
- **An actor per agent.** The Agents SDK runs every agent as a Durable Object with an identity and its own SQLite database. It uses no compute while hibernated and wakes when something arrives: a request, a WebSocket message, an alarm it scheduled or an email. The post's comparison: 10,000 agents that are each active 1% of the time need 10,000 always-on containers, or about 100 active actors.
- **Fibers for crash recovery.** A model call takes about 30 seconds and a loop far longer. A deploy or restart in that window cuts the connection and loses in-memory state. `runFiber()` registers the invocation in SQLite before it starts, `stash()` saves a checkpoint, and a recovery hook runs after a restart. The developer decides what to save and how to resume. Nothing is replayed.
- Waiting has two tiers. A keep-alive covers work that lasts minutes. For longer outside work (CI, video generation) the agent stores the job id, hibernates and wakes on the callback.
- **Sub-agents** are child actors with their own database, called through typed RPC, with no shared storage.
- **Sessions** are stored as a tree of messages. That gives forking, compaction that summarises while the full history stays in SQLite, and full-text search.
- **Execution ladder.** Tier 0 is a durable virtual filesystem. Tier 1 is a V8 isolate with no network that runs model-written code. Tier 2 adds npm packages, tier 3 a headless browser, tier 4 a full sandbox with toolchains. An agent should already be useful at tier 0.
- Isolates begin with no ambient authority, and capabilities are granted one by one. Stated figures: they start in milliseconds, which the post puts at about 100x faster than a container, and use up to 100x less memory.
- Code mode: the Cloudflare API MCP server exposes two tools at about 1,000 tokens, against about 1.17 million tokens for one tool per endpoint.
- `Think` is an opinionated harness built from these parts.

## What to do with it

- Price the idle time. If most agents wait most of the time, prefer a runtime that charges nothing while they sleep.
- Start long outside work, store its id, and sleep until a callback, instead of holding a process open.
- Escalate sandbox power only when a task needs it, and grant capabilities instead of removing them.

## Terms

- **Fiber** — a registered, checkpointable function invocation that is recovered after a restart.
- **Hibernation** — an idle actor evicted from memory with its state kept.
- **Execution ladder** — the tiers of compute an agent escalates through.

## Caveats

- A vendor's launch post. Project Think was a preview with APIs expected to change, and the cost comparison is illustrative, not measured.
