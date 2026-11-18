---
type: source
title: "The Plumbing Wars - Are Claude Managed Agents Worth It?"
author: "David Proctor"
publisher: "Trilogy AI Center of Excellence (Substack)"
url: https://trilogyai.substack.com/p/the-plumbing-wars-are-claude-managed
published: 2026-04-28
ingested: 2026-11-17
kind: article
read: full
concepts: [managed-agent-runtimes]
---

# The Plumbing Wars - Are Claude Managed Agents Worth It?

**In one line:** For a team committed to Claude, renting the agent runtime is argued to be nearly automatic: months of plumbing replaced for a runtime fee of $0.08 per active session-hour, at the cost of a Claude-only harness and sessions held by Anthropic.

## What it says

- **The case for renting.** Agent teams have spent two years rebuilding the same parts: a model loop, a sandbox, checkpointing, a credentials vault, a permissions model and tracing. Claude Managed Agents, launched April 8, 2026, hosts them all. The author counts the work replaced in months, cites Anthropic's latency figures for the decoupled design (time-to-first-token cut by roughly 60% at p50 and by more than 90% at p95), and gives teams still hand-rolling infrastructure for Claude roughly "ten weekends" to defend it. Differentiation, he argues, lies in what an agent does, not in how it runs.
- **Cost arithmetic.** The starting rate is $0.08 for each active session-hour, charged in addition to normal Claude token prices. Idle time is free. Web search costs a further $10 per 1,000 searches.
  - One always-on agent: 730 hours × $0.08 ≈ $58.40, about $58 a month.
  - 24 agents each working eight hours a day: 24 × 8 × 30 × $0.08 ≈ $460.80, about $461/month.
  - Both exclude inference tokens and are the author's illustrations, not Anthropic's. At a few hundred agents, he says, runtime "starts to rival" model spend.
- **What you give up.** Sessions live on infrastructure Anthropic manages. The harness runs Claude models only. Tool integrations follow Anthropic's runtime and MCP conventions.
- **Not generally available.** The whole product was in public beta, and every endpoint required the `managed-agents-2026-04-01` beta header. Multi-agent coordination and Outcomes (self-evaluation, claimed to add up to 10 points of task success) needed a separate research-preview application.
- **For everyone else** it depends on whether orchestration commoditises around neutral platforms (Microsoft's bet) or integrates vertically with model providers (Anthropic's). Microsoft is model-agnostic, sells Copilot Studio capacity packs at $200 a month for 25,000 Copilot Credits, and led agent orchestration adoption in a February 2026 VentureBeat survey with 38.6%, against 5.7% for Anthropic's tool-use API.

## What to do with it

- Cost the runtime fee apart from tokens: active hours × the current rate.
- Before designing around multi-agent coordination or Outcomes, check that they have left preview.
- Build the runtime yourself only for a reason you can name, such as model choice or control of stored state.

## Terms

- **Active session-hour** — an hour in which a session runs, not one spent awaiting input or tool confirmations.

## Caveats

- Commentary built mainly from Anthropic's own pages and press coverage; no first-hand use or measurement is reported.
- Written under three weeks after launch. Prices and preview gating may have moved.
- No token bill is worked out, so runtime rivalling the model bill is asserted, not shown. The survey (56, then 70 organisations) is called directional and predates Managed Agents.
- It notes that sessions sit with Anthropic but not whether that state can be moved, the point on which [Your harness, your memory](2026-04-11-chase-your-harness-your-memory.md) argues the opposite side. [Scaling Managed Agents](2026-04-08-anthropic-managed-agents.md) describes the product and supplies the latency figures.
