---
type: source
title: "Claude Managed Agents overview"
author: "Anthropic"
publisher: Claude Platform Docs
url: https://platform.claude.com/docs/en/managed-agents/overview
published: 2026-11-17
ingested: 2026-11-17
kind: docs
read: full
concepts: [agent-identity, managed-agent-runtimes, production-operations]
---

# Claude Managed Agents overview

**In one line:** Anthropic runs the loop and keeps the history behind four objects; the client still answers pauses, deduplicates events on reconnect and caps spend.

## What it says

- **Pages covered.** The overview and 24 sub-pages: sessions, events, environments, self-hosting, vaults, budgets, outcomes, multi-agent orchestration, workflow runs, scheduled deployments, webhooks, security, migration, reference.
- **Objects.** Agent: a versioned definition (model, system prompt, tools, MCP servers, skills). Environment: unversioned sandbox configuration. Session: a running instance of both, owning its sandbox and server-side history. Events: all messages either way.
- **Session lifecycle.** Statuses: `idle`, `running`, `rescheduling` (automatic retry), `terminated` (unrecoverable error, or archived).
  - Idle carries a stop reason: `end_turn` (finished or interrupted), `requires_action`, `budget_reached`; `retries_exhausted` and `refusal` also occur. On `requires_action` the client answers each listed event ID with `user.custom_tool_result` or `user.tool_confirmation`; the session waits indefinitely.
  - `user.interrupt` stops the model at once; a running tool call may finish first.
  - History lasts until deletion. The sandbox is checkpointed at each idle but kept only 30 days from creation, whatever the activity; later resumes start fresh.
- **Streaming.** A stream carries only events emitted after it opens. On reconnect: open a stream, list the full history, skip streamed events whose IDs were listed.
- **Environments.**
  - Cloud: a fresh Linux container at Anthropic (up to 8 GB memory, 10 GB disk); networking is `limited` to listed hosts or `unrestricted`, the API default.
  - Self-hosted sandbox: a work queue your worker polls over outbound HTTPS, running bash and file tool calls. History, tool results, skills and memory stores still reach Anthropic; only sandbox files and processes stay yours.
  - The whole service can be self-hosted on request; model calls still carry the conversation out.
- **Vaults.** MCP credentials never enter the sandbox; Anthropic's servers connect. Environment-variable credentials appear there as placeholders, swapped for the real value at egress to the credential's hosts, where sandbox code can still use them. A token obtained by exchange arrives unredacted.
- **Budgets and price.** List cost is model tokens at list price plus $0.08 per hour of session running time and $10 per 1,000 web searches. A budget, attachable only at creation, caps it and is checked between model requests, so each thread may overshoot by one request. Then the session idles until the cap is raised or removed.
- **Triggers.** A scheduled deployment starts sessions by cron; missed triggers are not retried or backfilled. Webhooks only notify: an event type and ID, three delivery attempts, unordered, then dropped.
- **Outcomes and multi-agent.**
  - Outcome: a description and markdown rubric; a grader with its own context window scores each iteration (default 3, maximum 20).
  - Subagents get context-isolated threads (one level, 25 at most) but share the sandbox, files and vault credentials.
  - Workflow runs: at most 64 concurrent threads and 1,000 agents, with a 24-hour lifetime by default. `completed` does not mean passed, and no client event ends a run.
- **Restrictions.** Beta, behind the `managed-agents-2026-04-01` header. Not eligible for Zero Data Retention or HIPAA: transcripts persist until deleted. Organisation rate limits: 300 creates and 1,200 reads a minute.

## What to do with it

- Rebuild client state from listed history, not the stream or webhooks.
- Set `networking` and a budget at creation.
- Export deliverables within the sandbox's 30 days.

## Terms

- **Workflow run** — one background execution of a program the agent wrote to run other agents.

## Caveats

- Undated documentation, read on 17 November 2026; the date above is the day it was read.
- A vendor's documentation for a beta product, read on one day. The design rationale is in [Scaling Managed Agents, Apr 2026](2026-04-08-anthropic-managed-agents.md).
- Not stated: a maximum session duration, a region for sandboxes or stored sessions (only an `inference_geo` pin for model requests), whether a retried tool call runs once. Prices come from the budgets page.
