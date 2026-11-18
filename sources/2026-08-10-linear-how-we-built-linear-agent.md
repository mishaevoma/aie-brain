---
type: source
title: "How we built Linear Agent"
author: "Matthijs Wolting"
publisher: Linear
url: https://linear.app/now/how-we-built-linear-agent
published: 2026-08-10
ingested: 2026-11-17
kind: article
read: full
concepts: [multi-agent-systems, side-effects]
---

# How we built Linear Agent

**In one line:** Linear built its own agent loop on a durable workflow engine because harness libraries fix a run's flow, and it needed to change runs in progress: inject tools mid-run, decide approval from context, and suspend a parent while its sub-agent works.

## What it says

- **Constraints go into tools, not prompts.** Tools are shaped so that invalid actions are impractical. A coding agent has a few deep tools that models know well; Linear Agent has many shallow ones over product concepts the model barely knows, so each feature ships tools, an explanation of its data and principles for using it.
- **System skills** bundle metadata, a system prompt fragment and tools. Likely ones are preloaded from the prompt and the invocation context; the agent loads others mid-task.
- **Typed tools over raw access.** Giving the agent the Linear SDK plus a coding environment, the GraphQL API or a CLI was considered and rejected. It would arguably enable more sophisticated behaviour, and more mistakes: the data model permits a wide range of actions, some UI concepts need interpreting before they map to it, and on long-tail requests an agent with no obvious path may try increasingly speculative actions. Predictability is bought with breadth: the agent will occasionally refuse a task.
- **The stack.** Linear owns every layer above the model providers' APIs: a provider-agnostic client with one wire and storage format for threads, the agent loop, which runs on a durable workflow engine, and a streaming and storage layer.
- **Why not a harness library.** Libraries tend to assume one flow: supply a prompt and tools, call run, wait for the answer. Three behaviours needed control during a run:
  1. **Tool injection.** Tools from a skill loaded mid-run must be callable as soon as the loading call resolves, without breaking the provider's prefix cache.
  2. **Conditional approval.** For risky or hard-to-undo actions the agent pauses mid-run and asks the user. Most libraries decide this from the tool name and parameters alone; Linear wanted context. The agent may delete, unasked, something it made earlier in the same conversation, but must confirm before deleting an issue that already existed. Most comment threads can be posted to without approval; a thread synced to a public repository cannot.
  3. **Suspended parents.** A sub-agent call looks synchronous to the parent, but the parent's turn is suspended mid-tool-call so it holds no server resources, and it resumes when the work is done.

## What to do with it

- Before adopting a harness library, list what must change while a run is in progress.
- Decide approval from context: who created the object, and who will see the result.
- When adding tools mid-run, check that the prefix cache still hits.
- Prefer narrow typed tools where a wrong action is costly, and accept some refusals.

## Terms

- **System skill** — one of Linear's built-in skills, as distinct from skills that users write.

## Caveats

- A vendor's account from August 2026 with no figures for cost, cache hits, approvals or errors.
- The workflow engine is not named, and nothing is said about how suspension, storage or recovery work.
- The post concedes that library harnesses can do all this, with awkward workarounds.
