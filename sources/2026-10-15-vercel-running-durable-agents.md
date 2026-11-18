---
type: source
title: "Running Durable Agents on Vercel"
author: "Anshuman Bhardwaj"
publisher: Vercel Knowledge Base
url: https://vercel.com/kb/guide/durable-ai-agents
published: 2026-10-15
ingested: 2026-11-17
kind: docs
read: full
concepts: [production-operations, side-effects]
---

# Running Durable Agents on Vercel

**In one line:** On Vercel a durable agent keeps run history in the workflow engine, shared records in a database and working files on a drive; deduplicating side effects, authorising approvers and replacing runs pinned to buggy code stay with the application.

## What it says

- **Where state goes.** `WorkflowAgent` runs model calls and the tool loop. Workflow SDK holds execution history, steps, retries, hooks and timers. A database holds application records and memory that several runs share. Vercel Sandbox with Drives holds tool execution and persistent files. Conversation history is the model's context; execution records say which operations completed.
- **Steps.** A `'use step'` function's completed result is persisted; on recovery the `'use workflow'` code runs again and reuses recorded results. A whole agent loop inside one step records nothing until it ends, so model calls and external tools each get a boundary. Only data and identifiers cross boundaries.
- **Approval.** The workflow creates a hook whose token is built from the proposal's id, then calls `getConflict()`. A conflict names the run already waiting on that token (the example throws); `null` confirms registration. Only then does a step expose the request, so an immediate reply finds the hook. The workflow races the hook against a durable timer, `sleep('7d')` in the example, and returns a decision or an expiry. No process runs meanwhile. Server-side code calls `resumeHook()` with the token after authenticating and authorising the reviewer.
- **Repeatable side effects.** An external call can succeed before its result is recorded, so the step may run again. The step reads `stepId` from `getStepMetadata()` and sends it as an `Idempotency-Key` header, which works only if the receiving API enforces it. The id is stable across retries of one invocation and differs between runs; duplicates across runs need a business identifier or a database uniqueness constraint.
- **Deploys.** Deployment pinning keeps each run on the deployment that started it, with its original step definitions; a fix never reaches a run in flight. The advice: cancel affected runs, restart them on the corrected deployment, and first check how the new runs will treat external actions already completed. Schemas and external APIs must stay compatible with old code that may resume later.
- **Workspace.** A drive outlives its sandbox. One sandbox at a time may mount it for writing; several may mount read-only snapshots fixed at mount time. A killed process can leave its sandbox running, so retries must find leftovers.

## What to do with it

- Ask of every tool what happens if it runs twice: reads are safe; publishing, charging and appending need deduplication or a recovery plan.
- Register the wait before exposing an approval request, give it a deadline, and authorise the approver in your own code.
- Before launch, interrupt a run between steps, retry an external action and deploy mid-run, and confirm each recovers.

## Terms

- **Hook** — a point where a run suspends until outside code resumes it with a payload.
- **Deployment pinning** — a run keeps executing the deployment that started it.

## Caveats

- Vendor documentation: patterns and examples, with no limits, costs or failure rates.
- It does not say how long an old deployment stays available to a run that waits for weeks.
