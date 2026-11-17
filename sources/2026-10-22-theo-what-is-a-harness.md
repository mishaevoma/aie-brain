---
type: source
title: "What is a \"harness\"?"
author: "Theo Browne"
publisher: "t3.gg"
url: https://t3.gg/blog/post/what-is-a-harness
published: 2026-10-22
ingested: 2026-11-17
kind: article
read: full
concepts: [agents-and-workflows, harness, mcp]
---

# What is a "harness"?

**In one line:** an LLM can only emit text; the harness turns that text into tool runs and feeds results back, an agent is a harness plus an LLM, and the app you click on is a separate interface.

## What it says

- People use computers through an **interface** (terminal, website, app), e.g. Chrome, Claude Code, the ChatGPT app.
- An LLM only generates text. To act it needs tools (commonly `read_file`, `edit_file`, `bash`, `search`), a text syntax for calling them, a system that parses output and runs the code, a way to return results, and a described list of available tools. That bundle is the **harness**.
- Claude Code is "kind of" a harness: an interface (the `claude` TUI or the desktop Code tab) with a harness baked in, the Anthropic Agent SDK. Codex's harness is the Codex App Server. Harnesses are rarely exposed to users.
- Harnesses get reused under other interfaces: Cursor's under "Grok Bot", the Agent SDK and Codex App Server under T3 Code, Pi under OpenClaw.
- Most important tools ship with the harness (many in Claude Code and Codex, few in Pi); good harnesses let users add their own. Tools sit on a "tool plane" that the harness exposes to both LLM and interface.
- **MCP:** a tool runs code here; an MCP server makes a request elsewhere. MCP mainly exposes data and needs no install, just a URL.
- T3 Code exposes its extra features (e.g. a Claude Code thread spawning Codex subagents) through one MCP server instead of plugins per harness.
- **Agent:** a harness combined with an LLM. Different agents are often just different harness configurations: tools, instructions, MCP servers.
- Analogy: LLM is the chef, harness the kitchen, T3 Code the restaurant. T3 Code is not a harness because it needs one to work.

## What to do with it

- Keep interface, harness and model separate in design and vocabulary.
- Build a custom agent by reconfiguring a harness (tools, instructions, MCP servers) before writing new infrastructure.
- To add one capability across many harnesses, expose it as an MCP server.

## Terms

- **interface** — what a human operates (terminal, website, app); not formally defined.
- **harness** — the tools, call syntax, parser/executor, result path and tool list that let a text-only LLM act.
- **agent** — a harness combined with an LLM.
- **tool** — runs code locally; **MCP** — requests something elsewhere.
- **tool plane** — where tools sit, exposed by the harness.

## Caveats

- No byline on the page (it links Theo's X account; first posted on X); author name taken from the brief.
- The author builds T3 Code and plugs it and a course; his definitions place T3 Code above the harness layer.
- Informal, no data; no mention of skills, AGENTS.md or sandboxing.
- Narrower than Loams (2026-10-18), which also counts gating, sandboxing, compaction and undo as harness parts and calls T3 Code a harness control surface.
