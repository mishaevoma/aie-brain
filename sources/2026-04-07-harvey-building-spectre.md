---
type: source
title: "Building Spectre"
author: "Joey Wang, Gabe Pereyra"
publisher: Harvey
url: https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform
published: 2026-04-07
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms, background-agents, production-operations]
---

# Building Spectre

**In one line:** In Harvey's internal agent platform the durable thing is the run record, workers are short-lived, the sandbox is an explicit boundary, and Slack, web, pull requests and schedules are all views of the same run.

## What it says

- Spectre turns a request from Slack, the web app or an automation into a durable run, executes it in an isolated sandbox, reaches GitHub, Datadog and Linear only across declared boundaries, and hands back things a person can review: summaries, diffs, branches, pull requests.
- Why build it: local coding agents break at the organisational boundary. They are tied to one laptop, one directory, one set of credentials and one person's private context, which makes them hard to share, secure and integrate.
- **Durable runs, ephemeral workers.** The durable object is the run record: ownership, sharing, attachments, execution history, artifacts, references to provider sessions. A worker executes one slice of work and terminates. A follow-up does not wake an old container. The control plane appends the new interaction to the run, starts a fresh worker, restores session context from the archive and continues.
- **The sandbox is the execution boundary.** A worker sees one repository workspace, a configured tool set and constrained credentials. It gets its configuration at start and has no ambient access to the control plane or its database. Repository access is scoped and short-lived, tools are injected at run start, and anything that must persist is written by the control plane, not by the worker. Disposable sandboxes were preferred to warm long-lived ones because half-reused environments with sticky state are harder to reason about.
- **A harness, not a wrapper.** The harness assembles context, starts the right provider adapter, translates provider events into a stable internal shape and owns run state. Runs need explicit progress, clear terminal states, per-run cost and usage accounting, timeouts, and rules for commits and pull requests. A thin wrapper suffices until durability, shared visibility, retries, cost accounting and several providers are needed.
- **Collaboration surfaces are part of the runtime.** Slack mattered because the context already lived there. The Slack invocation, the web page, the pull request and every follow-up refer to one run, which avoids each client growing its own half-private session.
- **Scheduled runs use the same runtime.** Cron automations create ordinary runs with ordinary history and artifacts, not a second background-job world.
- **Security.** Desktop agents have implicit boundaries: they inherit a whole machine, so nobody can say exactly what a run could reach or which credentials it used. A cloud run has a surface that can be listed: a single repository, a fixed set of tools, credentials that expire, one place for artifacts and one audit trail, with a record of who initiated, approved and executed.

## What to do with it

- Make the run record the unit people share, resume and audit, and let every surface point at it.
- Start a fresh worker for each slice of work and restore context from the record.
- Inject tools and credentials at run start, scoped to that run.
- Create scheduled work as ordinary runs.
- Account for cost and usage per run.

## Terms

- **Run record** — the durable object holding a run's history, artifacts and ownership.
- **Control plane** — the service that owns durable state and starts workers.

## Caveats

- Self-reported in April 2026, about an internal engineering platform, with no usage, cost or failure figures.
- The closing analogy to legal work is the company's product thesis, not evidence.
