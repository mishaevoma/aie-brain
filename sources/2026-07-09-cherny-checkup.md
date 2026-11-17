---
type: source
title: "New in Claude Code: /checkup"
author: "Boris Cherny"
publisher: "@bcherny on X"
url: https://x.com/bcherny/status/2074997570317779038
published: 2026-07-09
ingested: 2026-11-17
kind: x-post
read: full
concepts: [compounding, context-layer, instruction-files, mcp, sandboxing-and-permissions, skills]
---

# New in Claude Code: /checkup

**In one line:** Claude Code ships a command whose job is to shrink and tidy an agent's standing configuration, which tells you what its makers think goes wrong: unused extensions and an overgrown root instruction file.

## What it says

`/checkup` offers to do the following, asking before each change:

- Remove skills, MCP servers and plugins you do not use, to save context.
- Deduplicate your local `CLAUDE.md` against the checked-in one.
- Break a large root `CLAUDE.md` into nested `CLAUDE.md` files and skills.
- Turn off slow hooks.
- Update Claude Code.
- Enable auto mode by default.
- Pre-approve read-only commands that you keep getting prompted for.

## What to do with it

- Treat agent configuration as something that needs regular pruning, not only additions.
- Keep the always-loaded root file small. Move area-specific rules to nested files and procedures to skills.
- Count unused skills and MCP servers as a cost: their descriptions take context in every session.
- Fix repeated permission prompts at the source by allowing safe read-only commands.

## Terms

- **Nested CLAUDE.md** — an instruction file in a subdirectory that loads only when the agent works there.

## Caveats

- A product announcement in a single post. No detail on how the command decides what counts as unused.
- Specific to Claude Code as of July 2026; the author leads that product.
