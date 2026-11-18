---
type: source
title: "Building an Intern"
author: "David Cramer"
publisher: cra.mr
url: https://cra.mr/building-an-intern/
published: 2026-07-02
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms]
---

# Building an Intern

**In one line:** On serverless functions an agent loop needs a task broker (inbox, queue, one lease per conversation, a transcript saved during the run, a soft deadline that requeues), and credentials belong in a proxy outside the sandbox.

## What it says

- Junior is Sentry's open-source Slack agent: four months of work, around 100,000 lines of TypeScript before tests, evals and docs. It runs on Vercel with Pi's SDK.
- **Broker.** A Slack webhook is saved to the conversation's inbox and a task goes onto Vercel Queues. A worker stops if nothing is pending and defers if another holds the lease. Otherwise it takes the lease, ingests new messages and continues the agent from the session log.
- **Soft deadline.** Vercel's default limit was 300 seconds, and few useful runs fit. At 240 seconds Junior interrupts itself at the end of a tool result, enqueues a continuation task and releases the lease. The author calls it a good design even with longer limits.
- **Transcript.** Pi's session log is written to Redis incrementally during the run, giving a near-live view of a thread and a recovery point.
- **Credentials.** Vercel Sandbox's network policy forwards outbound requests to Junior, which verifies the sandbox's OIDC token and a signed credential context, resolves the provider from the host, issues a short-lived lease and adds the `Authorization` header on the host side. The sandbox holds only a placeholder, so the model never sees a token. Without a valid credential the agent pauses, and the user authorises through an ephemeral Slack link.
- **Reads and writes.** For GitHub the grant is chosen from the request: reads default to a global installation token, while Git, REST and GraphQL writes need the user's own OAuth grant, which meant parsing GraphQL. Raw calls that create issues or pull requests are refused, forcing creation through Junior's typed tools, which own idempotency and add a fixed footer.
- **Events.** The agent can subscribe to events on a pull request it opened, such as `checks.failed`. GitHub webhooks are normalised, matched to subscriptions and queued as a synthetic user message. An ordinary user message is injected as steering right after a tool result.
- **Scheduled tasks** get no credentials, to guard against accidental harm and harmful tasks planted unnoticed; some read access remains (GitHub). He calls this unsolved.

## What to do with it

- Hold one lease per conversation, and queue later messages in an inbox.
- Set a soft deadline below the platform's limit, stop only after a tool result, and requeue.
- Persist the transcript during the run, not at its end.
- Inject credentials at the network boundary: a shared token for reads, the user's own grant for writes.
- Give scheduled runs no write credentials until you can tell who created the task.

## Terms

- **Soft deadline** — a self-imposed cut-off ahead of the platform's timeout.
- **Lease** — used twice: a worker's claim on a conversation, and a short-lived credential grant.

## Caveats

- One engineer's account from July 2026. No byline: the name comes from the site's copyright line. He says the code has bugs and the event model is not battle-tested.
- No figures for usage, cost, latency or failures, and the design follows Vercel's limits.
