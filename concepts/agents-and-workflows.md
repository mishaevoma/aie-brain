---
type: concept
title: "Agents and workflows"
updated: 2026-11-22
reviewed: 2026-11-17
status: settled
---

# Agents and workflows

**Definition:** A *workflow* wires model calls and tools together along code paths you define. An *agent* is a model running in a loop that chooses its own steps and tool calls until the task is done. An agent is a model plus a [harness](harness.md).

## Why it matters

Choosing between a single call, a workflow and an agent is the first design decision in an AI product. It sets cost, latency and how far an error can spread before anyone notices.

Errors also multiply along the way. At 95% accuracy per step, a task of 10 steps succeeds 60% of the time and one of 100 steps 0.6%. That is arithmetic, assuming independent steps and no recovery, not a measurement. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md)

## What to do

- Start with one model call that has retrieval, tools and examples (the *augmented LLM*). Add structure only when measurement shows a gain. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Pick the least autonomous pattern that solves the task. Workflows suit well-defined tasks where predictability matters. Agents suit open-ended ones. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Mix the two when only part of the path is open. Keep the known steps in code and put a short agent loop, a micro agent, where the route depends on feedback such as a person's reply or a failed call. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Know the five workflow patterns before inventing one: prompt chaining, routing, parallelization (sectioning or voting), orchestrator-workers, evaluator-optimizer. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Keep the loop simple. The model emits text or a tool call. Text ends the turn. A tool call is checked, run, and its result fed back. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md)
- Give every agent stop conditions and points where a person can step in: iteration caps, and loop breakers such as stopping after three identical calls. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Check a plan before it runs when a wrong one is expensive: reject plans that name a tool the agent lacks or run past a step limit, or have a model judge them. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md)
- Mix the two in one coded workflow when some steps must always happen. Write linting, pushing and CI as fixed steps, and give the agent the steps that need judgment. Stripe does this to guarantee the required steps and to save tokens. Dropbox found that an agent left to wait for its own CI held a session for hours or validated against the wrong tests. [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md) · [Dropbox, May 2026](../sources/2026-05-21-dropbox-introducing-nova.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md)
- Try a thin scaffold first. A short prompt, a shell tool and an edit tool were state of the art on SWE-bench Verified in early 2025. [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)
- Do not use an agent for every model call. Small generation jobs such as titles and commit messages can go straight to a model API. [Theo, 9 Nov 2026](../sources/2026-11-09-theo-harness-difference-approaching-zero.md)
- Expect agents to fit best where success can be checked and a person can oversee. Coding and customer support were the first examples. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- If you adopt a framework, read what it actually sends. Frameworks speed up the start and hide the prompts and responses. Check first that you can edit the exact prompt and pause between the choice of a tool and its execution. One builder saw teams reach 70-80% quality on a framework and then start over, because improving it meant reverse-engineering its prompts and control flow. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) · [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)

## Where sources differ

- **What counts as an agent.** One wider definition takes in anything that senses an environment and acts on it through tools, ChatGPT and RAG pipelines included. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md) Another calls a mostly deterministic product with a short loop inside it an agent. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md) This brain's reading: keep the narrow sense, because the split between workflow and agent is what the design decision turns on.
- **A thin loop, or structure around it.** A short prompt with a shell tool and an edit tool topped a coding benchmark in early 2025. [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md) In the same months, builders of customer-facing features reported that a plain loop over a prompt and a bag of tools broke down past 10-20 turns, and that 90% success was not enough to ship. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md) A design of that time kept planning apart from execution, with a validator between them. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md) The yardsticks differ: one is a benchmark score, the other the reliability a customer-facing feature needs.

## What is changing

- The framing from [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) still holds, but default harnesses now ship planning, subagents and compaction. "Building an agent" increasingly means configuring an existing harness with tools, instructions and MCP servers. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md) See [context layer](context-layer.md).
- For work that runs for hours, the workflow patterns come back as roles: planner, generator, evaluator. See [long-running agents](long-running-agents.md).
- Production systems now sit between the two. One company calls its version a *blueprint*: a workflow whose nodes are either fixed code or an agent loop. [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md) An agent cut into recorded steps can also be paused, approved and resumed midway, which a single loop in memory cannot. [Building LangGraph, Sep 2025](../sources/2025-09-04-langchain-building-langgraph.md) See [durable execution](durable-execution.md).

Suh proposes that agents write durable workflows per tenant on the platform that already connects API and MCP data, combining deterministic steps with agent loops. He favours code over drag-and-drop automation. This brain's reading is that authoring the workflow and executing it are separate decisions. Generated workflow code still needs the [durability](durable-execution.md) and [side-effect](side-effects.md) controls of any deployed workflow. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md)

## Related

[Harness](harness.md) · [Tool design](tool-design.md) · [Multi-agent systems](multi-agent-systems.md) · [Long-running agents](long-running-agents.md) · [Durable execution](durable-execution.md) · [Background agents](background-agents.md)
