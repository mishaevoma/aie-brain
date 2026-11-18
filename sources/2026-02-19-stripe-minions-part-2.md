---
type: source
title: "Minions: Stripe’s one-shot, end-to-end coding agents—Part 2"
author: "Alistair Gray"
publisher: Stripe
url: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
published: 2026-02-19
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, agents-and-workflows, background-agents, verification]
---

# Minions: Stripe’s one-shot, end-to-end coding agents—Part 2

**In one line:** Stripe's unattended coding agents run in the same pre-warmed, isolated cloud machines its engineers use, inside a workflow that mixes agent steps with fixed steps, and stop after at most two rounds of CI.

## What it says

- Minions are unattended. A request goes in, most often as a Slack message, a pull request that passes CI comes out, and a person reviews it. Over 1,300 merged pull requests a week contain only minion-written code, up from 1,000 ten days earlier.
- **Environment.** Each run gets a devbox: the standard AWS EC2 development machine that Stripe engineers already use, one per task. A warm pool makes one ready in 10 seconds, with repositories cloned, caches warm and services started. Devboxes are treated as cattle, not pets.
- Devboxes sit in the QA environment, with no production access, no real user data and no arbitrary network egress. So the agent runs with full permissions and no confirmation prompts: a mistake is confined to one devbox.
- **Harness.** A fork of Block's goose, made in late 2024 and then specialised for unattended use. Interactive features such as interruption were not needed.
- **Blueprints.** A run is a workflow defined in code. Each node is either deterministic (run the configured linters, push the branch) or an agent loop with wide latitude (implement the task, fix CI failures). Fixed nodes guarantee the required steps, save tokens and give the model less room to err. Each agent node can have its own tools, prompt and trimmed context. Teams write their own blueprints, for example for migrations.
- **Rules and tools.** Almost no global rule files. Rules attach by subdirectory or file pattern, in the format Cursor uses, and are synced for Claude Code. One internal MCP server, Toolshed, holds nearly 500 tools for all of Stripe's agents. Each agent gets a small curated subset, and a security control framework blocks destructive tool use.
- **Feedback.** A subset of linters runs locally in a loop before any push. Then comes one full CI run with autofixes applied, one more attempt by the agent if failures remain, and hand-back to the person. The suite has over three million tests. More CI rounds were judged not worth their tokens, compute and time.

## What to do with it

- Run unattended agents where your engineers already work in the cloud, and make that environment disposable and quick to create.
- Let isolation, not prompts, carry the safety of an unattended run.
- Write the required steps as code around the agent, and cap the expensive feedback rounds.
- Serve tools to all agents from one place, and give each agent few of them.

## Terms

- **Devbox** — a standard, disposable cloud development machine.
- **Blueprint** — a coded workflow whose nodes are deterministic steps or agent loops.
- **Toolshed** — Stripe's central internal MCP server.

## Caveats

- Self-reported, from February 2026, about one very large codebase with years of investment in developer tooling. No failure rates, costs or review load are given.
- Part 1 of the series describes the user's side and has no note of its own.
