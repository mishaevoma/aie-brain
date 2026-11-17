---
type: source
title: "Redesigning source control at Anthropic"
author: "Nick G., S.G., R.K., Dan C., Garrett H., Ben L., Colin M., Joe P."
publisher: Anthropic
url: https://www.anthropic.com/research/redesigning-source-control
published: 2026-10-13
ingested: 2026-11-17
kind: article
read: full
concepts: [human-judgment, multi-agent-systems, production-operations]
---

# Redesigning source control at Anthropic

**In one line:** Once agents write most of the code, the bottleneck moves to infrastructure built for human-scale traffic. Anthropic replaced git for its monorepo with a centralized, server-side, always-online system called **Scion**.

## What it says

- Merged changes rose from about 2,500 a day in May 2026 to over 30,000 a day by September 2026. Source control, builds and CI, not coding, became the limit.
- The monorepo strained git: almost 100 GB of main-branch history, a compressed working copy over 25 GB, about 25 million CI checkouts a day (over 600 PB if fetched naively). Workarounds (shallow and sparse clones, hundreds of mirrors, snapshot seeds) drifted and broke diff and blame.
- Core insight: git was already used centrally, and nearly every client was an always-online agent or job, so git's offline-first design worked against them.
- Principles (after Google's Piper and Meta's Sapling/Mononoke): always-online clients fetch on demand; the server does history, blame, commits, merges and rebases; an API lets jobs like automated bisect skip checkouts; everything scales horizontally with no packfiles; commits are cheap, lock-free, server-side and cost in proportion to change size; working copies are optional and sparse.
- The unit is a **changeset**, a write-ahead-log entry of files changed from its first parent, with content-addressed blobs. Moving a ref is a compare-and-swap on one Spanner row.
- Daemon, regional cache and server tiers answer the same RPCs, each above 99% cache hits. Against the old git mirrors: about 200x less CPU and memory, checkouts in seconds not minutes, 25% more CI CPU capacity.
- Seven people built Scion, the **Antique** review tool and related systems, migrating in five months while daily merge volume grew 10x.
- Claude wrote most of the code. Engineers set architecture and often said no, e.g. to brute-force scans or over-defensive validation. Reviewers check intent rather than every line. An early **Claude Mythos Preview** snapshot rewrote an ingestion pipeline to use 20x less memory and run 4x faster.
- Merge queues and global locks fail at agent scale. They rely on post-merge and pre-deploy testing and let Claude fix conflicts.
- Scion stays internal. The authors propose git improvements instead, such as standard server-side RPCs and better negotiation.

## What to do with it

- Before adding more agents, check whether source control, CI and review can take 10x the change volume.
- Expose repository queries as APIs so agent jobs don't need full checkouts.
- Expect conflicts and catch regressions after merge, instead of serializing every change.
- Move human review toward intent and architecture, and plan for engineers to spend more time saying no.

## Terms

- **Scion** — Anthropic's in-house version control system (client: **scn**).
- **Changeset** — a server-created, first-parent-relative diff entry in a write-ahead log.

## Caveats

- One huge monorepo with unusual token spend; the authors say Scion is not a general git replacement.
- Internal tools and models (Claude Mythos Preview, Claude Tag) make it unreproducible. Numbers are self-reported, and Anthropic benefits from showcasing agents at scale.
