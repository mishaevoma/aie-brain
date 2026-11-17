---
type: source
title: "Coding-agent harnesses, taken apart: Codex, Claude Code, Cursor, OpenCode, Aider, Goose, Cline and T3 Code"
author: "Dinakaran"
publisher: "Loams"
url: https://www.loams.dev/blog/coding-agent-harnesses
published: 2026-10-18
ingested: 2026-11-17
kind: article
read: full
concepts: [agents-and-workflows, context-engineering, context-layer, harness, instruction-files, long-running-agents, mcp, sandboxing-and-permissions, tool-design]
---

# Coding-agent harnesses, taken apart: Codex, Claude Code, Cursor, OpenCode, Aider, Goose, Cline and T3 Code

**In one line:** the harness, not the model, decides whether an agent run is useful and safe, and across eight harnesses the same parts recur: loop, gate, sandbox, compaction, edit format, undo.

## What it says

- **Definition:** a coding agent is a model plus a harness. The model only proposes text and tool calls; the harness builds context, defines tools, decides which calls run, runs them, feeds results back, and fits it all in the window. Built from public code and docs only.
- **Loop:** text ends the turn; a tool call passes the gate, executes, and truncated output returns; compaction fires near the limit. Cline moved to native JSON Schema tool calls in v3.35; Aider's 2023 benchmarks found function calling gave worse edits than plain text.
- **Gate:** every harness has an autonomy ladder, e.g. Claude Code `plan` → `bypassPermissions` (with `auto`), Codex `read-only` / `workspace-write` / `danger-full-access`. Goose defaults to Completely Autonomous; T3 Code to Full access. Reviewer models in the gate (Claude Code `auto`, Cursor Auto-review, Codex `auto_review`) are, per each vendor, not the security boundary. Claude Code hooks can allow, deny, ask or rewrite; exit code 2 blocks.
- **Sandbox:** only Codex, Claude Code and Cursor ship one (Seatbelt on macOS; bubblewrap, seccomp or Landlock on Linux). Claude Code's network proxy starts with an empty allow-list and swaps placeholder credentials for real ones only on allowed hosts, but its sandbox covers shell commands only. Anthropic reports 84% fewer prompts, Cursor 40% fewer stops; fewer prompts is itself a security gain.
- **Compaction is lossy**; planted instructions can survive summaries. Goose compacts at 80% or 225,000 tokens.
- **Edits:** exact string replacement, patch envelopes (`apply_patch`), search/replace, unified diffs (Aider's `udiff` took GPT-4 Turbo from 20% to 61%). Lessons: no line numbers, anchoring context, readable failures.
- **Undo:** Claude Code keeps 100 checkpoints but not Bash changes; others use shadow git repos, hidden refs or per-edit commits. Worktrees isolate edits, not processes.
- **MCP/subagents:** all are MCP clients; Claude Code caps MCP output at 25,000 tokens and nests subagents three deep.
- **Failure modes:** rules files (`AGENTS.md`, `.cursor/rules`, `.clinerules`) are loaded into the prompt by design, so opening a repo means trusting its authors. Avoid Simon Willison's "lethal trifecta". Loop breakers: OpenCode `doom_loop` after three identical calls; Goose asks after 1,000 actions. A denial the model can read lets it adapt.
- **Loams' product (brief):** Loams Studio drives Claude Code, Codex, opencode, Pi and ACP agents via the `loams-agentd` daemon, supervised by default, unanswered approvals denied after 30 minutes. No OS confinement yet; `loams-sandbox` is Planned.

## What to do with it

- Invest in the harness; models change monthly.
- Put an OS sandbox that also wraps the network under any reviewer model.
- Treat rules files and repo content as untrusted input.
- Use anchored edits without line numbers; return readable errors and denials.
- Add loop breakers; document what you don't contain.

## Terms

- **harness** — everything in a coding agent except the model.
- **coding agent** — a model plus a harness.
- **gate** — decides if a call runs; the **sandbox** decides what it can reach.
- **compaction** — the harness rewriting its own context near the window limit.
- **lethal trifecta** — Simon Willison's name for an agent that has access to private data, exposure to untrusted content and a way to send data out; together they turn prompt injection into theft.

## Caveats

- Loams sells a harness that drives harnesses and ends with its roadmap; the "harness is the product" framing suits it.
- Snapshot as of October 2026; modes and defaults change fast. Roo Code shut down May 2026.
- No definition of interface or skill. Theo Browne (2026-10-22) says T3 Code is not a harness; Loams calls it a harness "control surface".
