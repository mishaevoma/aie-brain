---
type: concept
title: "Agents and workflows"
updated: 2026-11-17
reviewed: 2026-11-17
status: settled
---

# Agents and workflows

**Definition:** A *workflow* wires model calls and tools together along code paths you define. An *agent* is a model running in a loop that chooses its own steps and tool calls until the task is done. An agent is a model plus a [harness](harness.md).

## Why it matters

Choosing between a single call, a workflow and an agent is the first design decision in an AI product. It sets cost, latency and how far an error can spread before anyone notices.

## What to do

- Start with one model call that has retrieval, tools and examples (the *augmented LLM*). Add structure only when measurement shows a gain. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Pick the least autonomous pattern that solves the task. Workflows suit well-defined tasks where predictability matters. Agents suit open-ended ones. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Know the five workflow patterns before inventing one: prompt chaining, routing, parallelization (sectioning or voting), orchestrator-workers, evaluator-optimizer. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Keep the loop simple. The model emits text or a tool call. Text ends the turn. A tool call is checked, run, and its result fed back. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md)
- Give every agent stop conditions and points where a person can step in: iteration caps, and loop breakers such as stopping after three identical calls. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Try a thin scaffold first. A short prompt, a shell tool and an edit tool were state of the art on SWE-bench Verified in early 2025. [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)
- Do not use an agent for every model call. Small generation jobs such as titles and commit messages can go straight to a model API. [Theo, 9 Nov 2026](../sources/2026-11-09-theo-harness-difference-approaching-zero.md)
- Expect agents to fit best where success can be checked and a person can oversee. Coding and customer support were the first examples. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- If you adopt a framework, read what it actually sends. Frameworks speed up the start and hide the prompts and responses. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)

## What is changing

- The framing from [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) still holds, but default harnesses now ship planning, subagents and compaction. "Building an agent" increasingly means configuring an existing harness with tools, instructions and MCP servers. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md) See [context layer](context-layer.md).
- For work that runs for hours, the workflow patterns come back as roles: planner, generator, evaluator. See [long-running agents](long-running-agents.md).

## Related

[Harness](harness.md) · [Tool design](tool-design.md) · [Multi-agent systems](multi-agent-systems.md) · [Long-running agents](long-running-agents.md)
