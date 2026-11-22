---
type: source
title: "Continual learning for AI agents"
author: "Harrison Chase"
publisher: "@hwchase17 on X"
url: https://x.com/hwchase17/status/2040467997022884194
published: 2026-04-04
ingested: 2026-11-17
kind: x-article
read: full
concepts: [agents-and-workflows, compounding, context-layer, harness, knowledge-factory, memory]
---

# Continual learning for AI agents

**In one line:** An agent system can improve at three layers (model, harness, context), and the context layer, which is what people usually call memory, is the one you can change yourself.

## What it says

- Three layers of an agent system:
  - **Model**: the weights.
  - **Harness**: the code that drives every instance of the agent, plus instructions and tools that are always part of it.
  - **Context**: instructions, skills and tools that live outside the harness and configure it.
- Mapped to Claude Code: the model is a Claude model, the harness is Claude Code, the context is `CLAUDE.md`, skills and `mcp.json`. Mapped to OpenClaw: many models, a harness built on Pi, and context in `SOUL.md` plus skills.
- Learning at the model layer means training (supervised fine-tuning, reinforcement learning). The open problem is catastrophic forgetting. It is normally done once for the whole agent, not per user.
- Learning at the harness layer means changing the harness code. He cites the Meta-Harness paper: run the agent on tasks, evaluate, store the logs as files, and have a coding agent read the traces and propose harness changes.
- Learning at the context layer is what is commonly called memory. It can happen per agent (OpenClaw updating its own `SOUL.md`), per tenant (user, team or organisation), or at several levels together.
- Context updates happen in two ways:
  - Offline, as a job over recent traces that extracts lessons. OpenClaw calls this "dreaming".
  - In the hot path, while the agent works, either on its own judgement or when the user asks it to remember.
- A second axis is how explicit the update is: the user says "remember this", or the harness instructs the agent to remember on its own.
- All three kinds of learning are fed by **traces**, the full record of what the agent did.

## What to do with it

- When you want an agent to "learn", decide which layer you mean. For most teams it is the context layer.
- Keep traces. Without a record of what the agent did, none of the three kinds of learning is possible.
- Choose deliberately between memory written during the task and memory written by an offline pass, and between explicit and automatic updates.
- Scope memory on purpose: agent, user, team, organisation.

## Terms

- **Context layer** — configuration outside the harness (instructions, skills, tools); what "memory" usually refers to.
- **Dreaming** — an offline pass over past traces that updates memory.
- **Hot-path memory** — memory the agent writes while doing the task.
- **Trace** — the full execution record of an agent run.

## Caveats

- The author runs LangChain; the article ends by pointing to LangSmith for traces and Deep Agents as a harness.
- The comparison table in the original was an image and was not read.
- Anthropic's Nov 2026 article on agent memory covers the same ground from the model maker's side.
