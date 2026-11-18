---
type: source
title: "Q: Why is “error analysis” so important in AI evals, and how is it performed?"
author: "Hamel Husain, Shreya Shankar"
publisher: hamel.dev
url: https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html
published: 2025-06-27
ingested: 2026-11-17
kind: article
read: full
concepts: [error-analysis, evals]
---

# Q: Why is “error analysis” so important in AI evals, and how is it performed?

**In one line:** Read real traces and name what went wrong before you write any eval, because the failure categories you find decide which evals are worth having.

## What it says

- **Error analysis** is called the most important activity in evals. It decides what to evaluate, and it finds the failure modes particular to one application and its data.
- Step 1, a dataset: representative traces of real use, or synthetic ones when there is no data yet.
- Step 2, **open coding**: a person, ideally one domain expert with the final say, reads traces and writes free-form notes on what went wrong. Note the first failure in a trace, since later ones often follow from it. Annotate at least 30 traces yourself before looking at an agent's suggestions.
- Step 3, **axial coding**, named the most important step: group the notes into a failure taxonomy and count the failures in each category. A model can help with this.
- Step 4, repeat with an agent's help. It clusters the data, picks a diverse sample and, after the first 30 annotations, searches the rest for likely cases of the failures described. The person accepts or rejects them. Stop at **theoretical saturation**, when new reviews stop revealing or changing failure modes. A pool of roughly 100 diverse traces is a useful size.
- Skipping this leads to generic metrics, which most eval platforms nudge teams towards and which the authors call counter-productive.

## What to do with it

- Before building graders, read at least 30 traces and write down what failed in each.
- Turn the notes into categories, count them, and write evals for the categories that occur most.
- Let an agent propose more cases only after you have described the failures yourself.

## Terms

- **Open coding** — free-form notes on what went wrong in each trace.
- **Axial coding** — grouping those notes into a failure taxonomy.
- **Theoretical saturation** — the point where reading more traces reveals nothing new.

## Caveats

- One entry in a long FAQ, published in June 2025 and modified on 1 September 2026. This note follows the text as read on 17 November 2026, which describes an agent helping with the annotation.
- The authors teach a paid course on evals. The figures of 30 and 100 are rules of thumb, not measurements.
- The longer argument is in [A Field Guide to Rapidly Improving AI Products](2025-03-24-husain-field-guide-improving-ai-products.md).
