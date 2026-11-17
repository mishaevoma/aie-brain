---
type: source
title: "Claude Code: Best practices for agentic coding"
author: "Boris Cherny"
publisher: Anthropic
url: https://www.anthropic.com/research/claude-code-best-practices
published: 2025-04-18
ingested: 2026-11-17
kind: article
read: full
concepts: [human-judgment, instruction-files, multi-agent-systems, verification]
---

# Claude Code: Best practices for agentic coding

**In one line:** a coding agent works best when you give it written project context, the right tools and permissions, and a workflow that makes it explore and plan before it writes code and checks its own output.

## What it says

- **CLAUDE.md** is loaded into context automatically. Use it for build and test commands, code style, repo etiquette, environment quirks and warnings. It can live at the repo root, in parent or child directories (useful in monorepos) or in `~/.claude/CLAUDE.md`. `/init` writes a first draft. Keep it short, treat it as a prompt you iterate on, and commit it so the team shares it. Emphasis words such as "IMPORTANT" can make the agent follow a rule more reliably.
- **Permissions** are an allowlist managed through `/permissions`, `.claude/settings.json` (checked in), or `--allowedTools` for one session.
- **Tools**: the agent inherits your shell, so CLIs like `gh` work. Teach it a custom tool through `--help` or a note in CLAUDE.md. MCP servers can be shared through a checked-in `.mcp.json`. Reusable prompts go in `.claude/commands` as Markdown files and take `$ARGUMENTS`.
- **Explore, plan, code, commit**: have it read the relevant files without coding, then ask for a plan. Thinking keywords raise the thinking budget, from "think" to "think hard", "think harder" and "ultrathink". Only then implement, verify and commit. Skipping the first two steps leads it to jump straight into code.
- **Give it a target to check against**: write failing tests first and tell it not to change them (TDD), or give it screenshots and a visual mock. The post says output typically improves a lot after 2–3 iterations.
- **Steer early**: be specific, attach images, files and URLs, interrupt with Escape, and `/clear` between tasks. Keep a Markdown checklist for large jobs.
- **Headless mode** (`-p`, `--output-format stream-json`) suits CI jobs such as issue triage, and fan-out: one `claude -p` call per item in a long task list.
- **Multiple agents**: one instance writes, a fresh one reviews. Run parallel sessions in 3–4 checkouts or git worktrees.
- **"Safe YOLO mode"** (`--dangerously-skip-permissions`) belongs only in a container without internet access.

## What to do with it

- Keep a short, committed agent-instructions file per repo, and revise it whenever the agent gets something wrong.
- Require a read-and-plan step before any non-trivial change.
- Give the agent a way to verify its work (tests, screenshots, linters) before you rely on its output.
- Clear context between tasks, and review with a fresh instance.

## Terms

- **CLAUDE.md** — a project memory file the agent loads automatically at session start.
- **Headless mode** — non-interactive runs for scripts and CI.

## Caveats

- A banner dated Jan 26, 2026 says the post is no longer maintained and points to the official Claude Code docs. Commands and flags may have changed since; for example, the `/project:` prefix for slash commands and the thinking keywords are specific to that time.
- It was written by Anthropic about its own product, and it says the tips are starting points, not rules.
- The pipelining example uses a `--json` flag that does not match the `--output-format` flag described earlier in the post.
