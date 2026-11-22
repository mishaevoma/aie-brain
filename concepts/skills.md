---
type: concept
title: "Skills"
updated: 2026-11-22
reviewed: 2026-11-17
status: evolving
---

# Skills

**Definition:** A skill is a folder with a `SKILL.md` (a name, a description and instructions) plus optional scripts and reference files. The agent sees only the name and description until a task needs the rest.

## Why it matters

Skills let a general agent carry a large amount of procedural know-how without paying for it in every session. They are the main alternative to an ever-growing instruction file. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)

## How loading works

Three levels of progressive disclosure [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md):

1. At start, only each skill's name and description are in context.
2. When a skill looks relevant, the agent reads its `SKILL.md`.
3. Linked files and scripts are opened only if the task needs them.

## What to do

- Write the description as a trigger condition, then test that the skill fires when it should. The description decides relevance. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md) · [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Start from where the agent struggles, found through evals or use, not from a list of topics. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- Put deterministic steps such as parsing, extraction and sorting in bundled scripts. Code is cheaper and more reliable than generating the result token by token. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- Write down the procedures that are passed from colleague to colleague: how a task is done properly at this company. A background curator can draft them from traces of how people use the agents. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- Use a skill for data access guidance: which system holds what and how to query it. Do not copy data that already has a current source of truth. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- Write steps in tool-neutral terms ("run linting") and teach only what is specific to the project. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Keep `SKILL.md` short and move reference material into linked files. Say whether a script is to be run or read. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- Store skills in `.agents/skills/` and link them for tools that look elsewhere. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Lütke, Aug 2026](../sources/2026-08-25-lutke-agents-md-split-brain.md)
- Make a `verify` skill first: how to start, drive and inspect the app. Keep it fast and reliable. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Attach a feedback loop to skills that encode taste, making each a compounding skill. Save corrected outputs as gold cases, turn the corrections into yes/no checks, and iterate the skill against them in a clean context on more than one model. [Shipper, Nov 2026](../sources/2026-11-15-shipper-compounding-skills.md)
- Prune. Each installed skill's description costs context in every session. Remove the ones you do not use. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md) · [Theo, Jul 2026](../sources/2026-07-28-theo-rewriting-agents-md-by-hand.md)
- Review third-party skills like third-party code, including scripts and network calls. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)

## How skills relate to the rest

- MCP connects an agent to tools. Skills teach workflows that use those tools. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- An agent can save code it wrote as a skill for next time. [Code execution with MCP, Nov 2025](../sources/2025-11-04-anthropic-code-execution-with-mcp.md)
- Sharing across repositories goes through plug-ins and marketplaces, and the mechanics differ per tool. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)

## What is changing

- Agent Skills became an open standard in December 2025, and the discovery location is converging on `.agents/skills/`, though not every tool reads it. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md) · [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Users expect skills to follow them between harnesses, and are surprised when they do not. [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md)
- Skills are described as the settled format for procedural memory, the how-to part. For facts and definitions no format is agreed. One candidate named is Open Knowledge Format (OKF). [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

## Related

[Context layer](context-layer.md) · [Instruction files](instruction-files.md) · [MCP](mcp.md) · [Verification](verification.md) · [Compounding](compounding.md) · [Knowledge factory](knowledge-factory.md)
