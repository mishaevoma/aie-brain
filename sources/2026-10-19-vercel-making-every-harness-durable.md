---
type: source
title: "Making every harness durable"
author: "Pranay Prakash, Eric Dodds"
publisher: Vercel
url: https://vercel.com/blog/making-every-harness-durable
published: 2026-10-19
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, durable-execution, side-effects]
---

# Making every harness durable

**In one line:** Durability can be added around an existing coding harness from the outside: log an intent before every model or tool call and the outcome after it, back each turn with a queue message, and give every tool a declared policy for what happens if a crash interrupts it.

## What it says

- Harnesses such as Pi, Claude Code, Codex and OpenCode were designed as long-lived local processes that keep the session in memory. Their workloads are moving to the cloud, where tasks run for minutes or hours on functions that time out.
- A VM with persistent storage is not enough. It does not record which model and tool calls completed, and it does not resume an interrupted turn after a crash.
- `durable-harness` is an open-source set of adapters that makes those harnesses durable without changing them.
  - Every step of a turn is written to a durable log twice: an intent record before a model or tool call starts, and an outcome record when it ends.
  - A queue message stands behind each turn. When the function running it dies, the queue gives the turn to a fresh function, which continues from the log.
  - After a crash the log separates three cases: finished, in progress, not begun. Finished calls are read back, so a completed model call is never paid for twice.
- **Replay policy per tool.** An interrupted tool marked as safe (a lookup, reading CI status) runs again automatically. A tool marked as never (a refund, a pull request comment) is not run again. The model is told that the call possibly went through, and it decides whether to check first.
- Harnesses that keep their own session files (Claude Code's transcript, Codex's rollout, OpenCode's event store) are copied record by record into the log, and can be rebuilt from it in a fresh function or sandbox.
- One interface, called a World, provides the three things a durable agent needs: a log, a queue that restarts dead turns, and a stream for whoever is watching. Implementations exist for Vercel, local files, Postgres, MongoDB, Redis and Turso, so the same agent moves between them by configuration.
- A sandbox is not needed for everything. Tools that query a database or call an API can run in the function itself, which keeps their credentials out of any sandbox. For files there are three choices: a virtual workspace kept in the session log, an in-memory scratch space, or a sandbox whose workspace sits on a drive that outlives it. Claude Code and Codex always get a sandbox, because they expect a real shell and are not safe for multi-tenant use.
- Session documents (a plan, a to-do list) are typed data in the log, committed together with the tool result that changed them.
- The closing claim: a harness should be chosen for its prompts, tools and context handling, and how it survives a crash should not be part of that choice.

## What to do with it

- Record intent before an action and outcome after it, so that recovery can tell "never started" from "possibly done".
- Declare for every tool whether it may be repeated. For those that may not, surface the uncertainty to the model instead of guessing.
- Back every turn with a queue so that something outside the process notices its death.
- Keep database and API tools outside the sandbox.

## Terms

- **Intent record** — a log entry written before a call starts.
- **Replay policy** — a tool's declared behaviour after an interruption: run again, or never run twice.
- **World** — Vercel's interface combining the log, the restart queue and the stream.

## Caveats

- A vendor's launch post for a new package, from October 2026, with a demo and no production figures.
- Leaving the decision about a possibly completed call to the model is a design choice whose reliability is not measured here.
