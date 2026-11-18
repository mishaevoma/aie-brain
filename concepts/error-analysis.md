---
type: concept
title: "Error analysis"
updated: 2026-11-17
reviewed: 2026-11-17
status: evolving
---

# Error analysis

**Definition:** Reading real interactions with an AI product, noting what failed in each, grouping the notes into failure modes and counting them, to decide what to fix and what to measure.

## Why it matters

Without it a team measures what is easy to measure. Dashboards of generic metrics give false confidence, and nobody can say whether a change helped. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md) The failure modes found this way decide which evals are worth writing. [Error analysis FAQ, Jun 2025](../sources/2025-06-27-husain-shankar-error-analysis-faq.md) At one company three failure modes covered over 60% of the problems, and working on the worst took date handling from 33% to 95% success. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)

## What to do

- Collect representative traces of real use. With no users yet, have a model write user inputs across features, scenarios and personas, grounded in real records. Generate inputs only, never expected outputs. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md) · [Error analysis FAQ, Jun 2025](../sources/2025-06-27-husain-shankar-error-analysis-faq.md)
- Open coding: read each trace and write a free-form note on what went wrong. Note the first failure in a trace, since later ones often follow from it. [Error analysis FAQ, Jun 2025](../sources/2025-06-27-husain-shankar-error-analysis-faq.md)
- Do the first reading yourself, or have one domain expert with the final say do it. Annotate at least 30 traces before letting an agent propose more cases. [Error analysis FAQ, Jun 2025](../sources/2025-06-27-husain-shankar-error-analysis-faq.md)
- Axial coding: group the notes into failure modes and count the failures in each. A model can draft the grouping. [Error analysis FAQ, Jun 2025](../sources/2025-06-27-husain-shankar-error-analysis-faq.md) · [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- Write the first tests and [evals](evals.md) for the largest groups. Let metrics come out of these failures: stock ones such as hallucination or toxicity often miss what is specific to a domain. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- Stop when new traces stop showing new failure modes. A pool of roughly 100 diverse traces is a useful size. [Error analysis FAQ, Jun 2025](../sources/2025-06-27-husain-shankar-error-analysis-faq.md)
- Make reading cheap: a viewer that shows one interaction with all its context and takes a verdict and a note in one step. A spreadsheet will do at first. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)

## Where sources differ

- **Your own traces, or a general list.** Both texts above say the categories must come from your own data. An earlier one starts from a general list of agent failures: a tool that does not exist, wrong parameters, a missed goal, a false claim of being done. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md) This brain's reading: use the list to know what to look for, and keep only the categories your traces confirm.
- **Read first, or write tasks first.** A newer guide starts from 20 to 50 tasks drawn from real failures, and reads transcripts as a check on the score. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) The texts above put the reading first and let it decide what the tasks are. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md) See [evals](evals.md).

The two texts on the method share an author, who teaches a course on the subject. Their figures are rules of thumb and single cases, not measurements. The later text was revised in September 2026.

## Related

[Evals](evals.md) · [Trusting eval numbers](eval-validity.md) · [Human judgment and oversight](human-judgment.md)
