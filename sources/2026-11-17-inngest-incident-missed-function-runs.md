---
type: source
title: "Incident report for November 12, 2026 - Missed function runs"
author: "Inngest"
publisher: Inngest
url: https://www.inngest.com/blog/2026-11-17-incident-report-for-november-12-2026
published: 2026-11-17
ingested: 2026-11-17
kind: article
read: full
concepts: [durable-execution]
---

# Incident report for November 12, 2026 - Missed function runs

**In one line:** On Inngest Cloud a failed enqueue left a deduplication marker behind without its run, so redelivered events were skipped as duplicates and functions never started: event visible, no run, no failure record.

## What it says

- **Scope.** Between 19:25 and 19:43 UTC on 12 November 2026, some events that Inngest Cloud had accepted and stored never started their function runs. A subset of customers was affected. Enterprise workloads on Dedicated Infrastructure have separate queue shards and were not.
- **First failure.** During a rollout, one instance of the internal queue router, queue-proxy, timed out resolving one shard's address at startup. It served traffic anyway with that shard absent from its routing table, so scheduling failed for requests that crossed it and needed that shard.
- **Timeline (UTC, 12 November).** 19:24:58 the instance starts. 19:25:06 its DNS lookup times out. 19:25:20 first queue routing error. 19:43:23 last routing error from that instance.
- **Root cause.** After the failed enqueue the scheduler cleared the run state but left the marker that guards against duplicate execution. On redelivery it took the marker as proof that the run was already handled, so it did not retry.
- **What customers saw.** The event in the dashboard, with no run and no failure record beside it.
- **Detection.** The timeline's only detection entry is for 13 November: reports of missing runs were investigated.
- **Repairs.** The 13 November release stops an unavailable shard from failing run scheduling in this edge case, and monitoring of queue routing failures was improved. Nothing further is promised. Customers still missing a run may need the events replayed, with help from support.

## What to do with it

- Set and clear a deduplication marker together with the state it protects. It should mean "work durably handed off", never "attempt made".
- Reconcile events sent against runs started, on your own side too when the runtime is hosted. A silent skip leaves no failure to alert on.
- Do not let a router serve traffic with an incomplete routing table.

## Terms

- **queue-proxy** — Inngest's internal service that routes each queue request to the right shard.

## Caveats

- The vendor's own brief account, published five days after the incident.
- Not disclosed: how many events, runs or customers were affected; who reported the missing runs, and when; why the DNS lookup timed out, or why errors stopped at 19:43:23; what changed in the scheduler; whether Inngest replayed anything itself.
- This brain's reading: no failure was recorded because the run state was gone and the skip was treated as ordinary deduplication. The report shows no detection on the day, only reports investigated on the next, which suggests internal alerting missed it.
