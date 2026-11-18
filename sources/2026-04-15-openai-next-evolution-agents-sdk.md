---
type: source
title: "The next evolution of the Agents SDK"
author: "OpenAI"
publisher: OpenAI
url: https://openai.com/index/the-next-evolution-of-the-agents-sdk/
published: 2026-04-15
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms]
---

# The next evolution of the Agents SDK

**In one line:** OpenAI's agent SDK now ships a harness tuned to its own models and runs the agent's work in a sandbox kept separate from that harness, so credentials stay out of generated code and a lost container does not lose the run.

## What it says

- The post frames three existing options and what each costs. Model-agnostic frameworks are flexible but do not use frontier models fully. Model-provider SDKs sit close to the model but show little of the harness. Managed agent APIs are easy to deploy but limit where agents run and how they reach sensitive data.
- The harness gains configurable memory, sandbox-aware orchestration and Codex-like file tools, with standard support for MCP, skills, `AGENTS.md`, a shell tool and an apply-patch tool. The claim is that matching execution to how the models work best improves reliability on long tasks.
- Native sandbox execution: bring your own sandbox, or use built-in support for Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop and Vercel.
- A *Manifest* describes the agent's workspace in a way that is portable across providers: mounted local files, output directories, and data from AWS S3, Google Cloud Storage, Azure Blob Storage and Cloudflare R2.
- Harness and compute are separated, for three stated reasons.
  - Security: assume prompt injection and exfiltration attempts, and keep credentials out of the environment where model-written code runs.
  - Durability: with the agent's state held outside the sandbox, snapshotting and rehydration restore a run in a fresh container from the last checkpoint when the original fails or expires.
  - Scale: one sandbox or many, started only when needed, with subagents routed to their own environments.
- Generally available at standard API pricing. Python first, TypeScript later. Code mode and subagents are planned.

## What to do with it

- Keep the loop and its secrets outside the sandbox, and treat the sandbox as replaceable.
- Describe the workspace declaratively, so the same agent runs locally and on any sandbox provider.
- Weigh the three options by control: where the agent runs and what data it can reach.

## Terms

- **Manifest** — a provider-neutral description of an agent's workspace.
- **Rehydration** — restoring a run's state into a new container.

## Caveats

- A product announcement with little detail on mechanisms, limits or failure cases, and no measurements.
- Published a week after Anthropic's [Managed Agents article](2026-04-08-anthropic-managed-agents.md). It reaches the same split between harness and sandbox from the SDK side.
