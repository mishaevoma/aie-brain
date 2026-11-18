---
type: source
title: "Architecture"
author: "OpenAI"
publisher: OpenAI API docs
url: https://developers.openai.com/api/docs/guides/agents-api/architecture
published: 2026-11-17
ingested: 2026-11-17
kind: docs
read: full
concepts: [managed-agent-runtimes]
---

# Architecture

**In one line:** In OpenAI's Agents API an OpenAI-hosted Codex harness holds the loop and the session, while commands run in a separate, optional environment; self-host that environment and its compute, files, reconnection and shutdown are yours.

## What it says

- Covers four Agents API guide pages: Architecture, Sandbox lifecycle, the overview and OpenAI-hosted sandboxes. The API changelog dates the public beta to 10 September 2026.
- **Three parts.** The harness, an OpenAI-hosted Codex instance, owns the model-and-tool loop and the session. The environment is where commands and files live. The application server, your code, submits tasks, receives events and answers function tools.
- **Environment types.** `none`: no built-in Bash, apply-patch, workspace files or executor MCPs; remote MCP and function tools still work. `openai_hosted`: a Linux sandbox OpenAI creates per session. `self_hosted`: compute you start.
- **Self-hosted connection.** An executor in your compute dials out to the API with the environment ID and an environment key and runs what the harness requests. If input arrives with no executor connected, the API emits `agent.session.action_required` (`required_action.type: "environment_connection"`) and waits up to five minutes before failing the submission.
- **Not replayed, not restored.** A late connection does not replay timed-out input. A mid-turn disconnect can fail a tool while the turn still completes, and neither requests reconnection nor restarts a killed command. A reused environment ID brings back no files. Pending input is not guaranteed to survive a process crash.
- **Self-hosted shutdown.** An idle event alone is not a safe signal to stop compute. Deleting a session does not stop your compute and emits no webhook.
- **Hosted sandbox.** Files persist across turns while the sandbox exists. After an hour with neither activity nor keep-alives it can be deleted; the timeout is fixed. Files under `/workspace/outputs` become immutable artifacts at turn completion and outlive the sandbox. Sizes: `small` (1 vCPU, 1 GB), `medium` (2 vCPU, 4 GB, the default), `large` (4 vCPU, 16 GB).
- **Waiting and streams.** Waiting on the caller is a required action; the types named are `function_call` and `environment_connection`. Webhooks send `agent.session.action_required`, the stream `agent.session.requires_action`. With no function handler the agent can stay waiting. Closing the event stream leaves the task running; webhooks report state changes without a stream.
- **Billing.** Model usage at API rates, hosted sandboxes at standard container rates. Since a changelog entry of 9 October, hosted compute is billed during active turns, not idle time between them.
- **Restrictions.** Data residency only in the United States; no Zero Data Retention (ZDR), self-hosted or not.

## What to do with it

- With self-hosted compute, give each session one owner and start it on the `environment_connection` action, not on connection events.
- Recheck session state before stopping compute; set client and proxy timeouts above five minutes.
- Keep files in provider storage or snapshots; inspect tool results even when a turn completes.

## Terms

- **Executor** — the process in self-hosted compute that connects out to the API and runs requested commands.

## Caveats

- Undated documentation, read on 17 November 2026; the date above is the day it was read.
- Vendor documentation for a beta product; it may change.
- Not covered: resuming a dropped stream, how sessions are stored and recovered, container rates. Idle billing comes from the changelog.
