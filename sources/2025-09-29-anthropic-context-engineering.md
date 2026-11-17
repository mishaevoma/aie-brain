---
type: source
title: "Effective context engineering for AI agents"
author: "Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield"
publisher: Anthropic
url: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
published: 2025-09-29
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, instruction-files, memory, multi-agent-systems, retrieval, tool-design]
---

# Effective context engineering for AI agents

**In one line:** treat the context window as a scarce attention budget, and at every step of the agent loop fill it with the smallest set of high-signal tokens that makes the desired outcome likely.

## What it says

- **Context engineering** is presented as the successor to prompt engineering: not just writing instructions, but curating everything the model sees each turn (system prompt, tools, MCP, external data, message history). Agents generate new candidate context every loop, so curation is continuous.
- **Context rot**: needle-in-a-haystack studies show recall falls as context grows, in every model. Reasons given: n² pairwise attention, training data skewed to shorter sequences, and position-encoding interpolation. The decline is gradual, not a cliff.
- **System prompts** should sit at the "right altitude", between brittle hard-coded if-else logic and vague guidance that assumes shared context. Organize them into sections with XML tags or Markdown headers. Start with a minimal prompt on the best model, then add instructions and examples only for failures you observe. Minimal does not mean short.
- **Tools** should be self-contained, error-robust, distinct and economical in output. If a human engineer couldn't say which tool applies, neither can the agent.
- **Examples**: use a few diverse, canonical examples rather than long lists of edge-case rules.
- **Just-in-time retrieval**: the agent keeps lightweight references (paths, queries, links) and loads data through tools when needed, using metadata such as folder names, file names, sizes and timestamps to decide what to open. This is **progressive disclosure**. It is slower than loading everything up front and depends on good tools. Claude Code mixes the two: CLAUDE.md is loaded up front, and files are found with glob and grep on demand. The advice is to do the simplest thing that works.
- **Long-horizon tasks** need three techniques:
  - **Compaction**: summarize the history when it nears the limit, then continue. Claude Code keeps architectural decisions, unresolved bugs and implementation details, drops redundant tool output, and carries forward the five most recently accessed files. Tune the summary for recall first, then for precision. The lightest form is clearing old tool results, which is now a Claude Developer Platform feature.
  - **Structured note-taking**: the agent saves notes outside the context window (to-do lists, a NOTES.md file) and reads them back after a reset. Claude playing Pokémon kept tallies, maps and strategies across thousands of steps. A file-based memory tool entered public beta with the Sonnet 4.5 launch.
  - **Sub-agents**: each explores in a clean context, possibly using tens of thousands of tokens, and returns a condensed summary of about 1,000–2,000 tokens to a coordinating agent.
- Which to use: compaction for long back-and-forth, notes for milestone-driven work, sub-agents for research that benefits from parallel exploration.

## What to do with it

- Audit what fills context each turn and cut low-signal tokens: stale tool output, overlapping tools, rule lists.
- Grow the system prompt from observed failures, not imagined edge cases.
- Give agents references and search tools instead of pre-loading whole corpora.
- For long tasks, design in compaction, notes or sub-agents, and test that summaries keep what later steps need.

## Terms

- **Context engineering** — curating the full token state the model sees at each inference step.
- **Context rot** — falling recall and reasoning precision as the context grows.
- **Attention budget** — each added token spends part of a limited capacity to attend.

## Caveats

- Written by Anthropic's Applied AI team. It promotes Claude Developer Platform features (tool result clearing, the memory tool) and uses Claude Code as its running example.
- Model and feature status reflect September 2025. The article itself expects less hand-engineering as models improve.
- The context-rot evidence comes from outside research (Chroma), not measured here.
- It updates the pre-computed retrieval view of the 2024-09-19 contextual retrieval note by favoring hybrid and just-in-time approaches for agents. The 2025-11-04 and 2025-11-24 notes apply the same ideas to tools.
