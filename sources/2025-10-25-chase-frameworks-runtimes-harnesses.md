---
type: source
title: "Agent Frameworks, Runtimes, and Harnesses- oh my!"
author: "Harrison Chase"
publisher: LangChain
url: https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my
published: 2025-10-25
ingested: 2026-11-17
kind: article
read: full
concepts: [harness]
---

# Agent Frameworks, Runtimes, and Harnesses- oh my!

**In one line:** Three words for three layers of agent software: a *framework* gives abstractions, a *runtime* gives the infrastructure for running in production, and a *harness* is a ready-made agent with batteries included.

## What it says

- **Framework**: a library whose value is its abstractions, a shared mental model and a standard way to build. The risk is abstractions that hide what happens and block advanced use. Named examples: LangChain, Vercel's AI SDK, CrewAI, the OpenAI Agents SDK, Google ADK, LlamaIndex.
- **Runtime**: what you need once agents run in production. Durable execution is the main job. Streaming, human-in-the-loop support, and persistence within one thread and across threads belong here too. LangGraph is the author's example, and he names Temporal, Inngest and other durable execution engines as its closest relatives.
- Runtimes sit lower than frameworks and can power them: LangChain 1.0 is built on LangGraph.
- **Harness**: higher level than a framework. It ships default prompts, opinionated tool handling, planning tools and access to a filesystem. DeepAgents is the author's example, described as a general-purpose version of Claude Code. The Claude Agent SDK is the other one he names, and he grants that every coding CLI could count.
- The author says the lines are blurry (LangGraph is both a runtime and a framework), that "harness" is a term he picked up from others, and that none of the three has a settled definition.

## What to do with it

- When comparing tools, ask which layer each one is. A framework, a runtime and a harness are not alternatives to one another.
- Ask the runtime questions separately from the agent's quality: does a run survive a crash, can it pause for a person, where do thread state and cross-thread state live?

## Terms

- **Agent framework** — abstractions for building with models.
- **Agent runtime** — infrastructure for running agents: durable execution, streaming, human-in-the-loop, persistence.
- **Agent harness** — a batteries-included agent: prompts, tools, planning, filesystem.

## Caveats

- Short, and offered as a first attempt. The author maintains one product in each category.
- "Harness" is used more narrowly here than elsewhere in this brain, where the loop itself is part of the harness.
