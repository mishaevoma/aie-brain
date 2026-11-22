---
type: source
title: "How to build a knowledge factory"
author: "Harrison Chase"
publisher: "@hwchase17 on X"
url: https://x.com/hwchase17/status/2124181216719151585
published: 2026-11-21
ingested: 2026-11-22
kind: x-article
read: full
concepts: [compounding, context-layer, knowledge-factory, llm-wiki, memory, retrieval, skills]
---

# How to build a knowledge factory

**In one line:** What agents lack inside a company is its knowledge of how the work is done, so build a system (a knowledge factory) in which working agents flag what is missing and a separate curator agent keeps skills, domain knowledge and data access guidance current.

## What it says

- The limit on agents doing a company's work is not the model and not simply more context. It is the knowledge the best employees carry: who to ask, where the answer lives, why something is done a certain way. Much of it is unwritten or scattered across documents.
- **Context** is what an agent has available during a task. **Knowledge** is the reusable understanding a company maintains so the task is done correctly, such as what a metric means, which source to trust, how a situation is handled. Knowledge becomes context when it is loaded, and it is not the only context: data that is already stored reliably is passed to the agent directly.
- The name follows the **software factory**: the best engineers build the systems that let everyone build software, and agents write the code. General knowledge work is described as going the same way. The examples given are presentations, launch videos and outbound sales.
- Three kinds of knowledge to maintain:
  - **Skills**: how the work is done properly at this company. Often passed between colleagues and never written down.
  - **Domain knowledge**: how the business works. Definitions, policies, and facts about products, customers, competitors and the organisation. It changes slowly, and what was written is usually incomplete or wrong because there is so much of it.
  - **Data access guidance**: which source holds what, and how to query it. Where a complete and current source of truth exists (Snowflake and Databricks are named), keep no second copy.
- Three parts of the factory:
  - A tool that lets a working agent **flag** knowledge it could not find or found to be wrong, and optionally propose the correction.
  - A **curator agent** that runs in the background on a cadence and updates the knowledge. It reads the raw sources (Notion, Slack and the like), the agent traces, and the flags. Working agents should not maintain the knowledge themselves: they are pursuing their own goals, and the store fills with contradictions.
  - **Storage**, called the least important part and also the least explored. Options listed: skills in GitHub, one file in Notion, Open Knowledge Format (OKF) in LangSmith Context Hub, a knowledge graph in Neo4j. Skills are said to be the settled form for procedural memory, with no standard yet for semantic memory.
- LangChain says its internal go-to-market and content studio agents run on such a system, and that LangSmith Engine keeps one per agent.
- Worked example, a revenue report. The raw figures come from BigQuery and Salesforce as plain context. The knowledge is a report-writing skill in GitHub, the definition of ARR in the company wiki, and data access instructions kept as skills in Context Hub. During the run the agent finds a renamed column, works around it and flags it with the right name. A finance lead then corrects formatting and requires a new document header. That night the curator reads the flag and the trace of the correction and updates both skills.

## What to do with it

- Do not try to document everything before agents start. Pick one recurring workflow, watch where agents struggle, and close that loop.
- Give working agents a way to report missing or wrong knowledge, and keep the repair in a separate scheduled agent.
- Give the curator the raw sources, the traces and the flags.
- Leave fast-changing data in its system of record and maintain the instructions for reaching it.
- Keep the storage format simple until a standard appears.

## Terms

- **Knowledge factory** — the system that collects, curates and maintains a company's knowledge for its agents.
- **Knowledge** — reusable understanding kept so that agents do tasks correctly, as distinct from the context of one task.
- **Curator agent** — the background agent that updates the knowledge store.
- **Data access guidance** — instructions on what data lives where and how to query it.
- **Software factory** — the systems that let a whole company build software through agents.

## Caveats

- The author runs LangChain. The article names its products for traces, schedules and storage, and ends with a sales contact.
- A framing article with no measurements. Nothing on how often the curator writes something wrong, or what it costs to run.
- No person approves the curator's updates in the example, and the article does not say how conflicting sources are settled.
- The three diagrams were images and were not read. The linked LangChain posts on its go-to-market agent, content studio agent, company harness and Context Hub, and the OKF repository, were not read.
