---
type: source
title: "Introducing Nova, our internal platform for coding agents"
author: "Mike White, Kevin Altschuler"
publisher: Dropbox
url: https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents
published: 2026-05-21
ingested: 2026-11-17
kind: article
read: full
concepts: [agents-and-workflows, background-agents]
---

# Introducing Nova, our internal platform for coding agents

**In one line:** Dropbox runs coding agents as an internal service with one request shape (a commit, a task, validation commands, an iteration cap), and keeps CI triggering and code publication in deterministic workflows outside the agent loop.

## What it says

- Nova is an internal service for running coding agents in Dropbox's cloud. Engineers run several sessions in parallel, and internal systems call it as a step in automated workflows.
- Why a platform and not single-purpose tools: the monorepo depends on Bazel with remote execution and on-premise infrastructure, which third-party agent tools do not fit. Interactive chat and unattended background work needed the same execution, validation and context handling.
- **The session contract.** Every session gets its own isolated environment, holding the codebase as it stood at one commit. The caller supplies the task and, optionally, validation commands. If validation fails, Nova continues the session, feeds the results back and asks the agent to fix them, up to a set number of iterations (5 in the illustrative request).
- Several coding agents sit behind the same interface. Entry points are a web interface, a command line, an API, and a Slack thread whose context carries into the session. The platform also provides prompt evaluation, observability and feedback collection, plus skills, plugins and MCP integrations.
- **Publication stays outside the agent.** Each session is limited to a single branch. That gives a predictable view of what is active and being published, and makes the tasks around a branch (running tests, rebasing) easy to automate.
- Workflows built on it:
  - Deflaker, a durable workflow for flaky tests. It gathers passing and failing logs, asks the agent for a root cause and a fix, and validates the fix in CI with at least 100 runs of the test. On a new flake it carries notes forward and tries again, capped at five attempts.
  - Migrations and dependency upgrades, moved from an earlier Goose-based migrator that had no way to review or continue a failed attempt.
  - Experiments: reproducing production crashes as tests, deciding whether a change needs a second team's review, scheduled work on on-call toil, several agents reviewing one change.
- Lessons stated:
  - The platform around the agent is worth as much as the code the agent writes.
  - Context, validation and guardrails reinforce one another.
  - Not every step belongs inside the agent loop. Letting the agent run and wait for its own CI could hold a session for hours or validate against the wrong tests. It worked better for the surrounding workflow to trigger CI and bring the agent back when there was a failure to fix.

## What to do with it

- Give callers a narrow request shape: starting commit, task, validation commands, iteration cap, target branch.
- Let the workflow own waiting, CI and publication, and call the agent for the parts that need judgment.
- Cap every fix-and-validate loop.
- Make sure a failed background attempt can be opened and continued by a person.

## Terms

- **Validation commands** — checks the caller attaches to a session, run after the agent finishes and fed back on failure.

## Caveats

- Self-reported in May 2026, with no adoption, success-rate or cost figures.
- The request shown is described by the authors as illustrative pseudo-code.
