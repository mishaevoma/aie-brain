---
type: source
title: "A Field Guide to Rapidly Improving AI Products"
author: "Hamel Husain"
publisher: "hamel.dev"
url: https://hamel.dev/blog/posts/field-guide/
published: 2025-03-24
ingested: 2026-11-17
kind: article
read: full
concepts: [error-analysis, eval-validity, evals, human-judgment, production-operations]
---

# A Field Guide to Rapidly Improving AI Products

**In one line:** teams improve AI products fastest by reading their own data, counting failures, testing for the biggest and checking any LLM judge against a domain expert, not by choosing tools.

## What it says

- From advising 30+ companies: successful teams hardly discuss tools and focus on measurement. The usual mistake is the **tools trap**: trusting frameworks and dashboards of generic metrics, which give false confidence and split attention.
- **Error analysis** is called the highest-return activity. NurtureBoss's team read its apartment-industry assistant's conversations and wrote free-text notes on failures. Requests with relative dates (a tour in two weeks) failed 66% of the time; after categorising these failures and writing tests, date-handling success rose from 33% to 95%.
- Work bottom-up: stock metrics (hallucination, toxicity) often miss domain problems. One row per conversation, open notes, an LLM drafts a taxonomy of failure modes, label each row, count. Three failure modes covered over 60% of NurtureBoss's problems.
- A custom **data viewer** is the top investment: all context for one interaction on one screen, a one-click verdict, free-text notes, filters, hotkeys. The author claims 10x faster iteration and build times of hours with AI coding tools; a spreadsheet will do at first.
- Domain experts should edit prompts themselves, not brief engineers. Prompt playgrounds (Arize, LangSmith, Braintrust) are a start; better is an **integrated prompt environment** inside the real product.
- With no users, use synthetic data: an LLM writes user inputs, never expected outputs, across features, scenarios and personas, grounded in real records and business rules. Check each input triggers its scenario: a "no matches" query must return nothing.
- Teams drop evals they stop trusting. **Criteria drift** (Shankar et al., "Who Validates the Validators?"): people work out their criteria while grading, so criteria cannot be fully fixed in advance and need revising.
- Prefer pass/fail to a 1-5 scale: neighbouring scores are applied inconsistently and a cut-off is needed anyway. A written critique carries the nuance and makes experts spell out their standards; given to a judge prompt as few-shot examples, critiques often gave the author 15-20% higher agreement with humans.
- Keep measuring how often the LLM judge agrees with the expert (Eugene Yan's AlignEval does this): on Honeycomb's Query Assistant, exceeding 90% took three iterations. Begin with experts reviewing a large share of outputs, then sample where agreement is weakest.
- Roadmaps should promise experiments, not features: time-boxed feasibility work with decision points (Eugene Yan of Amazon: three months to a production decision), progress shown on Bryan Bischof's **capability funnel**. Evaluation tooling comes before feature commitments: GitHub Copilot's early offline evals, built on repositories' existing unit tests, enabled thousands of experiments.

## What to do with it

- Before picking metrics, read dozens of real interactions, note failures, group and count them, then test the largest groups.
- Build a viewer showing one interaction in full, with a verdict and a note.
- Have a domain expert edit prompts and give pass/fail plus a critique; track judge–expert agreement as inputs change.
- Plan in time-boxed experiments, not feature dates.

## Terms

- **error analysis** — reading real interactions, noting failures, grouping them into failure modes, counting.
- **criteria drift** — criteria changing as the grader sees more outputs.
- **integrated prompt environment** — an admin view of the product for editing prompts in context.
- **capability funnel** — levels of usefulness, from giving any response to completing the user's task.

## Caveats

- March 2025; tool names date it. Covers conversations and single queries, not multi-step agent runs, end-state grading, repeated trials, sample sizes or user privacy.
- The author sells consulting and an evals course; most cases are his clients, and 10x and 15-20% are impressions without data.
- It differs from [Demystifying evals](2026-01-09-anthropic-demystifying-evals.md), which gives partial credit where this one wants pass or fail, and from [Building strong safety evaluations](2026-11-13-anthropic-building-strong-safety-evaluations.md), which fixes the criteria before collecting data. The method is restated, with an agent helping, in the authors' [FAQ entry on error analysis](2025-06-27-husain-shankar-error-analysis-faq.md).
