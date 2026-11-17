---
type: concept
title: "Tool design"
updated: 2026-11-17
status: settled
---

# Tool design

**Definition:** Designing the functions an agent can call (names, descriptions, parameters, outputs and errors) for a caller that is a model, not a program. Also called the agent-computer interface (ACI).

## Why it matters

An agent may call a tool, skip it or misuse it, and it decides from the description alone. Small wording changes in tool descriptions have moved benchmark results, and most of the design effort in an early state-of-the-art coding agent went into its tool interfaces. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md) · [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)

## What to do

**Shape**

- Offer fewer, higher-level tools built around tasks, not thin wrappers over API endpoints. Prefer `search_contacts` to `list_contacts`. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Give each tool a distinct purpose. If an engineer could not say which tool applies, the agent cannot either. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Group tools under shared prefixes by service or resource, and test which naming form your model handles best. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)

**Inputs**

- Write descriptions as you would brief a new hire: formats, jargon, how resources relate. Use unambiguous parameter names such as `user_id`. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md) · [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Make mistakes hard to make (poka-yoke). Requiring absolute paths ended a whole class of errors. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) · [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)
- Add one to five realistic example calls for conventions a schema cannot express. Internally this raised accuracy on complex parameters from 72% to 90%. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)

**Outputs**

- Return what the model can use: readable names over opaque identifiers, and a concise or detailed mode. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Paginate, filter and truncate by default, and say how to narrow the request when output is cut. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Make errors and denials say what to do next. A refusal the model can read lets it find another route. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)

**File edits**

- Use exact string replacement that must match once, with enough surrounding context to anchor it. Avoid line numbers. Return a readable failure so the model can retry. [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)

**Large tool sets and large data**

- Use deferred tool loading once definitions pass about 10K tokens: the model searches for tools and loads only the ones it needs. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)
- Use programmatic tool calling when results are bulky or calls depend on each other: the model calls tools from code and returns aggregates. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md) · [Code execution with MCP, Nov 2025](../sources/2025-11-04-anthropic-code-execution-with-mcp.md)

**Improving tools**

- Evaluate tools with realistic tasks that take many calls, and keep a held-out set. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Have an agent read the transcripts and rewrite the tools. Tools optimised this way beat hand-written ones internally, and a tool-testing agent cut later task time by 40%. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md) · [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)

## What changed

A dedicated no-op "think" tool helped in policy-heavy tool use in early 2025. Since December 2025 the recommendation is to use extended thinking instead. [Think tool, Mar 2025](../sources/2025-03-20-anthropic-think-tool.md)

## Related

[MCP](mcp.md) · [Context engineering](context-engineering.md) · [Evals](evals.md) · [Agents and workflows](agents-and-workflows.md)
