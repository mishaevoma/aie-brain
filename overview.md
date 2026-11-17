# Overview

The mental model this brain works from, as of 17 November 2026. It is a synthesis of the pages it links to. When a concept page changes the picture, update this page too.

## The stack

Five layers, and three things that cut across them. Use these names when deciding where a problem or a change belongs.

| Layer | What it is | Who changes it | Page |
|---|---|---|---|
| Product | What the user is actually getting done | You | [Building an agent product](playbooks/building-an-agent-product.md) |
| Interface | Where a person meets the agent: CLI, app, chat | You or a vendor | [Harness](concepts/harness.md) |
| Context layer | Instruction files, skills, MCP servers, memory | You | [Context layer](concepts/context-layer.md) |
| Harness | Loop, tools, context management, gate, sandbox | A vendor, or you | [Harness](concepts/harness.md) |
| Model | The weights | A lab | |

Across all of them:

- **Checking**: [verification](concepts/verification.md) while the work happens, [evals](concepts/evals.md) across many runs.
- **Containment**: [permissions and sandboxing](concepts/sandboxing-and-permissions.md).
- **People**: [human judgment](concepts/human-judgment.md).

## What the sources agree on

1. **Start simple.** One good model call before a workflow, a workflow before an agent, an existing harness before your own. [Agents and workflows](concepts/agents-and-workflows.md)
2. **Context is a budget.** Load little, load on demand, and keep what is always loaded short. [Context engineering](concepts/context-engineering.md)
3. **Tools are written for a model.** Few, task-shaped, described like a briefing, and tested with evals. [Tool design](concepts/tool-design.md)
4. **Short instruction file, procedures in skills.** [Instruction files](concepts/instruction-files.md), [Skills](concepts/skills.md)
5. **Files first for knowledge and memory.** Add search or a database when the files stop being enough. [LLM wiki](concepts/llm-wiki.md), [Memory](concepts/memory.md)
6. **Verification is the bottleneck.** Give the agent a way to run the real thing, and accept evidence, not summaries. [Verification](concepts/verification.md)
7. **A deterministic boundary under any model-based gate.** [Permissions and sandboxing](concepts/sandboxing-and-permissions.md)
8. **Scaffolding expires.** Each piece is a bet on what the model cannot do yet. Re-test at every model release. [Harness](concepts/harness.md), [Long-running agents](concepts/long-running-agents.md)
9. **Evals start small and from real failures, and small gaps between scores mean little.** [Evals](concepts/evals.md), [Trusting eval numbers](concepts/eval-validity.md)
10. **Encode corrections, then prune.** [Compounding](concepts/compounding.md)
11. **Intent and accountability stay with a person.** [Human judgment](concepts/human-judgment.md)

## Live debates

- **Does the harness matter?** Barely, for choosing between mature coding harnesses [Theo video, 30 Oct 2026](sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md). Decisively, for whether a run is useful and safe [Loams, Oct 2026](sources/2026-10-18-loams-coding-agent-harnesses.md). A lot, but temporarily, for long tasks [Harness design, Mar 2026](sources/2026-03-24-anthropic-harness-design-long-running-apps.md). See [Harness](concepts/harness.md).
- **Compaction or a full log?** Summarise history inside the window [Context engineering, Sep 2025](sources/2025-09-29-anthropic-context-engineering.md), or keep everything outside and choose slices at read time [Managed Agents, Apr 2026](sources/2026-04-08-anthropic-managed-agents.md). See [Context engineering](concepts/context-engineering.md).
- **Many agents for coding?** A poor fit in 2025 [Multi-agent research system, Jun 2025](sources/2025-06-13-anthropic-multi-agent-research-system.md). Working at scale in 2026 where the checks are strong and the work separates [C compiler, Feb 2026](sources/2026-02-05-anthropic-building-c-compiler.md) · [Osmani, 17 Nov 2026](sources/2026-11-17-osmani-claude-code-team-verification.md). See [Multi-agent systems](concepts/multi-agent-systems.md).
- **Write more down or less?** Encode nearly all domain knowledge [Cherny, 15 Jul 2026](sources/2026-07-15-cherny-automation-is-the-highest-leverage.md), and keep the always-loaded file small [Red Hat, Jul 2026](sources/2026-07-27-redhat-agents-md-and-agent-skills.md). See [Instruction files](concepts/instruction-files.md).
- **When should memory be written?** During the task or in an offline pass, and how often to re-verify it [Agent memory, Nov 2026](sources/2026-11-06-anthropic-components-of-agent-memory.md) · [Chase, Apr 2026](sources/2026-04-04-chase-continual-learning-for-ai-agents.md). See [Memory](concepts/memory.md).
- **Evals from day one?** Yes, a few dozen tasks [Demystifying evals, Jan 2026](sources/2026-01-09-anthropic-demystifying-evals.md). Or dogfood first [Google, Sep 2026](sources/2026-09-09-google-anatomy-of-harness-engineering.md). See [Evals](concepts/evals.md).

