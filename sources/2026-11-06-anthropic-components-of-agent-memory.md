---
type: source
title: "The components of agent memory"
author: "Lance Martin"
publisher: Anthropic
url: https://www.anthropic.com/research/components-of-agent-memory
published: 2026-11-06
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, knowledge-factory, llm-wiki, memory, retrieval]
---

# The components of agent memory

**In one line:** Treat agent memory as layers: raw transcripts, notes, wikis and a small always-loaded context. Recent models write good notes if you tell them what memory is for, and an offline "dreaming" pass that checks, reorganizes and promotes notes adds much of the remaining value.

## What it says

- Memory here means knowledge from experience that persists across sessions as readable context. It excludes weight updates, in-context learning and compaction.
- Four layers, bottom to top: searchable **transcripts**, **memory notes**, **memory representations** such as wikis, and **injected context** loaded into every session. **Dreaming**, offline reorganization modelled on sleep consolidation and related to sleep-time compute, moves information between layers.
- Writing a note is a prediction that it will matter later. On CL-Bench 1.0 (a database Q&A task with fresh sessions and a persistent memory folder), mean reward went from baseline to with-memory as follows: Opus 5.5 0.655→0.838, Sonnet 5.5 0.644→0.833, Opus 5 0.564→0.828, Opus 4.7 0.383→0.700, Sonnet 5 0.306→0.610, Sonnet 4.6 0.330→0.364. Opus 5 was the first model to close the loop: record the failure, test a theory, and store a verified rule.
- Salience judgment improved. At about 10,000 steps of Pokémon Red, Sonnet 3.7 had 413 files in 225 folders, one badge, and was spending steps on upkeep. Claude Fable 5 kept 10 small files of strategy, plans and tested rules (what the screen doesn't show) and had four badges.
- Steering: say what memory is for, not how to use it. A "record only failures" rule cut strong models' memory gain sharply (Opus 5 lost 0.234). Older models need explicit steps: telling Sonnet 4.6 to read memory first and test theories raised it to 0.641.
- What dreaming does:
  - **Corrects:** checks notes against transcripts. A wrong Mt. Moon note kept trapping the agent; once fixed, it reached Cerulean (action 1,935), which uncorrected and no-memory runs never did.
  - **Builds wikis:** on the Stainless corpus (about 350,000 files, ~420M tokens), wiki-only scores rose from 13% to 48% as dreaming scaled from 2 to 128 Opus 5 sessions. Search alone: 53%; search plus wiki: 61%, saving about 20,000 tokens per question. On a Harvey LAB merger set, 87% with the wiki vs 73% search alone. No gain when answers sat in one document; one wiki outgrew its source.
  - **Promotes:** the top layer must stay small, since preloaded notes cost tokens and spread errors. Claude Code auto memory loads only the first 200 lines or 25 KB of `MEMORY.md`, used as an index.
  - **Focuses:** agents writing concurrently to one shared table kept 41 of 57 contract facts; one page per contract, quoted verbatim, kept all 57.
  - **Fills gaps:** a second pass fixed nine dangling wiki links.
- Open questions: write memory during the task or offline, how often to re-verify, and the cost and error risk of maintaining representations.

## What to do with it

- Keep transcripts searchable as ground truth under any notes.
- Give frontier models a memory folder and a one-line purpose, not rigid write rules.
- Run an offline pass that checks notes against transcripts.
- Keep always-loaded memory to a short index.
- Give each concurrent writer its own page, and pair wikis with search.

## Terms

- **Dreaming** — offline consolidation that corrects, restructures and promotes memory.
- **Memory representation** — a structured artifact, such as a linked wiki, built from notes and transcripts.

## Caveats

- Anthropic models and benchmarks, several very recent (Opus 5.5, Sonnet 5.5, Claude Fable 5). Anthropic's Managed Agents docs describe dreaming, so it is also a product pitch.
- The 87% vs 73% applies to the merger question set, not the legal-brief grading. The Mt. Moon action count appears only in a figure description.
- Builds on the [Managed Agents post's](2026-04-08-anthropic-managed-agents.md) log-first design by adding curated layers above the log.
