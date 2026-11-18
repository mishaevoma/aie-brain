---
type: concept
title: "Context engineering"
updated: 2026-11-17
reviewed: 2026-11-17
status: settled
---

# Context engineering

**Definition:** Deciding what the model sees at each step of the loop (instructions, tool definitions, retrieved data, history) so that the window holds the smallest set of high-signal tokens that makes the right outcome likely.

## Why it matters

Recall and reasoning get worse as the context grows, in every model. The decline is gradual, which makes it easy to miss. This is called context rot, and it is why context is treated as an attention budget, not free space. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)

The measurement behind the term is Chroma's, from July 2025. All 18 models tested, from Anthropic, OpenAI, Google and Alibaba, got less reliable as input grew, on tasks whose difficulty was held fixed. How much is lost depends on what the extra tokens are: passages on the right topic that do not answer the question, called distractors, cost more than unrelated filler. The report describes the loss as uneven across models and tasks, where the article above calls it gradual. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)

The name spread in June 2025 as a replacement for "prompt engineering", which most people had come to read as typing into a chatbot. [Willison, 27 Jun 2025](../sources/2025-06-27-willison-context-engineering.md) One agent builder calls it the main job of engineers who build agents. [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md)

## How a long context fails

Four names for what goes wrong, useful when reading a bad transcript. [How to fix your context, Jun 2025](../sources/2025-06-26-breunig-how-to-fix-your-context.md)

- **Context poisoning**: an error or hallucination gets into the context and keeps being referenced.
- **Context distraction**: the context is so long that the model leans on its history instead of reasoning afresh.
- **Context confusion**: superfluous content, such as tools the task does not need, lowers the quality of the response.
- **Context clash**: parts of the context contradict each other.

## What to do

**Every turn**

- Send the relevant parts, not everything that fits. On a chat-memory benchmark every model tested did better with about 300 relevant tokens than with the full history of about 113k tokens, and a thinking mode did not close the gap. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- Cut near-misses first. Stale versions of a fact and look-alike records do more harm than neutral filler. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- Audit what fills the window: stale tool output, overlapping tools and long rule lists are the usual waste. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Start with a minimal system prompt on the best model and add instructions only for failures you observe. Minimal does not mean short. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Build the context from structured parts in code and compile the prompt before each call. Then instructions and goals survive while documents and history are pruned or summarised. [How to fix your context, Jun 2025](../sources/2025-06-26-breunig-how-to-fix-your-context.md)
- Prefer a few varied, canonical examples to a list of edge-case rules. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Keep tool definitions and bulky results out of the window: defer tool loading, and process large data in code. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md) · [Code execution with MCP, Nov 2025](../sources/2025-11-04-anthropic-code-execution-with-mcp.md)

**Finding information**

- Give the agent references (paths, queries, links) and tools to load data when needed, instead of loading everything up front. This is just-in-time retrieval. A small always-loaded file plus on-demand search is the common mix. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Fetch in code what the model would almost certainly ask for, before the first model call, and leave the rest to be loaded on demand. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Disclose in layers: metadata first, body when relevant, linked files only if needed. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- A small body of reference material that nearly every request needs can go into the prompt whole instead. When each applies is on the [retrieval](retrieval.md) page, under "Where sources disagree". [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)

**Long tasks**

- Use compaction for long back-and-forth: summarise near the limit and continue. Tune the summary for recall first. Clearing old tool results is the lightest form. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Treat the summariser as a component of its own, and collect eval data on it. It is easy to add and hard to get right, and one team fine-tuned a smaller model for the job. [How to fix your context, Jun 2025](../sources/2025-06-26-breunig-how-to-fix-your-context.md) · [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md)
- Use structured notes for milestone work: the agent writes progress outside the window and reads it back. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Use subagents for exploration: each works in a clean context and returns a condensed summary of about 1,000 to 2,000 tokens, or writes to a file and returns a reference. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md) · [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)

## Risks

- Compaction is lossy and cannot be undone. Keep the full session log outside the window and choose what to load at read time. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Planted instructions can survive a summary. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Pruning has side effects. A bug that cleared earlier reasoning on every turn made an agent forgetful and repetitive. Test long and resumed sessions whenever you change what gets dropped. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Some models rush to finish as they near what they believe is the limit (context anxiety). Whether you need a full context reset or compaction is enough depends on the model. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- Chains of agents drift when each reads only the previous one's summary. Keep the original material reachable. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Whatever is always loaded costs tokens in every session and spreads its errors everywhere. Keep that layer to a short index. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)

## Related

[Retrieval](retrieval.md) · [Memory](memory.md) · [Tool design](tool-design.md) · [Instruction files](instruction-files.md) · [Long-running agents](long-running-agents.md)
