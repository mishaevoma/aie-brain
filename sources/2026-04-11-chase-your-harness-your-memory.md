---
type: source
title: "Your harness, your memory"
author: "Harrison Chase"
publisher: LangChain
url: https://www.langchain.com/blog/your-harness-your-memory
published: 2026-04-11
ingested: 2026-11-17
kind: article
read: full
concepts: [managed-agent-runtimes, memory]
---

# Your harness, your memory

**In one line:** Whoever runs your agent's harness holds its memory, and memory is the part that is hard to move, so a closed or hosted harness is a lock-in decision and not only a hosting one.

## What it says

- Harnesses are how agents are built now and will stay. Scaffolding that was needed in 2023 has gone, and other scaffolding replaced it. The author's evidence: the leaked Claude Code source ran to 512k lines, all of it harness. Features such as web search inside a model API are a light harness behind that API, not part of the model.
- Memory cannot be bolted on as a separate service today, because managing context is the harness's core job. The harness decides how instruction files load, how skills are shown, what survives compaction, whether interactions are stored and searchable. The post leans on an argument by Sarah Wooders of Letta for this.
- Three degrees of giving memory away:
  - Mildly bad: a stateful API, such as OpenAI's Responses API or Anthropic's server-side compaction. State sits on the provider's servers, so you cannot switch models and resume old threads.
  - Bad: a closed harness, such as the Claude Agent SDK. It writes artifacts whose shape you do not know, so they do not transfer to another harness.
  - Worst: the whole harness, long-term memory included, behind an API. Claude Managed Agents is the named example. Codex is open source but writes an encrypted compaction summary that is unusable elsewhere.
- Why providers do this: switching models has been easy because the APIs were stateless. State is what makes switching hard. Memory gives lock-in that the model alone does not.
- Why builders should care: memory is what lets an agent improve with use and fit each user. Without it the product can be copied by anyone with the same tools. With it you accumulate a dataset of interactions and preferences. An anecdote: the author's email assistant was deleted by accident, and a fresh one from the same template was much worse.
- The author's answer is an open harness: open source, model-agnostic, built on open standards (`AGENTS.md`, skills), with memory in a database you choose, and self-hostable.

## What to do with it

- Before adopting a hosted agent service, list what state it keeps (threads, compaction summaries, long-term memory) and whether you can export each in a usable form.
- Keep long-term memory in storage you control, in a format another harness could read.
- Treat a stateful model API as a commitment to that provider for the life of its threads.

## Terms

- **Open harness** — a harness whose code and stored state you can inspect, move and host yourself.
- **Stateful API** — a model API that keeps conversation state on the provider's side.

## Caveats

- The author sells an open harness and a hosting product for it, so the argument is also a pitch.
- Published three days after Anthropic's [Managed Agents article](2026-04-08-anthropic-managed-agents.md), which it answers. It predates later changes to that product, such as sandboxes that customers host themselves.
