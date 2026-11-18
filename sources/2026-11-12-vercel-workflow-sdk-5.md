---
type: source
title: "Workflow SDK 5: built for production"
author: "Pranay Prakash, Peter Wielander"
publisher: Vercel
url: https://vercel.com/blog/workflow-sdk-5
published: 2026-11-12
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms]
---

# Workflow SDK 5: built for production

**In one line:** Vercel's replay-based workflow engine now runs several steps per invocation and replays incrementally, and its own benchmark puts p75 overhead between steps at 109 ms, down from 618 ms.

## What it says

- Each run has an event log of every step's arguments and return value, and recovers from a crash or a deploy by replaying it. Stated scale since launching the previous year: over 4 billion steps in 700 million runs.
- **Queue hops.** Version 4 spent two queue hops per step: one to start it, one to continue the workflow. Version 5 runs several steps inline per invocation, parallel ones included, until a wait, a hook or a nearing timeout.
- **Incremental replay.** Version 4 replayed the full history, so overhead grew with the log. In version 5 it stays low.
- **Benchmarks:** v4.8.12 against v5.2.0, October 8, 2026, Vercel production in `iad1`, managed Vercel World, 1 KB of JSON in and out of each step.
  - First step, p75: 418 ms, then 172 ms. Resume, p75: 699 ms, then 425 ms.
  - Between steps, five-step run, p75: 618 ms, then 109 ms.
  - Late in a 1,020-step run, p75 overhead: 1,748 ms, then 70 ms. Whole run, median: 21.0 minutes, then 3.0.
  - Recorded 52.4-second agent response, 2,593 chunks, ten runs per version: median delivery 226.1 s, then 53.5 s (now over WebSockets). Chunk trip, p75: 172 ms, then 102 ms. Runs with a chunk over 1 s late: 6 of 10, then 0.
- **Encryption.** What a run stores (inputs and outputs of workflows and steps, hook payloads, streams) is encrypted with AES-256-GCM under a per-run key before leaving the application, so the backend holds only ciphertext. On Vercel it derives from a deployment-scoped key. Self-hosted Worlds supply a stable 32-byte key per run. Run attributes are plaintext. Compressed AI token streams average about 80% smaller.
- **Where state lives.** Version 4 kept every run's log, queue and streams in `iad1`. A version 5 run has a home region for them: by default where it started, or one passed to `start()`. Steps execute where the application is deployed. Under function failover steps may run in a fallback region; state stays in the home region.
- Other consumers of a World, such as durable-harness, share the storage, queue and streaming gains but not the replay optimisations.

## What to do with it

- Before ruling replay in or out for an agent loop, measure per-step overhead early and late in a long run.
- Treat run history as sensitive data: encrypt it and keep secrets out of plaintext attributes.
- Choose the home region for data residency or nearness to the database, and deploy the steps there.

## Terms

- **World** — the storage, dispatch and streaming interface beneath the SDK.

## Caveats

- A vendor's launch post with its own figures: one workload, small payloads, one region, one day. The post says they do not predict other applications. Tail latencies were not read.
- Incremental replay is not explained, nor what happens to a run whose home region fails.
- This brain's reading: the figures answer the objection of [Building LangGraph](2025-09-04-langchain-building-langgraph.md) that replay engines add latency between steps and slow as history grows.
