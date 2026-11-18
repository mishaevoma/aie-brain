---
type: source
title: "Building always-on agents"
author: "William Hu"
publisher: Anthropic
url: https://claude.com/resources/articles/building-always-on-agents
published: 2026-11-13
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, background-agents, side-effects]
---

# Building always-on agents

**In one line:** An always-on agent mostly sleeps; around its unchanged loop sit five pieces (event inbox, timers, memory, permissions, outbox), and every wake-up, a person's answer included, is a row in a durable inbox.

## What it says

- **Run and session.** A *run* is one wake-up (event in, work done, state saved) inside a *session*, the transcript. A user's reply resumes its session; other events start a new one.
- **Event inbox.** When sources call the agent directly, simultaneous events can set off competing runs and a crash can lose one. A handler appends each event to a durable table with a status, deduplicated on source identifiers; a background worker starts the run and marks events done.
  - The handler acknowledges fast, since webhook providers treat slow responses as failures. Prompt-injection checks wait for the run.
  - The inbox is the source of truth: a woken worker reads it first, so if one dies mid-run the next retries the event.
  - One active worker per inbox (at first, one inbox per user) stops two runs duplicating work or overwriting each other. Pending events are batched into one run.
- **Timers** (follow-ups the agent sets itself, and recurring schedules) live in their own durable store, since the inbox holds only ready events. A timer starts nothing: a scheduler, home-built or a durable execution engine, polls at a fixed interval and adds an inbox event per due timer.
- **Memory** is files mapped to a database or object store, so it outlives the worker. It holds only what cannot be looked up again: user instructions (loaded every run, as nobody is there to steer), notes on the user, messages already sent and task progress. Compaction and new sessions lose detail, so lasting facts go to memory during the run.
- **Permissions** are where the risk is highest, because an unattended run acts with the user's access. Each tool call proceeds, is blocked or waits. A proxy outside the agent's environment adds credentials to requests; classifiers screen higher-risk actions, as in Claude Code's auto mode.
- **Waiting for a person.** A deferred tool call ends the run and saves the session mid-call. The answer returns as an inbox event, whose run resumes the saved session. The worker stays free.
- **Outbox.** A run ends with a message, silence or a deferred call. A "send" tool suffices for most agents; an outbox table and dispatcher are needed only to pace messages or recover from errors.
- Cost: Opus 5.5 was 78% cheaper than Opus 5 per solved task on a long-horizon coding benchmark (40% on typical workloads).

## What to do with it

- Send every trigger, timers and human answers included, through one durable inbox.
- Allow one active worker per inbox, and choose whether a mid-run event waits, joins or interrupts.
- Model approval as ending the run and resuming on an inbox event.
- Tune message volume with evals, and start quiet.

## Terms

- **Deferred tool call** — a tool call parked until a person answers.

## Caveats

- A vendor's guide, four days old when read; no code, production numbers or failure rates.
- It does not say how a retried event avoids repeating side effects, or how the single worker is enforced. [Restate's article](2026-06-15-restate-checkpointing-is-not-resiliency.md) covers both.
