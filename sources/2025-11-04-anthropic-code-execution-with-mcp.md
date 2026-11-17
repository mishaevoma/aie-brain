---
type: source
title: "Code execution with MCP: Building more efficient agents"
author: "Adam Jones, Conor Kelly"
publisher: Anthropic
url: https://www.anthropic.com/research/code-execution-with-mcp
published: 2025-11-04
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, mcp, skills, tool-design]
---

# Code execution with MCP: Building more efficient agents

**In one line:** instead of loading every MCP tool definition and passing every result through the model, expose MCP servers as a code API and let the agent write code that calls them in a sandbox, so only the results it needs reach the context.

## What it says

- Two costs grow with the number of MCP servers. Most clients load every tool definition up front, possibly hundreds of thousands of tokens. And every intermediate result passes through the model: copying a 2-hour meeting transcript from Google Drive into Salesforce adds about 50,000 tokens, since the model reads it and writes it out again, risking copy errors.
- **The approach**: generate a file tree with one folder per server (`servers/google-drive/getDocument.ts`, ...), each file wrapping one MCP tool as a typed function. The agent lists folders, reads only the files it needs, and writes code that chains calls, so the transcript never passes through the model. The example drops from 150,000 to 2,000 tokens (98.7%). Cloudflare reported similar results as "Code Mode".
- **Benefits claimed**:
  - **Progressive disclosure** of tools, by browsing the filesystem or calling a `search_tools` tool with a detail-level setting (name only; name and description; or the full schema).
  - **Filtering in code**: from a 10,000-row sheet, the agent sees only the five pending rows it printed. The same applies to joins and aggregations.
  - **Control flow in code**: loops, retries and polling, for example waiting for a Slack message, run in the sandbox rather than as repeated model turns. This cuts latency.
  - **Privacy**: intermediate data stays in the sandbox unless the code logs it. The client can replace PII with placeholders such as `[EMAIL_1]` before the model sees it and restore the real values when calling the next tool. This allows deterministic rules about where data may flow.
  - **State and skills**: the agent can write files to a workspace and resume later, and can save working functions. Adding a `SKILL.md` turns them into reusable skills.
- **Cost**: running model-written code needs a secure sandbox, resource limits and monitoring. Weigh that operational and security burden against the token and latency savings.

## What to do with it

- With many tools or large payloads, present tools as importable code rather than loading every definition.
- Keep bulky data in the sandbox and return only summaries, counts or samples. Use code for loops, polling and joins.
- Tokenize PII in the client when sensitive data moves between systems.
- Budget for sandboxing before adopting this.

## Terms

- **Code execution with MCP** — the agent calls MCP tools by writing code against generated wrappers rather than through direct tool calls.
- **Code Mode** — Cloudflare's name for the same pattern.
- **PII tokenization** — the harness swaps sensitive values for placeholders the model sees and restores them for downstream tools.

## Caveats

- The 98.7% figure comes from one illustrative workflow and is not a benchmark.
- It comes from Anthropic, which launched MCP and promotes its ecosystem. MCP adoption claims ("de facto standard", thousands of servers) are the publisher's own.
- The article describes a pattern, not a shipped product feature. The 2025-11-24 advanced tool use note turns the same ideas into API features (Tool Search Tool, Programmatic Tool Calling).
