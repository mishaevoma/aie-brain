---
type: source
title: "Durable Execution Pricing in 2026: How Temporal, Step Functions and Others Bill You"
author: "Haziqa Sajid"
publisher: Diagrid
url: https://www.diagrid.io/blog/durable-execution-pricing-models-2026
published: 2026-09-17
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, durable-execution, production-operations]
---

# Durable Execution Pricing in 2026: How Temporal, Step Functions and Others Bill You

**In one line:** What a platform counts decides a durable execution bill more than its rate: Temporal Cloud and AWS Step Functions charge for every retry, Cloudflare Workflows for none, capacity plans for peak concurrency, and an agent picks its own step count.

## What it says

- **Two families.** Temporal Cloud, AWS Step Functions, Cloudflare Workflows and DBOS meter units of work, each with its own unit. Azure Durable Task Scheduler Dedicated and Diagrid sell reserved capacity. Figures are US list prices checked on 29 Sep 2026.
- **Temporal Cloud** bills Actions at $50 per million. One Action each: workflow start, activity start, each activity retry, timer, signal, query, update, and heartbeat that reaches the server. A child workflow start is 2 and a scheduled run 3. The Developer plan adds 10% of usage and has no base fee. Waiting is unmetered, but storage accrues.
- **AWS Step Functions Standard** bills state transitions: 4,000 a month free, then $0.000025 each (US East, N. Virginia). Each retry is another transition.
- **Cloudflare Workflows** (Workers Paid) includes 500,000 steps a month, then $0.80 per 100,000, plus meters for requests, CPU time and storage. Retries are not counted as steps. A sleeping or waiting step counts, but uses no CPU time.
- **DBOS** bills checkpoints (workflows, steps and transactions): Pro is $99 a month with 1 million, then $50 per million.
- **Azure Durable Task Scheduler.** Consumption bills actions, meaning messages dispatched to your application (two per activity in Microsoft's example); a completed timer is one. Dedicated bills Capacity Units at about $500 a month each in East US.
- **Diagrid** bills concurrent workflow instances, counting child workflows separately. Dedicated Cloud costs from $1,499 a month. Retries, timers and heartbeats are not metered; whether a parked workflow occupies a slot is not stated.
- **Worked example.** A million agent runs per month at 10 tool calls each, with 30% of calls succeeding on the fourth attempt, means 9 million retries. They alone cost $495 on Temporal's Developer plan ($450 plus the 10% fee), $225 on Step Functions Standard and $0 on Cloudflare.
- **Agents.** Step count is the agent's choice: the same request can need four tool calls or fourteen, so the metered bill is unknown before the run. Temporal's own cost guidance blames many activities, frequent signals, heartbeats and high retry rates for large Action counts; the article calls that an ordinary agent run. On Diagrid, five parallel sub-agents run as child workflows fill six slots.

## What to do with it

- Compare counting rules before rates; they are often not on the pricing page.
- Apply your tool-call failure rate to those rules; count timers, signals and heartbeats per run.
- Ask capacity-priced vendors in writing how a waiting workflow is counted.

## Terms

- **Action** — Temporal's billing unit; Microsoft uses the word for something else.

## Caveats

- Diagrid competes with the vendors it prices, lists its own capacity-priced product beside them, and ends with a sales pitch.
- Published 17 September 2026, updated 28 October 2026; confirm list prices with each vendor.
- The example prices only retries, at an assumed failure rate. Several cells read "not stated", including DBOS retries.
