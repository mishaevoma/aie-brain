---
type: concept
title: "LLM wiki (wiki memory)"
updated: 2026-11-22
reviewed: 2026-11-17
status: evolving
---

# LLM wiki (wiki memory)

**Definition:** A knowledge base that an agent compiles from raw sources and keeps current as linked markdown files, so later agents read a maintained synthesis instead of re-deriving it from the raw material. This repository is one.

## Why it matters

The expensive part of a knowledge base is bookkeeping: cross-references, summaries, consistency. People give up on it. A model does not tire of it, so the maintenance cost drops close to zero and knowledge accumulates instead of being rebuilt on every question. [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)

## The pattern

It was published as an *idea file*: a description meant to be handed to an agent, which builds a version that fits its owner. [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)

Three layers [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md):

- **Raw sources**: curated and never edited by the model.
- **The wiki**: summaries, concept pages and an overview, written and owned by the model.
- **The schema**: an instruction file that defines structure, conventions and workflows.

Three operations [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md):

- **Ingest**: read a source, write its summary, update every page it touches, update the index, append to the log.
- **Query**: read the index, read the relevant pages, answer with citations. File good answers back.
- **Lint**: look for contradictions, claims overtaken by newer sources, orphan pages, missing pages and gaps.

Two bookkeeping files: an index of every page with a one-line summary, read first on every query, and an append-only log. [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)

## What to do

- Use files. They can be inspected, edited, versioned, and read and written by any agent. [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md)
- Write the schema first and keep refining it. It is what makes the agent a consistent maintainer. [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)
- Start without a vector database. An index the model maintains was enough at about 100 sources. Add search when the index stops being enough. [Karpathy, 2 Apr 2026](../sources/2026-04-02-karpathy-llm-knowledge-bases.md) · [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)
- Keep the wiki in its own folder or vault, apart from notes you write yourself. Any markdown viewer works as the front end. [kepano, Apr 2026](../sources/2026-04-02-kepano-obsidian-as-agent-wiki.md)
- Run lint passes on a schedule, and check pages against their sources. A wrong note keeps misleading the agent until something corrects it. [Karpathy, 2 Apr 2026](../sources/2026-04-02-karpathy-llm-knowledge-bases.md) · [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Give concurrent writers one page each. Agents writing to a single shared table kept 41 of 57 facts; one page per item kept all 57. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)

## Limits

- It suits durable domain knowledge. It is not the place for conversation state, user preferences or high-frequency event logs. [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md)
- The evidence for "no search needed" is one person's experience at about 100 sources. At hundreds of thousands of files, a wiki works best alongside search. [Karpathy, 2 Apr 2026](../sources/2026-04-02-karpathy-llm-knowledge-bases.md) · [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- Maintaining the wiki costs tokens and can introduce errors of its own. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)

## Variants

- Generated documentation for codebases, such as DeepWiki and AutoWiki. [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md)
- Large personal knowledge systems with extra layers on top of files. [Tan, May 2026](../sources/2026-05-16-tan-gbrain.md)
- Organisational knowledge behind a shared company agent. [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md)
- A [knowledge factory](knowledge-factory.md): company skills and domain knowledge kept current by a curator agent. It adds two inputs to the wiki's maintenance beside the raw sources: traces of agents at work, and the gaps those agents flag. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

## How this repository adapts it

It is public, so full source texts stay out of git. `sources/` holds our own summary of each source with a link, and `raw/` is a local, ignored inbox. The schema is [AGENTS.md](../AGENTS.md).

## Related

[Memory](memory.md) · [Knowledge factory](knowledge-factory.md) · [Retrieval](retrieval.md) · [Instruction files](instruction-files.md) · [Compounding](compounding.md)
