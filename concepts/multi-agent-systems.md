---
type: concept
title: "Multi-agent systems"
updated: 2026-11-18
reviewed: 2026-11-17
status: evolving
---

# Multi-agent systems

**Definition:** Several agent instances working on one goal. The usual shapes are a lead agent that delegates to subagents with their own context windows (orchestrator-workers), and peers that coordinate through shared state such as a repository.

## Why it matters

More agents spend more tokens on a problem, in parallel, with each context kept clean. In Anthropic's study of its own research system, on Claude models of mid-2025, token use alone explained 80% of the variance in performance on the BrowseComp benchmark. The price is real: there, agents used about 4 times the tokens of a chat, and multi-agent systems about 15 times. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)

## When to use it

- Start with one agent and one continuous context. Every agent that acts without seeing the others' decisions is a place for those decisions to conflict. [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md)
- Use it for wide work with independent parts that would overflow one context. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Avoid it when the parts must share a lot of context. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Use a single subagent when the goal is simply a clean context for exploration or review: a well-defined question whose answer comes back as a summary. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md) · [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md) · [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md)

## What to do

- Write each delegation as a brief: objective, output format, tool guidance, boundaries. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Settle what has to agree before the work fans out: style, interfaces, naming. Workers in parallel cannot see each other's choices. [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md)
- Scale effort to the task. One system used one agent with 3 to 10 tool calls for a simple fact, 2 to 4 subagents for a comparison, and more than 10 for complex research. Without such budgets it spawned 50 subagents for simple queries. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Have subagents write results to files and return references or short summaries. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) · [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Try simple coordination first. Sixteen agents built a compiler with no orchestrator and no messaging, claiming tasks through lock files in git. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)
- Make the work separable. When every agent chased the same bug, a reference implementation used as an oracle split the problem. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)
- Separate the agent that builds from the agent that grades, where the task is beyond what the model does reliably alone. Below that line a grader only adds cost. See [long-running agents](long-running-agents.md). [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- Resume from checkpoints, because errors compound across agents. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Give a background subagent its own durable conversation and a handle, so that it can outlive the parent's turn, take follow-ups and wake the parent when it finishes. [Atlassian, Aug 2026](../sources/2026-08-26-atlassian-rovo-agent-harness.md) Or keep the call synchronous for the parent and suspend the parent's turn while it waits, so that it holds no server resources. [Linear, Aug 2026](../sources/2026-08-10-linear-how-we-built-linear-agent.md)
- Isolate subagents at the storage level, each with its own database or session, and let the lead agent start sessions and read their status through tools. [Project Think, Apr 2026](../sources/2026-04-15-cloudflare-project-think.md) · [Ramp, Jan 2026](../sources/2026-01-12-ramp-background-agent.md)

## Risks

- Subagent output re-entering the lead agent is a path for trust escalation. One permission system checks subagents at hand-off and again on return. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) · [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- A multi-agent setup reached benchmark answers by unintended routes 3.7 times as often as a single agent. [Eval awareness, Mar 2026](../sources/2026-03-06-anthropic-eval-awareness-browsecomp.md)
- Your capacity to review is the real limit. If finished work piles up faster than you can check it, more agents do not help. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- The systems around the agents become the bottleneck: source control, builds, review. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)

## Where sources disagree

Two articles from the same week of June 2025 give opposite advice, and a guide from that spring gives a third answer.

- **Keep one thread.** Subagents act on context the others cannot see, and their actions carry decisions that conflict. Rule out by default any design that allows either, and run a single linear agent, compressing its history when the task outgrows the window. [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md)
- **Fan out.** A lead agent with parallel subagents beat a single agent by 90.2% on an internal research eval, with Claude Opus 4 leading Claude Sonnet 4 subagents. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- **Small agents run by code.** Keep each agent to 3-10, maybe 20 steps, and let ordinary code, not a lead agent, run them one after another. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)

This brain's reading, which is a synthesis and not a source claim: the first two disagree less than their titles suggest. Both call work whose parts must share context a poor fit, and each argues from its own kind of task. Research subagents mostly read, and their findings merge as summaries. Coding subagents write, and every write is a decision the others have to live with. So ask whether the parallel parts make decisions that must agree. If they only gather information, fan out. If they build one thing together, keep one thread, or first fix what must agree in something every agent can check, as the compiler project below did with its tests. Small agents avoid the conflict only when they run in sequence and code carries the state between them. None of the three measured another's case, and all predate the results under "What is changing".

A single long thread also has a cost that none of them measured: a context gets less reliable as it grows, well before it is full. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)

## What is changing

In mid-2025 the advice was that most coding is a poor fit for multiple agents. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) · [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md) By 2026, teams of agents were building large systems, and one team says verification loops are what let a person run dozens or hundreds of agents instead of one or two. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md) · [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md) What changed was the checking around them: near-perfect test harnesses and verification loops, not more elaborate communication between agents. See [verification](verification.md).

An interface can also broker between harnesses, so that an agent in one harness starts a subagent in another through an MCP server. [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md)

## Related

[Agents and workflows](agents-and-workflows.md) · [Long-running agents](long-running-agents.md) · [Verification](verification.md) · [Context engineering](context-engineering.md) · [Agent platforms](agent-platforms.md) · [Background agents](background-agents.md)
