---
type: source
title: "Streaming and Asynchronous Operations for Long-Running Tasks"
author: "The Linux Foundation"
publisher: A2A Protocol
url: https://a2a-protocol.org/latest/topics/streaming-and-async/
published: 2026-11-17
ingested: 2026-11-17
kind: docs
read: partial
concepts: [mcp]
---

# Streaming and Asynchronous Operations for Long-Running Tasks

**In one line:** In A2A a long-running job is a task with its own lifecycle: a send call blocks until the task ends or needs the client, unless told to return at once, and progress arrives by polling, a stream or a webhook, with `GetTask` as the fallback read.

## What it says

- **Pages covered.** This overview, "Life of a Task" and, read in part, the protocol specification: operations, the task model, update delivery, push notifications and idempotency.
- **What A2A is.** The specification describes Agent2Agent (A2A) as an open standard for communication and interoperability between independent agent systems, which may be opaque to each other.
- **States.** Besides unspecified, submitted and working, a task has four terminal states (`TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_CANCELED`, `TASK_STATE_REJECTED`) and two interrupted ones (`TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_AUTH_REQUIRED`), where it waits for input or authorisation.
- **After a task ends.** A terminal task cannot restart and accepts no more messages (`UnsupportedOperationError`). Follow-up or refinement work becomes a new task in the same `contextId`; the client's message may cite the old task in `referenceTaskIds`. A task awaiting input continues when the client sends a message carrying its `taskId`.
- **When send blocks.** `SendMessage` blocks by default until the task is terminal or interrupted, then returns it with its artifacts. Setting `returnImmediately` to true in the request configuration returns as soon as the task is created, leaving the caller to follow it. Streaming calls ignore the flag.
- **Three ways to learn of progress.**
  - Polling `GetTask`: works with every binding, at the price of latency and wasted requests.
  - Streaming: `SendStreamingMessage` returns the task, then status and artifact events in the order generated. A dropped connection does not stop the task; `SubscribeToTask` opens a new stream that starts with the task's current state, though status messages missed meanwhile may be lost. Needs `capabilities.streaming`.
  - Push notifications: the agent POSTs the same event payloads to a webhook supplied with the send request or through `CreateTaskPushNotificationConfig`. Meant for work lasting minutes to days and clients that cannot hold a connection. Needs `capabilities.pushNotifications`.
- **Push delivery.** The agent must attempt delivery at least once per configured webhook. Retries with exponential backoff are not mandatory, and it may stop after a configured number of consecutive failures. Recommended timeout per webhook request: 10-30 seconds. Receivers must answer with a 2xx status and should handle duplicates idempotently.
- **Idempotency.** Get operations and `CancelTask` are idempotent, though a repeated cancel may return `TaskNotFoundError` once the task is purged, and cancellation may not succeed. Sending is not guaranteed idempotent: an agent may use `messageId` to detect duplicates.

## What to do with it

- Set `returnImmediately` for slow work and store the task id.
- Treat streams and webhooks as hints: confirm with `GetTask`, and keep polling as a backstop.
- Make webhook handlers idempotent and authenticated.
- Do not assume a retried send is deduplicated.

## Terms

- **Interrupted state** — input-required or auth-required: paused, not finished.

## Caveats

- Undated documentation, read on 17 November 2026; the date above is the day it was read. The specification page gives 1.0.0 as its latest released version.
- The pages contradict each other: send returns immediately in one section and blocks by default in another; streams close on terminal states in one place, on interrupted states too elsewhere.
- No retention period appears in the sections read; a completed task may already be purged (`TaskNotFoundError`).
