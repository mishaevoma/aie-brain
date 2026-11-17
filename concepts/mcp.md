---
type: concept
title: "MCP (Model Context Protocol)"
updated: 2026-11-17
status: evolving
---

# MCP (Model Context Protocol)

**Definition:** A standard way to connect an agent to tools and data that live outside its harness. A built-in tool runs code inside the harness. An MCP server is a contract through which the harness asks another system to do something.

## Why it matters

MCP is how an agent reaches your database, issue tracker or analytics without custom code for each harness. Every coding harness in one teardown is an MCP client. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) The cost is context: each connected server adds tool definitions, and each result passes through the model.

## What to do

- Use MCP for access to things that live elsewhere, mainly data. Use built-in tools for acting on the local environment. One builder calls these the data plane and the tool plane. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md) · [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md)
- To offer one capability across several harnesses, expose it once as an MCP server instead of writing a plug-in for each. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md)
- Measure what your servers cost. Five common servers with 58 tools took about 55K tokens of definitions before any work started. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)
- Above roughly 10K tokens of definitions or 10 tools, defer loading and let the model search for tools. Keep the three to five most-used loaded. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)
- With many tools or large payloads, use code execution with MCP (also called code mode): present servers as a code API and let the agent write code that calls them in a sandbox. Only the results it needs reach the context. One example workflow dropped from 150,000 to 2,000 tokens. [Code execution with MCP, Nov 2025](../sources/2025-11-04-anthropic-code-execution-with-mcp.md)
- Design MCP tools as carefully as any other tool: few, task-shaped, with clear descriptions and capped output. See [tool design](tool-design.md). [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Remove servers you do not use. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md)
- For non-developers, package a local server as a single-file bundle (`.mcpb`) with declared settings, not as install instructions. [Desktop Extensions, Jun 2025](../sources/2025-06-26-anthropic-desktop-extensions.md)

## Security

- A remote server's tools can change after you approved them. Treat anything outside an audited directory as untrusted, and remember that an audited connector does not make the data it returns trustworthy. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Keep credentials away from both the sandbox and the harness: route calls through a proxy that fetches tokens from a vault. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Inspect tool results before they reach the model where you can. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

## How it relates to skills

MCP connects tools. Skills teach multi-step workflows that use them. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)

## Related

[Tool design](tool-design.md) · [Context engineering](context-engineering.md) · [Skills](skills.md) · [Permissions and sandboxing](sandboxing-and-permissions.md)
