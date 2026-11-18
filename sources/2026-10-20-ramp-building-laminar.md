---
type: source
title: "Building Laminar: Ramp's Managed Agents Platform"
author: "Sam Kronick"
publisher: Ramp
url: https://builders.ramp.com/post/building-laminar
published: 2026-10-20
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, background-agents, managed-agent-runtimes, production-operations]
---

# Building Laminar: Ramp's Managed Agents Platform

**In one line:** After trying vendor agent SDKs, managed agent APIs and frameworks, Ramp built one in-house platform for every agent product it ships, and gives three reasons: freedom to choose models, speed of iterating next to product teams, and owning the traces.

## What it says

- Laminar is the in-house harness and platform under all of Ramp's agent products. The decision to build one common platform came around May 2026, after products had been built on a dozen different stacks. Version 1 took 6 weeks. Five months later every agentic product at Ramp runs on it. The early motto was to build agents, not infrastructure.
- It has to serve four kinds of agent: interactive support chat, headless document processing with no person involved, coding agents in a development sandbox, and long-horizon knowledge-work agents that manage subagents, automations, sandboxes, cloud browsers and MCP connectors, with several people in one session and deep Slack integration.
- Why not a managed agents API, whose shape Laminar otherwise resembles:
  - **Model choice.** A managed agents API from one model provider locks you into its models. A common layer over several providers' managed APIs was considered and judged to be about as much work as building the platform.
  - **Speed.** A platform team next to the product teams, in the same Slack and codebase, turns a request into a shipped change in minutes. No vendor can.
  - **Observability.** Good agents come from reading traces. Off-the-shelf services imposed abstractions that did not fit, so the team built its own session debugging interface.
  - Coding agents had made building and maintaining the platform cheap compared with taking on vendor dependencies.
- What the harness is responsible for, as listed: conversation storage, compaction, standard tool interfaces such as MCP, message queuing and steering, lifecycle hooks, durable execution of the loop across deploys and failures, interoperability with many model APIs, sandboxes and filesystems, tool search, synchronous and asynchronous subagents, token streaming, human-in-the-loop, a protocol for generated UI, multiplayer chat and observability tooling.
- Four early choices that held up:
  - **Sandbox as a tool.** A session's lifetime is independent of any sandbox. The agent definition, conversation history and turn state live in a database, and the agent reaches a full computer through tool calls when it needs one.
  - **Boring technology.** Postgres, Temporal and S3, chosen because the team knows how to run, scale and repair them.
  - **Non-blocking by default.** Approvals, new messages sent during a run, and work handed to subagents never close the session to new input.
  - **Cloud only.** Everything runs on generic disposable workers. The author treats the months when agents ran on engineers' laptops, late 2025 to early 2026, as a brief reversal of the long move to the cloud.
- Request path: client, API service, a signal to Temporal, workers running workflows and activities, model calls through an internal model gateway, events streamed back, with sessions and messages in PostgreSQL.
- Would they do it again: yes. Building in-house has never been cheaper, and it still needs experienced engineers on call who work out what product teams need.

## What to do with it

- Before renting a managed agent runtime, check three things: whether you can change model provider, how fast you can change the platform, and whether you can read every trace.
- If you build, serve all your agent types from one platform, and review each requested feature for whether it generalises.
- Keep the session independent of the sandbox, and keep it open to input while work is in progress.
- Prefer infrastructure your team already knows how to operate.

## Terms

- **Sandbox as a tool** — the agent calls a sandbox through tools, and the session does not live in it.
- **Steering** — sending a message to a run in progress to redirect it.

## Caveats

- Self-reported in October 2026 by the platform's builder, with no cost, reliability or scale figures. Deeper posts on tools, sandboxes, connectors and developer experience are announced as companions and were not read.
- The claim that building was cheap rests on a small experienced team and an agent-written codebase.
- From the same company as the [background agent post](2026-01-12-ramp-background-agent.md), whose coding agent now runs on this platform.
