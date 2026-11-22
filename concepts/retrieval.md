---
type: concept
title: "Retrieval"
updated: 2026-11-22
reviewed: 2026-11-17
status: evolving
---

# Retrieval

**Definition:** Getting the right outside information into the context window when it is needed. The three main routes are a pre-built index queried at question time (RAG), search tools the agent drives itself, and a knowledge base compiled ahead of time.

## Why it matters

Most AI products depend on information the model was not trained on. The route you choose decides cost, freshness and whether the system gets better with use or re-derives everything on each question. [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)

## What to do

- For a small corpus, skip retrieval. Put all of it in a cached prompt. The threshold given in 2024 was about 200,000 tokens, which reflects the context windows and prices of that time. For material inside an agent loop, see "Where sources disagree" below. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- If you build an index, start with hybrid search: embeddings plus BM25, which catches exact identifiers such as error codes. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- Use contextual retrieval: add a short note on where each chunk sits in its document before indexing, written by a small model with the whole document cached. With reranking this cut failed retrievals by 67% in Anthropic's tests, averaged over four kinds of corpus, with Claude 3 Haiku writing the notes. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- Rerank a wide first pass (150 candidates) down to about 20. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- Keep the final list short. One passage on the right topic that does not answer the question lowered accuracy, and four lowered it further. Applying that to retrieved lists is this brain's reading, since the report tested no retriever. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- For agents, prefer just-in-time retrieval: give the agent search tools and let it pull what it needs, using file names, sizes and dates as signals. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Do not copy data that has a complete and current system of record. Leave it there and maintain data access guidance: which source holds what, and how to query it. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- For a domain you return to, compile the knowledge once into a maintained wiki. See [LLM wiki](llm-wiki.md). [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md) · [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)
- At large scale, combine a wiki with search. In Anthropic's test on a corpus of about 350,000 files, with its own models building the wiki, search alone answered 53% of questions, a wiki alone 48%, and both together 61%, with the wiki saving about 20,000 tokens per question. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Do not expect a wiki to help when the answer sits in a single document. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Apply the same thinking to tools: with many tools, let the model retrieve definitions on demand. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)

## Where sources disagree: in the prompt, or on demand?

- **Put it all in the prompt.** A knowledge base small enough to fit goes into the prompt whole, with prompt caching, and no retrieval is built. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- **Load it on demand.** Recall falls as the context grows, so give an agent references and search tools instead of loading whole corpora up front. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md) Whatever is always loaded costs tokens in every session and spreads its errors. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- **Measured since.** A full chat history of about 113k tokens, under the 2024 threshold, did worse than about 300 relevant tokens on every model tested, each in a single call. The relevant parts were picked by hand, so that gap is the most selection could gain. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)

This brain's reading, which is a synthesis and not a source claim: the two answer different jobs. The first is one question-answering call over a knowledge base, where nearly every request needs the material. The second is an agent loop, where the material would ride along on every step and most steps do not need it. The measurement adds a third case: one call over material that is mostly irrelevant to the question, which also loses. What decides it is the share of the material that a request uses. So:

- Send it whole when nearly every request needs most of it and the job is one call.
- Make it a search tool or a [skill](skills.md) when it would sit in a loop whose steps mostly do not use it.
- Do not expect caching to settle the question. A cached prompt costs less and answers sooner, but the model still has to attend to all of it.
- When unsure, run both against the same [eval](evals.md) and keep the one that scores better.

## What is changing

- The 2024 view was a pipeline built in advance. By late 2025 the emphasis for agents had moved to search the agent runs itself. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md) · [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- In 2026, compiled wikis became a named pattern, with vector search added only once the collection is very large. [Karpathy, 2 Apr 2026](../sources/2026-04-02-karpathy-llm-knowledge-bases.md) · [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md) · [Tan, May 2026](../sources/2026-05-16-tan-gbrain.md)

## Related

[LLM wiki](llm-wiki.md) · [Knowledge factory](knowledge-factory.md) · [Context engineering](context-engineering.md) · [Memory](memory.md) · [Skills](skills.md) · [Evals](evals.md)
