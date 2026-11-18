---
type: source
title: "The harness has to finish the job"
author: "Joey Wang"
publisher: AI Engineer
url: https://ai.engineer/code/2026/talks/online-harvey-agent-platform
published: 2026-11-11
ingested: 2026-11-17
kind: video
read: full
concepts: [background-agents, production-operations]
---

# The harness has to finish the job

**In one line:** Once agents, scripts and alerts could start work on Harvey's agent platform, capacity broke; the fixes were deduplicated triggers, a fair launch queue between accepting and starting a task, and automations that switch themselves off.

## What it says

- **Scale.** Spectre, Harvey's internal cloud agent platform, started more than one agent a minute on average last month, for about 460 people; agents have written 10,000 pull requests. Anything a person can click, an agent can call from the CLI, which by October started about 6,500 tasks a month.
- **Follow-up loop.** A loop reads CI failures on an agent's pull request and pushes fixes unattended. In October, four in five agent pull requests merged into the backend had been through it. Wang's pick, if you build only one piece.
- **Alert storm, mid August.** A release bug fired an alert per workspace into one Slack channel, a workflow tagged the agent on each, and every tag started a task: around 900 in about 4 hours, against about 50 on a normal day, all chasing one bug. Fix: a repeat alert joins the investigation already open.
- **One engineer's burst, October.** About 950 tasks from the command line in about 3 hours filled the cluster, and everyone else's work waited.
- **Fair launch queue**, shipped four days later. Starting a task gives a place in line, and a dispatcher starts it when there is room. Interactive work goes first. Each person has a concurrency limit and can borrow beyond it when the cluster is quiet. Queue position is visible.
- **Automations**, woken by a schedule or an event, are the fastest-growing source of work; about 110 people ran them last month. One that fails five times in a row switches itself off, and each can carry a budget or an expiry date.
- **Next bottleneck: merging.** Company-wide pull requests rose about 60% in a month, a merge went from 15 to 30 minutes to over an hour, and the merge queue kept being switched off. Unsolved, he says. Only one merge in 20 carries proof that it works.
- **Checkout.** Git was the slowest step: checking out every repository took over a minute on average, so workers keep copies that tasks borrow.

## What to do with it

- Separate accepting a task from launching it, with per-person limits, before opening a CLI to agents.
- Attach a repeated trigger to the run already handling it.
- Give every automation a consecutive-failure cut-off, a budget and an expiry date.

## Terms

- **Follow-up loop** — unattended retries after CI fails on an agent's pull request.
- **Fair launch queue** — admission control between accepting a task and starting it.

## Caveats

- Based on the event page's summary and machine transcript (AI Engineer CODE 2026), with recognition errors; only unambiguous figures are reported. Garbled and left out: volume and completion figures for the busiest days, and what fell from almost two seconds to 70 milliseconds in a 300-task load test.
- The title is the site's own description; the formal talk title was not verified. Slides not seen.
- Self-reported. Several fixes shipped together, so Wang cannot say which worked.
- The platform's architecture is in [Building Spectre](2026-04-07-harvey-building-spectre.md).
