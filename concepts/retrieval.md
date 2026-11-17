---
type: concept
title: "Retrieval"
updated: 2026-11-17
reviewed: 2026-11-17
status: evolving
---

# Retrieval

**Definition:** Getting the right outside information into the context window when it is needed. The three main routes are a pre-built index queried at question time (RAG), search tools the agent drives itself, and a knowledge base compiled ahead of time.

## Why it matters

Most AI products depend on information the model was not trained on. The route you choose decides cost, freshness and whether the system gets better with use or re-derives everything on each question. [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)

## What to do

- For a small corpus, skip retrieval. Put all of it in a cached prompt. The threshold given in 2024 was about 200,000 tokens, which reflects the context windows and prices of that time. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- If you build an index, start with hybrid search: embeddings plus BM25, which catches exact identifiers such as error codes. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- Use contextual retrieval: add a short note on where each chunk sits in its document before indexing, written by a small model with the whole document cached. With reranking this cut failed retrievals by 67% in the original tests. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- Rerank a wide first pass (150 candidates) down to about 20. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- For agents, prefer just-in-time retrieval: give the agent search tools and let it pull what it needs, using file names, sizes and dates as signals. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- For a domain you return to, compile the knowledge once into a maintained wiki. See [LLM wiki](llm-wiki.md). [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md) · [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)
- At large scale, combine a wiki with search. On a corpus of about 350,000 files, search alone answered 53% of questions, a wiki alone 48%, and both together 61%, with the wiki saving about 20,000 tokens per question. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Do not expect a wiki to help when the answer sits in a single document. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Apply the same thinking to tools: with many tools, let the model retrieve definitions on demand. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)

## What is changing

- The 2024 view was a pipeline built in advance. By late 2025 the emphasis for agents had moved to search the agent runs itself. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md) · [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- In 2026, compiled wikis became a named pattern, with vector search added only once the collection is very large. [Karpathy, 2 Apr 2026](../sources/2026-04-02-karpathy-llm-knowledge-bases.md) · [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md) · [Tan, May 2026](../sources/2026-05-16-tan-gbrain.md)

## Related

[LLM wiki](llm-wiki.md) · [Context engineering](context-engineering.md) · [Memory](memory.md)
