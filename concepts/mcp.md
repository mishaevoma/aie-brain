---
type: concept
title: "MCP (Model Context Protocol)"
updated: 2026-11-18
reviewed: 2026-11-18
status: evolving
---

# MCP (Model Context Protocol)

**Definition:** A standard way to connect an agent to tools and data that live outside its harness. A built-in tool runs code inside the harness. An MCP server is a contract through which the harness asks another system to do something.

## Why it matters

MCP is how an agent reaches your database, issue tracker or analytics without custom code for each harness. Every coding harness in one teardown is an MCP client. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) The cost is context: each connected server adds tool definitions, and each result passes through the model. [Code execution with MCP, Nov 2025](../sources/2025-11-04-anthropic-code-execution-with-mcp.md)

## What to do

- Use MCP for access to things that live elsewhere, mainly data. Use built-in tools for acting on the local environment. One builder calls these the data plane and the tool plane. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md) · [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md)
- To offer one capability across several harnesses, expose it once as an MCP server instead of writing a plug-in for each. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md)
- Measure what your servers cost. In Anthropic's measurement, five common servers with 58 tools took about 55K tokens of definitions before any work started. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)
- Above roughly 10K tokens of definitions or 10 tools, Anthropic advises deferring them and letting the model search for tools, with the three to five most-used kept loaded. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)
- With many tools or large payloads, use code execution with MCP (also called code mode): present servers as a code API and let the agent write code that calls them in a sandbox. Only the results it needs reach the context. In Anthropic's example a workflow dropped from 150,000 to 2,000 tokens. [Code execution with MCP, Nov 2025](../sources/2025-11-04-anthropic-code-execution-with-mcp.md)
- Design MCP tools as carefully as any other tool: few, task-shaped, with clear descriptions and capped output. See [tool design](tool-design.md). [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Remove servers you do not use. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md)
- For non-developers using Claude Desktop, package a local server as a single-file bundle (`.mcpb`) with declared settings, not as install instructions. The format is open to other desktop apps. [Desktop Extensions, Jun 2025](../sources/2025-06-26-anthropic-desktop-extensions.md)

**State and long-running calls**

- Do not key server state on the connection. The 2026-07-28 revision dropped the handshake and the transport session, so any instance of a server can answer any protocol request. A tool that needs state returns a handle, which the model passes back as an argument. [MCP 2026-07-28, Jul 2026](../sources/2026-07-28-mcp-2026-07-28-specification.md) The state behind a handle still needs a home: a shared store, or one instance that requests reach by routing on the id. [Tasks extension, Apr 2026](../sources/2026-04-27-mcp-sep-2663-tasks-extension.md)
- When a tool needs input mid-call, return a request for it and expect the call again with the answers, instead of holding a stream open. [MCP 2026-07-28, Jul 2026](../sources/2026-07-28-mcp-2026-07-28-specification.md)
- For slow work, the server may answer with a task handle instead of blocking, if the client has declared the Tasks extension, an official extension outside the core protocol. The client polls, answers and cancels by id, and should store the id durably. The server must persist the task before returning the handle, and a cancel is only a request. [Tasks extension, Apr 2026](../sources/2026-04-27-mcp-sep-2663-tasks-extension.md)

**Across many agents**

- Put one gateway between your agents and the systems they reach through MCP. DoorDash's scopes permissions to each task, logs every action and holds authentication and policy. [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) Uber's verifies each agent's token and enforces policy per tool. [Uber, May 2026](../sources/2026-05-21-uber-solving-identity-crisis-for-ai-agents.md)

## Security

- A remote server's tools can change after you approved them. Treat anything outside an audited directory as untrusted, and remember that an audited connector does not make the data it returns trustworthy. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Judge the connected tools together, not one server at a time. Mixing servers is how the lethal trifecta gets assembled: one reads private data, another fetches text an attacker wrote, a third can send. A single server can also hold all three. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md) See [permissions and sandboxing](sandboxing-and-permissions.md).
- Keep credentials away from both the sandbox and the harness: route calls through a proxy that fetches tokens from a vault. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Inspect tool results before they reach the model where you can. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- In a workspace shared by several people, check what a server can scope. Most servers were designed for one user and do not handle permissions per resource, which led one product to build some integrations itself. [Notion, Feb 2026](../sources/2026-02-27-notion-security-in-custom-agents.md)

## How it relates to skills

MCP connects tools. Skills teach multi-step workflows that use them. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)

## Next to MCP

A2A (Agent2Agent) is an open protocol between agent systems. A long-running job in A2A is a task with a lifecycle that can stop to wait for input or authorization, and the client follows it by polling, a stream or a webhook. [A2A docs, Nov 2026](../sources/2026-11-17-a2a-streaming-and-asynchronous-operations.md) In this brain's reading, A2A is to agents what MCP is to tools.

## Related

[Tool design](tool-design.md) · [Context engineering](context-engineering.md) · [Skills](skills.md) · [Permissions and sandboxing](sandboxing-and-permissions.md) · [Agent platforms](agent-platforms.md) · [Agent identity and tenancy](agent-identity.md)
