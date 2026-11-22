---
type: source
title: "Run Your Harness Outside the Sandbox: Why and How"
author: "Nathan Flurry"
publisher: Rivet
url: https://rivet.dev/blog/2026-07-27-run-your-harness-outside-the-sandbox/
published: 2026-07-27
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms, durable-execution, sandboxing-and-permissions]
---

# Run Your Harness Outside the Sandbox: Why and How

**In one line:** Keep the loop, session history, credentials and approvals in your backend and reach the sandbox only through tool calls; Rivet would host the loop in an actor per agent, not a stateless server or workflow engine.

## What it says

- The easy first design runs the `claude` CLI inside a per-agent sandbox. Mature projects are said to be leaving it; OpenAI, Anthropic, Vercel, Cloudflare and Amp recently shipped platforms with the loop outside.
- **Blast radius.** Sandboxes exist to contain disorder, so they break: a build exhausts memory, a script pins the CPU, files get corrupted. Whatever lives inside dies too: the loop and its retries, the session history, the failure report.
- **Trust boundary.** Anything reachable from the sandbox should be assumed leaked or abused: model credentials, permission and approval checks, audit logs, per-user access rules, secrets for internal tools. Coding agents are trained to get around barriers, so a check enforced inside can probably be bypassed.
- **Sleep.** A paused sandbox cannot wake itself for a schedule or a long workflow, and reading or indexing sessions should not require booting one.
- **The design.** Every command or file operation becomes a tool that calls into the sandbox. Claude Code, Codex and OpenCode do not support this split natively.
- **Against stateless servers.** Two calls for one agent can both run the loop, and a dead server takes the run with it.
- **Against a workflow engine for the main loop.** The loop never ends, so replay of every step so far keeps growing. Changing code under a live run is hard, and a run that never exits makes every deploy a mid-run deploy. A workflow cannot hold a WebSocket or stream tokens.
- **Proposed instead:** one actor per agent, with its own sandbox and SQLite database. It restarts after a crash, sleeps when idle, wakes on a request or schedule, and serves several clients over WebSockets. The sample (about 180 lines) stores the sandbox id to reattach after sleep and takes prompts singly from a durable queue.
- **Figures.** A Pi session on Rivet is put at 0.82 MB of RAM. Keeping the loop outside adds roughly 10 milliseconds per tool call within one datacentre, against 50 to 200 milliseconds for an ordinary browser API request.

## What to do with it

- Keep the loop, retries, session history, permission checks and audit logging where a broken or compromised sandbox cannot reach them.
- Queue each agent's prompts so two requests never run its loop at once.
- Before running an open-ended loop on a workflow engine, check how replay cost grows and how a deploy reaches a never-ending run.

## Terms

- **Actor** — a long-lived, addressable process per agent with its own storage, asleep when idle.

## Caveats

- By a co-founder of Rivet, which sells the recommended runtime; its Pi library was added to the post on October 2, 2026.
- The figures have no stated method, hardware or workload.
- The case against workflow engines is argued, not measured; [Workflow SDK 5](2026-11-12-vercel-workflow-sdk-5.md) later reported replay overhead staying low over a long run.
- The sample saves history only after a prompt's whole loop returns; a mid-prompt restart is not shown.
