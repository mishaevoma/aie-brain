---
type: source
title: "1,500+ PRs Later: Spotify’s Journey with Our Background Coding Agent (Honk, Part 1)"
author: "Max Charas, Marc Bruggmann"
publisher: Spotify Engineering
url: https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1
published: 2025-11-06
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, background-agents]
---

# 1,500+ PRs Later: Spotify’s Journey with Our Background Coding Agent (Honk, Part 1)

**In one line:** Spotify put a coding agent into the one slot of its existing fleet-migration system where a script used to be, and kept everything around it (targeting, pull requests, review, merge) unchanged.

## What it says

- Fleet Management already applied scripted code changes across thousands of repositories, as containerised jobs that open pull requests. Since mid-2024 about half of Spotify's pull requests have come from it. Scripts stopped scaling for complex changes: the Maven dependency updater alone grew past 20,000 lines.
- From February 2025 the script could be replaced by an agent that takes a prompt. Targeting repositories, opening pull requests, review and merge stayed as they were.
- The agent is wrapped in a small internal CLI. It hands the prompt to an agent, runs formatting and linting through local MCP, has a model judge the diff, uploads logs and records traces in MLflow. The wrapper is what lets the team swap agents and models, which it had already done several times.
- Results at publication: more than 1,500 agent-written pull requests merged, and 60–90% of the time saved on those migrations compared with writing them by hand.
- The same agent was then exposed over MCP, so that people can start tasks from Slack and GitHub Enterprise. An interactive agent first gathers the details and writes the prompt, then hands it to the coding agent.
- Sharing one platform between migrations and ad hoc tasks standardised commit tagging, LLM quota management and trace collection.
- Open problems named: long run times, unpredictable output, sandboxing and guardrails, and cost.

## What to do with it

- Before building an agent platform from nothing, look for an existing job system (migrations, CI, batch) with a slot the agent can fill.
- Wrap the agent behind your own thin interface, so that the agent and the model can be replaced.
- Put quotas, tracing and commit attribution in the platform, once, for every entry point.
- Separate the conversation that clarifies a task from the unattended run that carries it out.

## Terms

- **Fleet Management, Fleetshift** — Spotify's system for applying one change across many repositories.
- **Honk** — the internal name of the background coding agent.

## Caveats

- From November 2025 and self-reported.
- [Part 3](2025-12-09-spotify-feedback-loops-part-3.md) covers verification. Part 2 (prompts and tools) and part 4 (a dataset migration, April 2026) have no notes yet.
