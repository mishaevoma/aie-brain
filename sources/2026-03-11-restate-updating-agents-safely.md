---
type: source
title: "Updating AI Agents safely in production"
author: "Giselle van Dongen, Francesco Guardiani"
publisher: Restate
url: https://restate.dev/blog/dealing-with-versioning-in-long-running-agents
published: 2026-03-11
ingested: 2026-11-17
kind: article
read: full
concepts: [production-operations]
---

# Updating AI Agents safely in production

**In one line:** Prompts, tool descriptions and schemas are the manual a model uses to read its own history, so changing them under a running agent corrupts decisions silently; deploy versions immutably and pin each in-flight run to the version it started on.

## What it says

- **The example.** A fraud agent's `compute_risk_score` tool scores 0 to 10 and returns 8. Before the result reaches the model, a redeploy changes the scale to 0–100. On resuming, the agent sends stored history with the new tool description, the model reads 8 as nearly clean, and the transaction passes, with no crash or warning.
- Changed schema descriptions, prompts, guardrails (an approval granted under one policy counts under another) and removed tools fail in the same silent way.
- **Why it is hard.** History lives in a database and its interpretation in code: one state, versioned separately, branching inside the model's reasoning where code cannot gate it. Runs can take weeks awaiting approvals, so they overlap with releases; SDKs that resume from session history (LangChain and ADK are named) resume onto whatever is deployed.
- **What falls short.** Version markers in state with branches in code may do for deserialising tool inputs and outputs, not for prompts and descriptions, since the loop writes its own next step. Keeping tasks short still leaves a history to be read across versions.
- **Recommended: two infrastructure rules.** Immutable deployments: each version is a complete snapshot (code, prompts, schemas, tool definitions, guardrails, model configuration) at its own endpoint, beside the old ones. Pinned executions: each retry, resumption or callback goes back to the starting version; only new requests go to the latest.
- **Loud, not silent.** Restate journals each non-deterministic step. If the environment conflicts with the journal, replay detects it and the execution fails visibly.
- **Old versions.** A published AWS Lambda version costs nothing to keep, scales to zero and wakes when an approval arrives a month later; patches and cold starts are still owed. On Kubernetes parallel versions consume resources; Restate's operator deploys new versions, drains old ones and decommissions them once idle. Short executions drain within minutes or hours; per-version counts of in-flight invocations show when removal is safe.
- **Escape hatches.** Overriding the pin is a deliberate, auditable operation: move runs off a version with a critical bug, cancel and restart a run stuck on a callback, or migrate off retiring infrastructure. For runs lasting weeks or months it names a cancel-rollback-restart move to a new deployment.

## What to do with it

- Version prompts, tool descriptions, schemas, guardrails and model settings with the code as one release.
- Pin in-flight runs to their starting deployment; send only new runs to the new one.
- Retire a version only when its in-flight count is zero.
- Decide in advance who may override a pin, and log each override.

## Terms

- **Pinning** — keeping a run on the deployment it began on through every retry and resumption.

## Caveats

- Vendor post on Restate's mechanism. It does not say which changes replay detects; its own example, a reworded description with unchanged steps, is the hard case.
- Rolling back a bad release is not covered; cancel-rollback-restart is left to another post.
