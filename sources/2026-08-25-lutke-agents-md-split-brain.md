---
type: source
title: "Thinking about banning Claude Code at Shopify until it reads AGENTS.md (untitled post)"
author: "Tobi Lütke"
publisher: "@tobi on X"
url: https://x.com/tobi/status/2092259436538495186
published: 2026-08-25
ingested: 2026-11-17
kind: x-post
read: full
concepts: [context-layer, instruction-files, skills]
---

# Thinking about banning Claude Code at Shopify until it reads AGENTS.md

**In one line:** When coding tools read different instruction files, a team's shared context forks; Shopify's CEO wanted every tool to read `AGENTS.md` and `.agents/skills`.

## What it says

- He was considering banning Claude Code at Shopify until it reads `AGENTS.md` and `.agents/skills`.
- His reason: a tool that only reads `CLAUDE.md` causes "split brain" problems when teammates use different tools, and that is avoidable.
- The post had about 19,000 likes when read on 17 Nov 2026.

## What to do with it

- Keep one source of truth for project instructions and skills, in the vendor-neutral locations (`AGENTS.md`, `.agents/skills/`).
- Where a tool needs its own filename, make that file a pointer to the shared one, not a copy.

## Terms

- **Split brain** — two sets of agent instructions for one project that drift apart because different tools read different files.

## Caveats

- A complaint from August 2026. Claude Code's documentation, checked on 17 Nov 2026, says it now reads `AGENTS.md` when a project has no `CLAUDE.md`, but still reads nothing under `.agents/`. This brain therefore keeps skills in `.agents/skills/` and links them from `.claude/skills/`.
