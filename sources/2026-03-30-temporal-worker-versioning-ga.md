---
type: source
title: "Announcing GA for Worker Versioning and Public Preview for Upgrade on Continue-as-New"
author: "Brandon Chavis"
publisher: Temporal
url: https://temporal.io/blog/ga-worker-versioning-public-preview-upgrade-on-continue-as-new
published: 2026-03-30
ingested: 2026-11-17
kind: article
read: full
concepts: [production-operations]
---

# Announcing GA for Worker Versioning and Public Preview for Upgrade on Continue-as-New

**In one line:** Temporal makes deploying under running Workflows a setting per Workflow type, pin or upgrade, and previews a way for very long runs to stay pinned yet change version when they continue as a new run.

## What it says

- The traditional answer, Workflow Patching, puts version branches inside Workflow code, and they accumulate over runs of days to years. Worker Versioning instead has each Workflow type declare a Versioning Behavior.
  - **PINNED.** A run stays on the Worker version where it started for its whole life, on Workers still running the old code.
  - **AUTO_UPGRADE.** Runs move to the newest Worker Deployment Version once it is available.
- The rule of thumb sets run length against deploy frequency. Runs that finish before the next deploy: PINNED, never patched. Runs that span several deploys: AUTO_UPGRADE, with patching. Runs of weeks to years that use Continue-as-New: PINNED plus Upgrade on Continue-as-New, never patched. Runs that long without Continue-as-New: AUTO_UPGRADE plus patching.
- **Upgrade on Continue-as-New** targets month-long entity Workflows and AI agents whose sleeps between interactions last weeks. A run stays pinned, detects that a newer version has become Current or Ramping (`target_worker_deployment_version_changed`), and opts in at its next Continue-as-New, so the successor run starts on the new version.
- Adoption: choose a behaviour per Workflow type, register Workers with a deployment version, and have the deployment pipeline create a new version on every deploy.
- Worker Versioning is generally available in every Temporal SDK. Upgrade on Continue-as-New is in Public Preview.

## What to do with it

- Classify each workflow by run length against deploy frequency, and choose pinning or upgrading per type.
- Give long-lived agent runs a regular hand-over point to a fresh run, and upgrade there.
- Plan for old Workers to stay up while pinned runs remain on them.

## Terms

- **Continue-as-New** — ending a run and carrying on in a fresh one, which resets accumulated Event History.

## Caveats

- A vendor announcement from March 2026, without failure cases or adoption figures. Upgrade on Continue-as-New was in preview and may have changed.
- It does not spell out what pinning asks of operations. Temporal's Worker Versioning documentation (undated) says rolling deployments are incompatible with the feature and that pinned Workflows are designed for rainbow deployments, where older versions run until their Workflows drain.
- [Agent checkpointing is far from production-grade resiliency](2026-06-15-restate-checkpointing-is-not-resiliency.md) takes a firmer line: pin every in-flight run to the deployment it started on. Temporal recommends upgrading with patches for runs that outlive a deploy and do not use Continue-as-New.
