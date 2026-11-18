---
type: source
title: "Durable Objects now defer code updates by default"
author: "Cloudflare"
publisher: Cloudflare Changelog
url: https://developers.cloudflare.com/changelog/post/2026-10-30-durable-objects-deferred-code-updates/
published: 2026-10-30
ingested: 2026-11-17
kind: docs
read: full
concepts: [production-operations]
---

# Durable Objects now defer code updates by default

**In one line:** A deploy no longer resets an active Durable Object at once: by default the object may keep its old code for up to 300 seconds while it waits to hibernate, which narrows the window in which a deploy kills an agent mid-task without closing it.

## What it says

- Covers this entry and, in the last bullet, the related entry of October 1, 2026 on [pending I/O](https://developers.cloudflare.com/changelog/post/2026-10-01-pending-io-keep-alive/).
- **The problem.** A Durable Object is globally unique, so it runs one version of its code at a time. A deployed change used to apply immediately, which could interrupt work in flight and close open connections.
- **New default.** After a deploy an active object may stay on its existing code for as long as 5 minutes (300 seconds), waiting to hibernate. If it hibernates in time, it starts on the new code at its next request. If the delay runs out first, it resets and adopts the new code. WebSockets on the Hibernation API stay connected through a switch made after hibernating.
- **Best effort.** Not every operation is guaranteed to finish. An object can still reset before the delay is up, for example during a Cloudflare runtime update.
- **Configuration.** `code_update_strategy` under `durable_objects` in the Wrangler configuration takes a `mode` and a `max_delay`, in seconds, anywhere from 0 to 86400 (24 hours). For a single deployment, `--durable-objects-code-update-mode` takes `immediate` or `deferred <duration>`; immediate is suggested for incidents.
- **Idle eviction** (October 1 entry). With no client connected, pending work now keeps an object running for up to 15 minutes per operation, including service binding requests, calls to other Durable Objects, `waitUntil()` promises and timers. It is the default from compatibility date `2026-10-01`, and duration charges continue.

## What to do with it

- Keep the checkpoint and recovery code: deferral is bounded and best effort.
- Set `max_delay` to cover an ordinary turn; an object that has not hibernated by then is reset anyway.
- Use immediate mode to ship an urgent fix.

## Terms

- **Deferred code update** — a deploy that waits, up to a maximum delay, for an active object to hibernate before it adopts new code.

## Caveats

- A vendor changelog entry, with no figures on how often objects still reset early.
- The documentation it points to, on gradual deployments and the REST API, was not read.
- Both entries describe Durable Objects in general; the Agents SDK runs each agent as one, per [Long-running agents](2026-10-27-cloudflare-long-running-agents.md).
