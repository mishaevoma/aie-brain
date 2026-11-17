---
type: source
title: "Introducing advanced tool use on the Claude Developer Platform"
author: "Bin Wu"
publisher: Anthropic
url: https://www.anthropic.com/research/advanced-tool-use
published: 2025-11-24
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, mcp, retrieval, tool-design]
---

# Introducing advanced tool use on the Claude Developer Platform

**In one line:** three beta API features address the main problems of large tool sets: search for tools instead of loading them all, let the model call tools from code so bulky results stay out of context, and add example calls to tool definitions.

## What it says

- **Tool Search Tool**
  - The problem: five common MCP servers (GitHub, Slack, Sentry, Grafana, Splunk; 58 tools) take about 55K tokens; Jira alone about 17K; Anthropic has seen 134K internally. Big sets also cause wrong picks between similar tools.
  - The fix: mark tools `defer_loading: true`. The model sees a search tool (regex or BM25, e.g. `tool_search_tool_regex_20251119`, or custom such as embeddings) and loads the 3–5 matching definitions on demand. Prompt caching survives because deferred tools sit outside the prefix. Whole MCP servers can be deferred via `mcp_toolset`.
  - The numbers: about 77K tokens of upfront context fall to about 8.7K, which the article calls an 85% reduction. MCP-eval accuracy rose from 49% to 74% for Opus 4, and from 79.5% to 88.1% for Opus 4.5.
  - When to use: more than 10K tokens of definitions, 10 or more tools, several MCP servers, or tool-selection errors. Skip it for small, compact tool sets used in every session.
- **Programmatic Tool Calling**
  - The model writes Python in the code-execution sandbox (`code_execution_20250825`) that calls your tools. Tools opt in with `allowed_callers`, and parallel calls are made with `asyncio.gather`. Intermediate results stay in the sandbox, and only the script's final output enters context.
  - Example: a budget check over 20 employees would otherwise put 2,000+ expense line items into context; the script returns only the few over budget.
  - The numbers: average tokens on complex research tasks fell from 43,588 to 27,297 (37%). Internal knowledge retrieval rose from 25.6% to 28.5%, "GIA" benchmarks from 46.5% to 51.2%. Claude for Excel uses it.
  - When to use: aggregating large data, three or more dependent calls, filtering, parallel fan-out. Not for single calls or when the model must see every result. Opt in only idempotent, parallel-safe tools, and document their return formats.
- **Tool Use Examples**
  - An `input_examples` array of realistic sample calls teaches conventions a JSON Schema cannot express: date formats, ID patterns, which optional fields go together. Complex-parameter accuracy rose from 72% to 90% internally.
  - Use 1–5 examples per tool, with real-looking data, covering minimal, partial and full variants. Skip them for simple tools.
- **Layering**: match the feature to the bottleneck. Use tool search for context bloat, programmatic calling for large intermediate results, and examples for parameter errors. Keep the 3–5 most-used tools always loaded, and describe the available tool categories in the system prompt.
- Access is through the beta header `advanced-tool-use-2025-11-20`.

## What to do with it

- Measure your tool-definition tokens. Over 10K, defer most tools and keep the core few loaded.
- Give tools clear, searchable names and descriptions, since retrieval depends on them.
- Move multi-step data processing into code, returning aggregates rather than raw records.

## Terms

- **Tool Search Tool** — a built-in tool that finds and loads deferred tool definitions on demand.
- **Programmatic Tool Calling** — the model orchestrates tool calls from code in a sandbox, so intermediate results bypass its context.

## Caveats

- These are beta features of Anthropic's paid API, with model names and type strings dated November 2025. Check the current docs.
- The article's token figures are not fully consistent: 77K to 8.7K is closer to an 89% cut than 85%, and a second pair of figures (191,300 vs 122,800 tokens of context preserved) does not obviously match the first.
- "GIA" is written as on the page; it may mean GAIA. The benchmarks are mostly internal.
- This note productizes the pattern from the 2025-11-04 code-execution note. Its token-efficiency advice builds on the 2025-09-11 tool-writing note.
