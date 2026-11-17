---
type: source
title: "Building effective agents"
author: "Erik S., Barry Zhang"
publisher: Anthropic
url: https://www.anthropic.com/research/building-effective-agents
published: 2024-12-19
ingested: 2026-11-17
kind: article
read: full
concepts: [agents-and-workflows, human-judgment, tool-design]
---

# Building effective agents

**In one line:** Start with the simplest thing that works, usually a single well-augmented LLM call, and move to fixed workflows or autonomous agents only when measurements show the extra cost and latency pay off.

## What it says

- The teams that succeeded with agents used small, composable patterns, not heavy frameworks.
- It splits "agentic systems" into **workflows** (LLMs and tools wired together along code paths you define) and **agents** (the LLM decides its own steps and tool use). Workflows suit well-defined tasks where predictability matters. Agents suit open-ended ones.
- The base unit is the **augmented LLM**: a model with retrieval, tools and memory, exposed through a clean, documented interface (MCP is given as one option).
- Five workflow patterns:
  - **Prompt chaining:** fixed sequential steps, with optional programmatic gates between them.
  - **Routing:** classify the input, then send it to a specialised prompt or model, e.g. easy questions to a small model and hard ones to a larger one.
  - **Parallelization:** either *sectioning* (independent subtasks run at once, such as a separate guardrail call) or *voting* (the same task run several times).
  - **Orchestrator-workers:** a central LLM decides the subtasks at runtime and merges the results.
  - **Evaluator-optimizer:** one model drafts, another critiques, in a loop. It fits when criteria are clear and feedback measurably helps.
- An agent is essentially an LLM calling tools in a loop, grounded by environment feedback such as tool output or test results at every step. It needs stopping conditions (e.g. an iteration cap) and checkpoints for human input. Autonomy raises cost and lets errors compound, so test in sandboxes with guardrails.
- Frameworks (Claude Agent SDK, Strands Agents SDK, Rivet, Vellum) speed up the start but hide prompts and responses. The advice is to begin with direct API calls and to understand any framework code you adopt.
- Agents fit best where conversation and action combine, success is checkable and humans can oversee. The two examples are customer support and coding (SWE-bench Verified).
- Appendix on tools: give tool definitions the same prompt-engineering care as prompts. Prefer familiar formats, leave room to think, avoid overhead like line counting or escaping. Make tools mistake-proof (**poka-yoke**): requiring absolute file paths ended the SWE-bench agent's relative-path errors.

## What to do with it

- Try a single call with retrieval and examples before building anything agentic.
- Pick the least autonomous pattern that solves the task, and add steps only when evals show a gain.
- Treat the **agent-computer interface (ACI)** as seriously as a human UI: clear parameter names, examples, edge cases, and testing with many inputs.
- Show the agent's plan to users and operators. Transparency is one of the three stated principles, with simplicity and well-tested tools.
- Give agents hard stop conditions and run them in sandboxes.

## Terms

- **Workflow vs agent** — predefined code paths vs model-directed control flow.
- **Augmented LLM** — a model plus retrieval, tools and memory.
- **ACI (agent-computer interface)** — the tool surface the model works through.
- **Poka-yoke** — designing tool arguments so mistakes are hard to make.

## Caveats

- Published December 2024. The page now carries a note that much of the tooling it describes has changed, and it points readers to the Managed Agents post (see [2026-04-08 note](2026-04-08-anthropic-managed-agents.md)).
- The page has been edited since publication. The routing example now names Claude Haiku 4.5 and Claude Sonnet 4.5, which did not exist in 2024.
- Anthropic sells the models and the Claude Agent SDK.
- Later Anthropic posts in this list build on this one: [orchestrator-workers at scale](2025-06-13-anthropic-multi-agent-research-system.md), and long-running harnesses that add planners and evaluators ([2026-03-24](2026-03-24-anthropic-harness-design-long-running-apps.md)).
