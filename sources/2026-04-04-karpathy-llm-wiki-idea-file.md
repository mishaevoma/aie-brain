---
type: source
title: "LLM Wiki (idea file)"
author: "Andrej Karpathy"
publisher: "GitHub Gist"
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
via: https://x.com/karpathy/status/2040470801506541998
published: 2026-04-04
ingested: 2026-11-17
kind: article
read: full
concepts: [compounding, llm-wiki, retrieval]
---

# LLM Wiki (idea file)

**In one line:** The reference description of the LLM wiki pattern: three layers (raw sources, an agent-owned wiki, a schema file), three operations (ingest, query, lint), and two bookkeeping files (index and log).

## What it says

- The announcing post introduces the **idea file**: you share a description of an idea instead of code, and each person's agent builds a version that fits them. The gist is deliberately abstract.
- The contrast is with retrieval at question time (NotebookLM, file uploads, most RAG systems), where the model re-derives everything on each question and nothing accumulates. In the wiki pattern, knowledge is compiled once and kept current.
- **Three layers:**
  - Raw sources: curated and immutable. The model reads them and never edits them. They are the source of truth.
  - The wiki: markdown the model writes and owns. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis.
  - The schema: a file such as `CLAUDE.md` or `AGENTS.md` that defines structure, conventions and workflows. The person and the model refine it together.
- **Three operations:**
  - Ingest: the model reads a new source, discusses the takeaways, writes a summary page, updates the index and the affected pages, and appends to the log. One source can touch 10 to 15 pages. He prefers one source at a time with supervision.
  - Query: the model reads the index, finds and reads relevant pages, and answers with citations. Good answers are filed back as new pages.
  - Lint: periodic checks for contradictions, claims overtaken by newer sources, orphan pages, concepts without a page, missing cross-references, and gaps a web search could fill.
- **Two files:**
  - `index.md` lists every page with a link and a one-line summary, grouped by category, updated on every ingest and read first on every query. He reports this working at about 100 sources and hundreds of pages without embeddings.
  - `log.md` is append-only and chronological. Entries start with a fixed prefix (date, operation, title) so they can be read with `grep` and `tail`.
- Search tooling is optional and comes later. He names `qmd`, a local markdown search engine with a CLI and an MCP server.
- Why it works: the cost of a knowledge base is bookkeeping, which people give up on. A model does not tire of it. The person curates sources and asks questions.
- Suggested uses include research, personal notes, reading a book, and team wikis fed by chat threads and meeting transcripts.

## What to do with it

- Write the schema file first and keep improving it; it is what makes the agent a consistent maintainer.
- Update the index and log on every change. They are what replace retrieval infrastructure.
- Schedule lint passes. Stale and contradictory pages are the main way a wiki decays.
- Treat the gist as a starting point to adapt.

## Terms

- **Idea file** — a description of a pattern written to be handed to an agent.
- **Schema** — the instruction file that tells the agent how the wiki is organised and maintained.
- **Ingest / query / lint** — the three operations on the wiki.

## Caveats

- A pattern, not an implementation, and the scale claim is his own experience.
- Fetched through a summarising tool; the last few hundred characters of the page (after the gist body) were not read.
