---
type: source
title: "SEP-2663: Tasks Extension"
author: "Luca Chang, Caitie McCaffrey"
publisher: Model Context Protocol
url: https://modelcontextprotocol.io/seps/2663-tasks-extension
published: 2026-04-27
ingested: 2026-11-17
kind: docs
read: full
concepts: [mcp]
---

# SEP-2663: Tasks Extension

**In one line:** An MCP server may answer a tool call with a task handle instead of a result, and the client then polls, supplies input and cancels through three methods; the server alone decides when, and may not return the handle until the task can be read back.

## What it says

- **Problem.** Lets a server answer `tools/call` with a task handle instead of blocking until the result is ready. Tasks are durable state machines with server-generated ids, meant for expensive computations and batch processing.
- **Why the experimental design went.** The `2025-11-25` tasks feature, called a stopgap, had three faults. Opting in required reading `tools/list` first to learn which tools took a `task` parameter. `tasks/result` blocked until the operation finished, forcing long-lived connections. `tasks/list` could not be scoped safely once sessions were removed (SEP-2567). The redesign drops all three.
- **Who decides.** The server, per request. A client only declares the `io.modelcontextprotocol/tasks` capability on its requests; it cannot ask for a task, and must handle an ordinary result or one with `resultType: "task"`.
- **Follow.** `tasks/get` is an idempotent read: the status (`working`, `input_required`, `completed`, `failed`, `cancelled`) with the result, error or pending input requests inline. `pollIntervalMs` suggests the polling interval; after `ttlMs` the task may be discarded. Servers may also push `notifications/tasks` over `subscriptions/listen`.
- **Update.** In `input_required`, the client answers the listed `inputRequests` with `tasks/update`. Input needed before the task exists uses MRTR on the original call.
- **Cancel.** `tasks/cancel` signals intent. Whether and when the work stops is the server's call, so the task may keep `working` or finish in another terminal status. The client may discard its state at once.
- **Durable before returned.** The handle must not be returned until the task is durably created, meaning a `tasks/get` for it would resolve; on an eventually consistent store the server waits. Creation is strongly consistent, at an admitted latency cost.
- **Client persistence.** Clients are advised to keep task ids in durable storage, so polling can pick up after a crash or restart.
- **Routing.** On Streamable HTTP the `Mcp-Name` header carries the task id, letting a load balancer reach the instance holding the task's state, which the SEP says correctness typically requires.
- **Scope and status.** Final, Extensions Track: an official extension, not core, intended for promotion to core once stable and widely adopted. It covers `tools/call` only and is not wire-compatible with the experimental feature.
- **Security.** Task ids may serve as bearer tokens, so they must be unguessable, and every task request is authorised.

## What to do with it

- In a client, handle both result shapes on every tool call and store task ids durably.
- In a server, persist the task before replying, and route by task id when state is per instance.
- Treat cancellation as a request; the work may still complete.

## Terms

- **Task** — a durable, server-side state machine for one request, polled by id.

## Caveats

- The date above is the SEP's creation date, 27 April 2026; the page was last modified on 29 July 2026.
- The page is a frozen record and defers to the current specification and changelog.
- It calls its target revision `2026-06-30`, but the revision shipped as [2026-07-28](2026-07-28-mcp-2026-07-28-specification.md).
