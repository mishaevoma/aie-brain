---
type: concept
title: "Memory"
updated: 2026-11-17
reviewed: 2026-11-17
status: evolving
---

# Memory

**Definition:** Knowledge an agent gains from experience and keeps across sessions as readable context. It is not weight updates and it is not the current context window.

## Why it matters

Each session starts blank. Memory is how an agent stops repeating a mistake, and it is the form of "learning" you can add without training a model. On Anthropic's CL-Bench 1.0, a task with fresh sessions and a memory folder, its recent models improved sharply: Opus 5.5 went from 0.655 to 0.838 mean reward. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)

## The layers

From bottom to top [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md):

1. **Transcripts**: the searchable record of what happened. Ground truth.
2. **Notes**: what the agent chose to write down.
3. **Representations**: structured artefacts built from notes and transcripts, such as a [wiki](llm-wiki.md).
4. **Injected context**: the small part loaded into every session.

**Dreaming** is an offline pass that moves information between layers: it corrects notes against transcripts, builds representations, and promotes what matters. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)

## Design choices

- **When to write**: while working (hot-path memory), or offline over recent traces. [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)
- **Who decides**: the user says "remember this", or the agent decides on its own. [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)
- **Scope**: one agent, one user, a team or an organisation, or several at once. [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)

## What to do

- Keep full transcripts or traces. Every kind of learning depends on a record of what the agent did, and notes need something to be checked against. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Give a capable model a memory folder and say what memory is for. Do not prescribe rigid rules: a "record only failures" rule cut the benefit sharply. Older models need explicit steps instead. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Run an offline pass that checks notes against the record. One wrong note kept trapping an agent until it was corrected. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Keep the always-loaded layer to a short index. Preloaded notes cost tokens and spread their errors. Claude Code loads only the first 200 lines or 25 KB of its memory index. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Select what to recall instead of replaying the whole history. On a chat-memory benchmark, models from four vendors all answered better from the relevant parts than from the full history. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- Use files before a memory product. [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md)
- For long tasks, have the agent keep working notes outside the window and read them back after a reset. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Give each concurrent writer its own page. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)

## Risks and open questions

- Memory can be poisoned: instruction files, memory files and state directories are all read back as trusted context. This is listed as an open problem. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- A model's judgement of what is worth keeping has improved a great deal. An older Claude model, Sonnet 3.7, accumulated 413 files and spent its steps on upkeep, where a recent one, Claude Fable 5, kept 10 small ones and got further. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Every figure on this page was measured on Anthropic's models, on tasks Anthropic chose. In those tests the newest models wrote useful notes unaided, and an older one gained little until it was given explicit steps. Where another vendor's models fall is not measured in these sources, so test the model you run before trusting it to decide what to keep. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Still open: whether to write during the task or afterwards, how often to re-verify, and what maintaining representations costs in tokens and errors. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)

## Related

[LLM wiki](llm-wiki.md) · [Context layer](context-layer.md) · [Context engineering](context-engineering.md) · [Compounding](compounding.md)
