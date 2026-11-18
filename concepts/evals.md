---
type: concept
title: "Evals"
updated: 2026-11-17
reviewed: 2026-11-17
status: evolving
---

# Evals

**Definition:** Repeatable tests of an AI system. A *task* has inputs and success criteria, a *trial* is one attempt at it, and *graders* score the result. Evals are how you tell improvement from regression and from noise.

## Why it matters

Without evals, a team learns about regressions from complaints and cannot tell whether a change helped. With them, a prompt tweak, a tool change or a model upgrade can be checked before it ships. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) · [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)

## Vocabulary

- **Task, trial, grader**: as above.
- **Transcript**: the full record of a trial.
- **Error analysis**: reading real interactions and counting what fails, before deciding what to measure. See [error analysis](error-analysis.md). [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- **Outcome**: the final state of the environment, such as the booking existing in the database. Not the agent saying it booked. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- **Evaluation harness** runs and scores tasks. **Agent harness** is the scaffold being tested. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- **Capability evals** start with low pass rates and show what the system cannot do yet. **Regression evals** sit near 100% and catch breakage. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- **pass@k** is the chance of at least one success in k tries. **pass^k** is the chance all k succeed. At 75% per trial, pass^3 is about 42%. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)

## What to do

- Start with [error analysis](error-analysis.md): read real interactions, name and count the failures, and write the first evals for the largest groups. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md) · [Error analysis FAQ, Jun 2025](../sources/2025-06-27-husain-shankar-error-analysis-faq.md)
- Start small and early: 20 to 50 tasks drawn from real failures, manual pre-release checks and support tickets. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) · [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Grade the end state, not the agent's claim and not its exact sequence of steps. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Prefer deterministic graders. Where you need a model as judge, calibrate it against human experts, give it an "unknown" option, score each dimension separately, and use a different model from the one under test. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) · [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- Keep measuring how often a model judge agrees with a domain expert's pass or fail labels, and measure again when inputs change. One team needed three rounds of prompt changes to pass 90%. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- Ask a human grader for pass or fail, not a 1-5 score, with the nuance in a written critique. Neighbouring points on a scale are applied inconsistently, and the critiques serve later as examples for a model judge. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- Express taste as many small yes/no questions (binary checks), not one overall score. [Shipper, Nov 2026](../sources/2026-11-15-shipper-compounding-skills.md) · [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- Write unambiguous tasks with a reference solution that passes every grader, and cover both when a behaviour should happen and when it should not. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Add behavioural evals: small, fast, deterministic checks on what the agent does along the way, such as which tool it called. Write one per failure mode you have seen. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)
- For agents, count failures by kind as you read: a tool that does not exist, invalid or wrong parameters, a missed goal or constraint, a false claim of being done, a wrong tool output. Track steps, cost and time per task beside correctness. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md)
- Start every trial from a clean environment. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Read transcripts before trusting a score. A 0% pass rate usually means a broken task, and one benchmark score went from 42% to 95% after grading and scaffold fixes. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Report pass^k when users need consistency. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) · [Think tool, Mar 2025](../sources/2025-03-20-anthropic-think-tool.md)
- Rerun the suite on every prompt, tool-schema and model change, and track pass rates over time instead of blocking on a single noisy run. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)
- Use a broad suite for prompt edits. A narrow one missed a 3% drop from a single system-prompt line. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)

## Evaluate the parts too

- Tools: realistic tasks that take many calls, with a held-out set. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Skills: checks built from your own corrections. [Shipper, Nov 2026](../sources/2026-11-15-shipper-compounding-skills.md)
- Reviewers: past incidents with a one-sentence answer key, a control set of clean changes, and recall measured at each stage. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

## Where sources differ

- **Where to start.** One guide says to write the first evals now. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) Another says to begin with instinct and dogfooding and add evals once the agent can work on its own codebase. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md) A third says the first move is neither: read and annotate real interactions, and let the first evals come out of the failure counts. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md) All three agree evals are what keep progress going once the product is in real use.
- **A score or a verdict.** A grader can give partial credit [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md), answer many small yes/no questions [Shipper, Nov 2026](../sources/2026-11-15-shipper-compounding-skills.md), or give one pass or fail verdict with a written critique [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md). This brain's reading: the finer the check, the easier it is to automate, and the single verdict suits a human expert judging whether an output did its job.
- **Criteria first, or criteria that emerge.** See [trusting eval numbers](eval-validity.md).

Evals are one layer. Production monitoring, A/B tests, user feedback and transcript review cover what they miss. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)

## Related

[Error analysis](error-analysis.md) · [Trusting eval numbers](eval-validity.md) · [Verification](verification.md) · [Harness](harness.md) · [Running agents in production](production-operations.md)
