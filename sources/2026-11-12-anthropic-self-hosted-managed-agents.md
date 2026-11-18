---
type: source
title: "Operate Claude Managed Agents inside your security perimeter"
author: "Anthropic"
publisher: Anthropic
url: https://claude.com/resources/articles/self-hosted-claude-managed-agents
published: 2026-11-12
ingested: 2026-11-17
kind: article
read: full
concepts: [managed-agent-runtimes]
---

# Operate Claude Managed Agents inside your security perimeter

**In one line:** Managed Agents now has three hosting levels (all at Anthropic, only the sandbox on your side, or the whole service on your side); at the third the customer runs the server, database and workers and chooses where model requests go.

## What it says

- Managed Agents (APIs that supply the harness, sandboxes, credential handling and session history) can now be hosted three ways:
  - **Hosted.** Anthropic runs the infrastructure on the Claude Platform.
  - **Self-hosted sandboxes.** The customer hosts only the sandbox, so that its code stays in its own environment.
  - **Self-hosted Managed Agents.** New, for unattended agents that need access to internal systems. Harness, sandboxes, credentials and session history all run in the customer's cloud or on-premise.
- At the third level the customer operates the server, its database and the workers on which agents run shell and file tools. Session history is stored in the customer's own database. The core APIs are the same as on the hosted service.
- Model requests go where the customer chooses: Anthropic directly, a cloud provider (Amazon Bedrock, Google's Agent Platform, Microsoft Foundry) or its own gateway. They are the only traffic to Anthropic that the article mentions at this level, and an organisation's zero data retention (ZDR) terms apply to them as to any Messages API call.
- Self-hosting changes two more things. Credentials can be kept in the customer's own secrets manager. And wherever the customer hosts the sandbox, it sets the network limits in its own firewall.
- Unchanged at every level: harness split from sandbox, credentials kept out of the sandbox, an optional list of allowed hosts per environment, and a full record of each session that exports over OpenTelemetry.
- Status: private beta, with access through an Anthropic account team.

## What to do with it

- Choose the level by what must stay inside your perimeter: code alone, or also the loop, credentials and session history.
- Count the operating cost of the third level: a server, a database and workers become yours to run.

## Terms

- **Self-hosted sandbox** — only tool execution runs on the customer's side.
- **Self-hosted Managed Agents** — the whole service does.

## Caveats

- A vendor's announcement of a private beta. It does not say how a self-hosted worker receives work, what the self-hosted service lacks beside the hosted one ("same core APIs" is the only hint), or what it costs. Its one diagram is an image, absent from the text read.
- That the loop, credentials and session history stay at Anthropic at the sandbox-only level is implied, not stated.
- [Scaling Managed Agents](2026-04-08-anthropic-managed-agents.md) is the earlier and fuller description of the same product.
