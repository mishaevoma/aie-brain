---
type: source
title: "Pinecone: Harnessing the wisdom of the workforce"
author: "Allen Chen, Tess Rosania"
publisher: Sierra
url: https://sierra.ai/blog/pinecone-harnessing-the-wisdom-of-the-workforce
published: 2026-07-15
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, background-agents]
---

# Pinecone: Harnessing the wisdom of the workforce

**In one line:** Sierra moved agents off laptops into one internal cloud agent whose sessions outlive their sandboxes, wrapping vendor harnesses behind a common protocol so fixes ship once for everyone.

## What it says

- **Session.** Agents on laptops did not scale and kept what people learned on their own machines. A prompt gets its own pod with the repository checked out, the build cache warm, dev servers running and a harness, in about a second. Sessions start from a browser, Slack, Linear, webhooks or schedules.
- **Three components.** The app server logs every turn, passes it to Agency and follows the runner's stream. Agency maps each runner to a Kubernetes pod, carries live traffic on Redis Streams and separately keeps durable events and checkpoints for recovery. In the runner, a Go supervisor runs Codex or Claude Code, manages dev services and brokers privileged operations.
- **Durable sessions.** Sessions are meant to last hours or days, keeping conversation and uncommitted work through harness crashes and pod or node failures. Agency keeps recording their state, so a new runner takes over where the failed one stopped. The same mechanism lets another user branch a whole session under their own MCP authorisation.
- **Credentials.** The harness's network and filesystem access is restricted. Authenticated calls (to an inference provider, to GitHub) pass through a network proxy that allows or refuses each one and attaches the credentials, so the agent never holds real ones.
- **Routing.** A classifier reads the prompt and picks the model and reasoning budget, the harness, the repository and the environment, since users could not tell whether a task called for 8 CPUs or 0.1 CPU. If the task changes, a new environment gets the same context.
- **Borrowed harnesses.** Every sandbox has Codex and Claude Code installed, with an adapter translating both to one shared protocol based on AG-UI. Sierra can move traffic between providers and gains whenever vendors improve their harnesses.
- **PR monitoring.** A monitor sub-agent stays with a session's pull requests, dealing with most review comments and failing tests, rebasing on conflicts and asking a person only when judgement is needed.
- **Lessons.** Build primitives (context, environments, company tools), not workflows, which had to be rewritten as models improved. Centralise: a misbehaving harness is fixed once for everyone, and a small team owns cost, defaults and model routing, with no token-usage leaderboard.
- **Adoption.** Over the last month 600 people created more than 75,000 sessions and 70% of pull requests were opened through Pinecone; 96% of engineering uses it. Since April usage has tripled monthly while costs fell.

## What to do with it

- Wrap vendor harnesses behind one adapter protocol rather than writing a loop.
- Record session state outside the sandbox, so a replacement runner can resume and others can branch.
- Attach credentials at a network proxy; give the harness none.

## Terms

- **Session** — the unit of work: a prompt, an isolated environment, an output stream.

## Caveats

- Self-reported by Sierra, July 2026, about an internal tool; no failure, resume-time or cost figures.
- Recovery is described in the companion post, [Agency](2026-07-29-sierra-agency-sandboxes-for-agents.md).
- Here the harness runs inside the sandbox. [Under the River](2026-05-28-shopify-under-the-river.md) argues for keeping the loop outside.
