---
type: source
title: "How to Fix Your Context"
author: "Drew Breunig"
publisher: dbreunig.com
url: https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html
published: 2025-06-26
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, tool-design]
---

# How to Fix Your Context

**In one line:** A long context fails in four named ways, and six named tactics keep it small and clean, because every token in the window sways the answer.

## What it says

- Four failure modes, recapped from the author's earlier post. **Context poisoning:** an error or hallucination enters the context and keeps being referenced. **Context distraction:** the context is so long that the model leans on it and neglects its training. **Context confusion:** superfluous content lowers the quality of the response. **Context clash:** new information or tools conflict with what is already there.
- **RAG:** add only the relevant information. A larger window does not retire it, because junk in the context still shapes the response.
- **Tool loadout:** load only the tool definitions the task needs. In the "RAG MCP" paper, tool selection became critical for DeepSeek-v3 above 30 tools, and beyond 100 the model was almost certain to fail the test. Retrieving fewer than 30 gave up to 3x better tool selection accuracy. In the "Less is More" paper, Llama 3.1 8b failed a benchmark with 46 tools and passed with 19, and choosing tools dynamically raised its Berkeley Function Calling Leaderboard score by 44%.
- **Context quarantine:** give isolated subtasks their own threads and contexts, as Anthropic's multi-agent research system does. It suits work that parallelises, not problems where agents must share context.
- **Context pruning:** remove what is no longer needed. Provence, a 1.75 GB pruning model, cut 95% of a Wikipedia article and kept the part that answered the question. Hold the context as structured data and compile the prompt before each call, so instructions survive while documents and history are pruned.
- **Context summarization:** condense what has accrued. It also counters distraction: a Pokémon-playing agent on Gemini 2.5 Pro repeated past actions instead of planning once its context grew well past 100,000 tokens. It is easy to add and hard to get right, so make it a stage of its own and collect eval data on it.
- **Context offloading:** keep notes outside the context through a tool, such as Anthropic's "think" tool, which the author would rather call a scratchpad. Anthropic reported up to a 54% improvement on a benchmark when it was paired with a domain-specific prompt.

## What to do with it

- Ask of every part of the context whether it is earning its place.
- Count your tools. Past a few dozen, choose a loadout per task, and expect small models to struggle much earlier.
- Assemble the context from structured parts in code, so each part can be pruned, summarised or dropped on its own.
- Give the agent a scratchpad.

## Terms

- **Tool loadout** — the set of tool definitions chosen for a task. The word comes from games.
- **Context quarantine** — isolating a context in its own thread.
- **Context offloading** — storing information outside the context through a tool.

## Caveats

- June 2025, and a synthesis: the figures come from the cited papers and posts (DeepSeek-v3, Llama 3.1 8b, Gemini 2.5 Pro, Claude), not from tests by the author. The Gemini observation is called anecdotal at its source.
- The tool counts are for models of early 2025. Choosing a loadout has since moved into the API as [deferred tool loading](2025-11-24-anthropic-advanced-tool-use.md).
