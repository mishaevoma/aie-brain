---
type: source
title: "How we built our multi-agent research system"
author: "Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford"
publisher: Anthropic
url: https://www.anthropic.com/research/multi-agent-research-system
published: 2025-06-13
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, evals, multi-agent-systems, production-operations, tool-design]
---

# How we built our multi-agent research system

**In one line:** For broad, parallelizable research, a lead agent that spawns subagents with their own context windows beats a single agent, mainly because it spends more tokens usefully. That costs about 15× the tokens of a chat, so it pays off only on high-value tasks.

## What it says

- Claude's Research feature is an **orchestrator-worker** system. A lead agent plans, saves its plan to memory (context past 200,000 tokens gets truncated), and spawns parallel subagents. The subagents search, judge results with interleaved thinking and return condensed findings. A separate CitationAgent then attaches sources to claims.
- Multi-agent (Claude Opus 4 lead with Claude Sonnet 4 subagents) beat single-agent Opus 4 by 90.2% on an internal research eval.
- On BrowseComp, three factors explained 95% of performance variance: token usage, number of tool calls and model choice. Token usage alone explained 80%. Moving to Sonnet 4 helped more than doubling the token budget on Sonnet 3.7.
- Cost: agents use about 4× the tokens of chat, and multi-agent systems about 15×. The approach is a poor fit when agents must share a lot of context, which the authors say covers most coding.
- Early failures included spawning 50 subagents for simple queries, endless searching and duplicated work. Prompting fixed most:
  - Watch agents step by step with the real prompts and tools.
  - Give each delegated task an objective, output format, tool guidance and boundaries.
  - Scale effort to the query: 1 agent with 3–10 tool calls for a simple fact, 2–4 subagents with 10–15 calls each for comparisons, more than 10 subagents for complex research.
  - Give each tool a distinct purpose and a clear description. A tool-testing agent that rewrote flawed tool descriptions cut later task time by 40%.
  - Start with broad queries, then narrow them. Use extended thinking to plan.
  - Parallelize: the lead runs 3–5 subagents at once, and each uses 3+ tools at once. This cut research time by up to 90% on complex queries.
- Evals: start with about 20 real queries, since early effects are large. One LLM-judge call with a rubric (factual accuracy, citations, completeness, source quality, tool efficiency) returning 0.0–1.0 scores plus pass/fail matched humans best. Humans still caught agents preferring SEO content farms to authoritative sources.
- Production: errors compound, so resume from checkpoints and tell the agent when a tool fails. Trace decision patterns, not conversation content. Use **rainbow deployments** so running agents aren't broken mid-task. Synchronous subagent batches are a bottleneck.
- Appendix: grade state-changing agents on end state. Summarize finished phases into external memory. Have subagents write outputs to files and return references.

## What to do with it

- Use multi-agent setups for wide, independent subtasks that overflow one context, not tightly coupled work.
- Write delegation prompts as task briefs with an effort budget per query type.
- Let a model test and rewrite your tool descriptions.
- Start evals with about 20 real cases and an LLM judge, plus human review.
- Build resumability, tracing and version-safe deploys before scaling.

## Terms

- **Rainbow deployment** — gradually shifting traffic between versions running side by side.
- **End-state evaluation** — grading the final state, not the path taken.

## Caveats

- Mid-2025, Claude 4-era models; the token-versus-model findings may have shifted. The 90.2% comes from an unpublished internal eval.
- Anthropic sells Claude and the Research feature.
- File-based handoffs and durable state recur in later posts on [long-running harnesses](2025-11-26-anthropic-harnesses-long-running-agents.md) and [Managed Agents](2026-04-08-anthropic-managed-agents.md).