## How the picture moved

- **Late 2024.** Simple patterns over frameworks; workflows versus agents. Retrieval as a pipeline built in advance. [Building effective agents, Dec 2024](sources/2024-12-19-anthropic-building-effective-agents.md) · [Contextual Retrieval, Sep 2024](sources/2024-09-19-anthropic-contextual-retrieval.md)
- **2025.** Tool interfaces get the attention. Context engineering is named. Skills, code execution with MCP and tool search arrive to keep context small. Sandboxing replaces per-action prompts. [Writing tools for agents, Sep 2025](sources/2025-09-11-anthropic-writing-tools-for-agents.md) · [Context engineering, Sep 2025](sources/2025-09-29-anthropic-context-engineering.md) · [Agent Skills, Oct 2025](sources/2025-10-16-anthropic-agent-skills.md) · [Code execution with MCP, Nov 2025](sources/2025-11-04-anthropic-code-execution-with-mcp.md) · [Advanced tool use, Nov 2025](sources/2025-11-24-anthropic-advanced-tool-use.md) · [Claude Code sandboxing, Oct 2025](sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- **Early 2026.** Eval practice and its pitfalls are written down. Harnesses for multi-hour work get planners and evaluators, then lose parts as models improve. Classifiers take over routine approvals. [Demystifying evals, Jan 2026](sources/2026-01-09-anthropic-demystifying-evals.md) · [Infrastructure noise, Feb 2026](sources/2026-02-05-anthropic-infrastructure-noise.md) · [Eval awareness, Mar 2026](sources/2026-03-06-anthropic-eval-awareness-browsecomp.md) · [Harness design, Mar 2026](sources/2026-03-24-anthropic-harness-design-long-running-apps.md) · [Auto mode, Mar 2026](sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- **Spring 2026.** The LLM wiki pattern spreads. Learning is described as model, harness and context layers. Hosted agents split into session log, harness and sandbox. A harness-level regression gets a public postmortem. [Karpathy, 2 Apr 2026](sources/2026-04-02-karpathy-llm-knowledge-bases.md) · [Chase, Apr 2026](sources/2026-04-04-chase-continual-learning-for-ai-agents.md) · [Managed Agents, Apr 2026](sources/2026-04-08-anthropic-managed-agents.md) · [Claude Code postmortem, Apr 2026](sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- **Summer 2026.** Pruning becomes a product feature. `AGENTS.md` and `.agents/skills` become the expected shared locations. [Cherny, 9 Jul 2026](sources/2026-07-09-cherny-checkup.md) · [Lütke, Aug 2026](sources/2026-08-25-lutke-agents-md-split-brain.md) · [Red Hat, Jul 2026](sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- **Autumn 2026.** Agents write most of the code at some companies, and the limits move to source control and review. "Harness" gets precise definitions and an argument about whether it still matters. Memory gets layers and an offline pass. Verification is described as a system of its own. [Source control, Oct 2026](sources/2026-10-13-anthropic-redesigning-source-control.md) · [Theo, 22 Oct 2026](sources/2026-10-22-theo-what-is-a-harness.md) · [Loams, Oct 2026](sources/2026-10-18-loams-coding-agent-harnesses.md) · [Agent memory, Nov 2026](sources/2026-11-06-anthropic-components-of-agent-memory.md) · [Osmani, 17 Nov 2026](sources/2026-11-17-osmani-claude-code-team-verification.md) · [Osmani, 3 Nov 2026](sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

## What this brain does not cover yet

- Most sources are from Anthropic or from people who build on Claude. Guidance from other labs is nearly absent.
- Most figures were measured on Anthropic's models and products: memory gains, approval rates, classifier miss rates, retrieval failure rates. Read them as a direction, and measure again on the model you run.
- Nothing on fine-tuning, voice or multimodal products, cost and pricing, or product and interface design for AI features.
- Coding agents dominate. Other verticals appear only as examples.

A review of a product design against this brain on 17 November 2026 found four more gaps:

- Durable execution for tasks that wait on a person or must survive a restart: workflow engines, retries, writes that are safe to repeat. [Long-running agents](concepts/long-running-agents.md) covers the agent's side only.
- Serving many customers from one product: keeping tenants apart, data residency, limits per customer.
- Model gateways: routing, falling back to another model, and what a silent fallback does to eval results.
- Agents that operate an existing application through its interface: browser and computer use, and tools a page declares for the agent.

Leads for filling these gaps are in the [watchlist](watchlist.md).
