---
type: concept
title: "Harness"
updated: 2026-11-17
reviewed: 2026-11-17
status: contested
---

# Harness

**Definition:** The software around a model that turns its text into actions. It builds the context, defines the tools, decides which tool calls run, runs them, feeds the results back and keeps everything inside the context window. Model plus harness is an agent. A harness is not the interface a person uses, and it is not the configuration loaded into it.

## The four layers

Use these words for these things. Most confusion about "the harness" comes from mixing them.

| Layer | What it is | Who changes it |
|---|---|---|
| Model | The weights | The lab |
| Harness | Loop, tools, context management, permission gate, sandbox | The harness vendor, or you if you build one |
| [Context layer](context-layer.md) | Instruction files, skills, MCP servers, memory | You |
| Interface | The CLI, app or chat surface a person uses | The product |

The model, harness and context split is from [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md). The interface distinction is from [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md): Claude Code is an interface that bundles a harness, the Agent SDK. An app that sits above several harnesses and manages agent work has been called an agentic development environment (ADE). [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md)

## What is inside a harness

A teardown of eight coding harnesses finds the same parts in each [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md):

- **Loop**: call the model, run tool calls, feed results back.
- **Gate**: permission modes and approvals. See [permissions and sandboxing](sandboxing-and-permissions.md).
- **Sandbox**: what an action can reach.
- **Compaction**: rewriting context near the limit. See [context engineering](context-engineering.md).
- **Edit format**: how the model changes files. See [tool design](tool-design.md).
- **Undo**: checkpoints, shadow repos or worktrees.
- **MCP client and subagents.**

Definitions vary in width. The narrow one is tools, a call syntax, an executor and a result path [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md). The wide one is everything in a coding agent except the model [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md). The barest comes from product builders: a prompt, a switch statement over the model's structured output, the accumulated context and a loop [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md). In eval vocabulary the *agent harness* is the scaffold under test, and the *evaluation harness* is what runs and scores the tasks [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md). Building and tuning this layer, including testing how it behaves, is called *harness engineering* [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md).

## What to do

- Adopt before you build. Reconfigure an existing harness with tools, instructions and MCP servers before writing infrastructure. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md)
- Own the loop where a harness or framework will not let you edit the exact prompt, shape what the model sees, and pause between the choice of a tool and its execution. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Treat each harness feature as a bet on something the model cannot yet do. At every model release, remove scaffolding one piece at a time and keep only what still carries load. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Gate harness changes with the same evals as a model change. Lower default effort, a bug that cleared reasoning, and one terse-output prompt line degraded Claude Code in March and April 2026 while the model was unchanged. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Name the harness next to any benchmark score. The score belongs to the model plus its scaffold. [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)
- Test harness behaviour with small behavioural evals, not only end-to-end benchmarks. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)
- If you host agents, fix the interfaces between session log, harness and sandbox, not one particular loop, so each part can be replaced as models change. Anthropic calls this a meta-harness. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)

## Where sources disagree: does the harness matter?

- **Barely.** For the same model, one builder puts the gap between mature coding harnesses at 3 to 5 percent, notes that labs train each model on their own harness, and observes that users no longer notice which harness they are using. [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md) · [Theo, 9 Nov 2026](../sources/2026-11-09-theo-harness-difference-approaching-zero.md)
- **It is the product.** The harness, not the model, decides whether a run is useful and safe. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- **Own it.** Builders of customer-facing features took a framework to 70-80% quality, found that too low, and rebuilt, because improving meant reverse-engineering the framework's prompts and control flow. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- **It matters and it expires.** Harness design changed the outcome of multi-hour builds, yet the pieces that mattered for one model generation were removed for the next. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md) · [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)

This brain's reading, which is a synthesis and not a source claim: they are answering different questions. Which mature coding harness you choose for a given model matters little. How a harness you build handles context, verification and containment matters a lot, until the next model makes part of it unnecessary. What you configure into the harness is where your own effort pays most, and it moves with you. The 2025 case for owning the loop is about the loop inside your own product's feature, and the 2026 advice to adopt is about general coding harnesses. The loud voices have a stake: one builds a layer above harnesses, another sells one, and a third sells tooling for the loop you own.

## Related

[Context layer](context-layer.md) · [Agents and workflows](agents-and-workflows.md) · [Long-running agents](long-running-agents.md) · [Evals](evals.md) · [Running agents in production](production-operations.md)
