---
type: source
title: "Wiki Memory"
author: "Harrison Chase"
publisher: "@hwchase17 on X"
url: https://x.com/hwchase17/status/2071963622298050997
published: 2026-06-30
ingested: 2026-11-17
kind: x-article
read: full
concepts: [llm-wiki, memory, retrieval]
---

# Wiki Memory

**In one line:** Names the emerging pattern for long-term agent memory: an agent compresses raw source material into a persistent set of files that later agents read, instead of retrieving raw chunks at question time.

## What it says

- Agent memory has few standards and means different things to different people. One pattern keeps appearing, which he calls **wiki memory**.
- Raw material (logs, notes, code, docs, experiments, chat threads, transcripts) holds the knowledge but is too large and noisy to hand to an agent directly. So a process turns it into something denser.
- The difference from basic RAG: RAG fetches raw chunks when asked. A wiki computes and maintains a higher-level synthesis ahead of time, so the agent does not have to rediscover the structure on every question.
- His definition of a wiki: a data structure maintained by an agent that represents source knowledge in a form agents can use. It does not need to look like Wikipedia. What matters is that it is persistent, structured, inspectable and updated over time.
- Examples he lists: DeepWiki from Cognition (generated documentation for GitHub repositories), Karpathy's LLM wiki (the same idea over arbitrary files), and Factory's AutoWiki (codebase documentation that stays current).
- Memory products such as LangMem, Letta, Mem0 and Zep address the wider memory problem. Wiki memory stands out for using the simplest storage available: files.
- The common answers to the design questions: the raw data is anything an agent can read; the compressed form is files; an agent does the compressing; an agent does the maintenance.
- Files win because they can be inspected, edited, versioned, and read and written easily by agents.
- Wikis are not all of memory. They suit durable domain knowledge, not short-term conversation state, user preferences or high-frequency event logs.

## What to do with it

- For a domain you work in repeatedly, build the compressed knowledge base once and maintain it, instead of pointing an agent at the raw pile each time.
- Use files in a repo before reaching for a memory product.
- Keep other kinds of memory (preferences, conversation state, event logs) in mechanisms suited to them.

## Terms

- **Wiki memory** — durable domain knowledge held as agent-maintained files.
- **Wiki** — in this sense, any persistent, structured, inspectable knowledge layer an agent keeps up to date.

## Caveats

- A short framing article. It names the pattern and does not evaluate it.
- The author runs LangChain, which sells agent tooling including memory.
