---
type: concept
title: "Context layer (harness configuration)"
updated: 2026-11-17
status: evolving
---

# Context layer (harness configuration)

**Definition:** Everything you load into a harness to set it up for your project or product: instruction files, skills, MCP servers and memory. It sits outside the harness, it belongs to you, and it is the part that should move with you between tools. Also called harness configuration.

## Why it matters

It is the layer you control. You do not train the model and you rarely write the harness, but you decide what the agent knows about your work. It is also what "the agent learned something" usually means in practice. [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)

## The parts

| Part | Loaded | Use it for | Page |
|---|---|---|---|
| Instruction files | Every session | Short orientation, conventions, pointers | [Instruction files](instruction-files.md) |
| Skills | When a task needs them | Procedures and bundled scripts | [Skills](skills.md) |
| MCP servers | Tool definitions up front unless deferred | Access to outside systems and data | [MCP](mcp.md) |
| Memory | A small index always, the rest on demand | What the agent learned from experience | [Memory](memory.md) |

## Where does a piece of knowledge go?

- Needed in every session and short: instruction file.
- A procedure needed sometimes: skill.
- Checkable by a machine: lint rule, test or hook, not prose. See [compounding](compounding.md).
- Access to another system: MCP server or a command-line tool.
- Learned by the agent while working: memory.

## What to do

- Keep one source of truth in vendor-neutral locations (`AGENTS.md`, `.agents/skills/`), with tool-specific files as pointers. Different tools reading different files splits a team's context. [Lütke, Aug 2026](../sources/2026-08-25-lutke-agents-md-split-brain.md) · [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Write down the domain knowledge that lives in people's heads. Aim for an agent that can work in the codebase with no extra context from the person prompting. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
- Prune on a routine. Unused skills, MCP servers and stale rules cost context in every session. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md) · [Theo, Jul 2026](../sources/2026-07-28-theo-rewriting-agents-md-by-hand.md)
- Decide the scope of anything learned: one agent, one user, a team or the whole organisation. [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)
- Treat this layer as attack surface. Its files are loaded into the prompt by design, so opening a repository means trusting its authors. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

## What is changing

- Users switch harnesses and expect their skills and instructions to follow. Tools that sit above several harnesses are being asked to manage this layer. [Theo, 29 Oct 2026](../sources/2026-10-29-theo-harness-configuration-question.md) · [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md)
- Organisations are building one shared agent with common knowledge and connections instead of per-person setups. [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md)

## Related

[Harness](harness.md) · [Instruction files](instruction-files.md) · [Skills](skills.md) · [MCP](mcp.md) · [Memory](memory.md)
