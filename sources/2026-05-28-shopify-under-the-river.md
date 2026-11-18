---
type: source
title: "Under the River"
author: "Burke Libbey, Javier Moreno, River"
publisher: Shopify Engineering
url: https://shopify.engineering/under-the-river
published: 2026-05-28
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, background-agents, durable-execution]
---

# Under the River

**In one line:** Shopify's Slack agent runs on an internal platform built around one rule, that the session must outlive every process, sandbox and machine, and on which a new agent product is a bundle of configuration and not a new system.

## What it says

- River is an agent in Shopify's company Slack, launched about two months before the post. One in eight merged pull requests across the company is co-authored by it. In a recent 30-day period there were 59,918 sessions in 5,170 channels, and 3,536 River-co-authored pull requests merged. The median session lasts 19 minutes and makes 50 tool calls.
- Two earlier bets made it possible: one monorepo, and every environment (development, CI, production) built reproducibly with Nix. The lesson drawn is that what makes a codebase workable for agents is what its human engineers were owed anyway.
- **Public by construction.** River only works in public channels, with no direct messages. Every session is a searchable transcript that others can join and redirect. The team mines the transcripts and feeds patterns back into skills, prompts and defaults. A private local agent teaches only the person at the keyboard.
- **Aquifer** is the platform underneath: session, harness, sandbox, gateway, durable event log, credentials proxy and observability pipeline. Its design constraint: cells, sandboxes and machines die, and the conversation does not.
  - Session: a durable identity with an append-only event log in Postgres. The canonical record.
  - Harness: the agent loop. It reads history, calls the model and emits tool intents. Disposable and cheap to recreate.
  - Sandbox: filesystem, shell and repository. Disposable, sometimes warm, often fresh.
- The harness runs outside the sandbox. Three properties follow: safety (the loop is outside the blast radius of a destructive command), replaceability (models and runtimes change without touching the sandbox) and observability (the whole decision stream is in one place). The post says this boundary cannot be retrofitted, and cites Anthropic's [Managed Agents article](2026-04-08-anthropic-managed-agents.md) as confirmation of a shape it had been approaching.
- **Session cells.** A live session is an ephemeral process. When idle it exits. The next interaction starts a fresh cell, possibly on another host, and the work continues because it lives in Postgres and not in memory. Cattle, not pets, at the level of the session.
- **Profiles.** An agent product is data: a system prompt, skills, extensions, a sandbox policy and model defaults, shipped as a bundle. River is one profile and pull request review is another.
- The same objects serve three modes: interactive (a durable session with a live person), automation (a durable session woken by an outside system, often with nobody in the loop) and job (ephemeral batch or CI work that reuses the sandbox plane, where the session log is optional).

## What to do with it

- Make the session log the source of truth, and make everything that executes disposable.
- Keep the loop outside the sandbox from the start.
- Design the second agent as a profile on the first one's platform. If it needs a new platform, the first was not a platform.
- Consider making agent sessions visible to the team by default, and mine them.

## Terms

- **Session cell** — a short-lived process that hosts one live session and exits when idle.
- **Profile** — the configuration that turns the shared platform into a particular agent.

## Caveats

- Self-reported, May 2026, with usage counts from a table the agent writes itself. The platform was still rolling out, and no failure rates or costs are given.
- It rests on a monorepo and Nix that few organisations have.
