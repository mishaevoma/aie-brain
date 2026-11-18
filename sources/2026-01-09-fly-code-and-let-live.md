---
type: source
title: "Code And Let Live"
author: "Kurt Mackey"
publisher: Fly.io
url: https://fly.io/blog/code-and-let-live/
published: 2026-01-09
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, durable-execution, long-running-agents]
---

# Code And Let Live

**In one line:** Fly.io argues that an agent needs a durable computer, not a sandbox destroyed after each job, and presents Sprites: machines created in a second or two that sleep when idle, keep their disk and restore a checkpoint in about a second.

## What it says

- **The claim.** The read-only, ephemeral sandbox, which Fly.io sold for years as agent isolation, is obsolete. Stop destroying the sandbox after every use.
- **Why.** Stateless instances, with persistent data confined to database servers, buy simplicity, scale-out and a smaller blast radius, and suit professional developers, not agents. A computer, by the author's test, need not vanish when a job completes and has durable storage. Current agent sandboxes are said to fail both.
- **Sprite.** A Linux machine with a root shell. `sprite create` reports 1.0s in the demonstration, and creating hundreds takes 1–2 seconds each. It starts with 100GB of capacity, sleeps and stops metering when idle, can get an HTTPS URL, and lives until deleted. An installed package survived a sleep of days.
- **Checkpoint and restore.** Creating a checkpoint is called instant but was not measured. A restore took about one second, fast enough to be routine.
- What agents do badly on a disposable machine:
  - They rebuild the development environment (`node_modules` is the example) for every pull request. The industry is said to spend tens of millions of dollars on snapshotting and restoring sandboxes, which the author calls solvable but unnecessary.
  - Teams run S3 buckets, Redis servers or RDS instances outside the sandbox, because a file written inside does not stay.
  - Ephemerality means time limits. The author guesses the 99th percentile sandboxed run needs under 15 minutes, but some tasks are dominated by compute and network time.
  - State travels between runs in "plan files", prose used as a key-value store.
  - The agent cannot watch what it built. Phoenix.new's agent sits on a Fly Machine, where it sees the generated app's logs and investigates exceptions.
- **The larger bet.** People will own small applications that an agent keeps changing, with development and production on one machine.
- **Stated limits.** An app for millions of people does not belong on a Sprite. Most of the author's team does not believe the larger bet. He says outright that he is selling something.

## What to do with it

- List what your agent rebuilds, downloads again or stores elsewhere on every run: that is the price of a disposable sandbox.
- Check the sandbox's time limit against tasks dominated by compute or network waits.
- On a writable machine, checkpoint before risky changes and restore instead of repairing.

## Terms

- **Sprite** — Fly.io's durable Linux machine with checkpoint and restore.

## Caveats

- A vendor's launch post, January 2026. Timings come from a demonstration; the 15 minutes and the tens of millions are unsourced. No prices, nothing on isolation.
- It does not say whether running processes survive a sleep or a restore; only files on disk are shown surviving. See [SBD: We Have a Filesystem at Home](2026-10-22-fly-sprites-block-device.md).
- Opposite designs: [Under the River](2026-05-28-shopify-under-the-river.md) (disposable sandbox, session log as the record) and [Why We Built Our Own Background Agent](2026-01-12-ramp-background-agent.md) (the snapshot-and-restore this post calls unnecessary).
