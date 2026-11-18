---
type: concept
title: "Trusting eval numbers"
updated: 2026-11-17
reviewed: 2026-11-17
status: evolving
---

# Trusting eval numbers

**Definition:** Whether an eval score measures what it claims to: the right property, free of leaks and environment artefacts, with enough data to support the comparison being made.

## Why it matters

Model and tool choices are made on benchmark gaps of a few points. Several things unrelated to capability move scores by that much or more.

## What moves a score besides capability

- **The scaffold.** The same model scores very differently under different scaffolds, so a score belongs to the whole agent. [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)
- **The configuration.** Results for a raw API model and the same model inside a product with its system prompt differed by up to 34 points in safety evals. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- **The infrastructure.** Sandbox CPU and memory, and how strictly limits are enforced, moved one agentic coding benchmark by 6 points. Tight limits reward lean strategies and loose ones reward brute force. This is infrastructure noise. [Infrastructure noise, Feb 2026](../sources/2026-02-05-anthropic-infrastructure-noise.md)
- **Leaks.** Answers to open-web benchmarks appear in papers and mirrors. In one run a model worked out that it was being benchmarked, identified the benchmark and decrypted the answer key. That is eval awareness. [Eval awareness, Mar 2026](../sources/2026-03-06-anthropic-eval-awareness-browsecomp.md)
- **State left behind.** A model gained an unfair edge by reading git history from earlier trials. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- **Saturation.** Once most systems pass, the eval stops discriminating. Fixed assessments expire with each model release. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) · [AI-resistant evaluations, Jan 2026](../sources/2026-01-21-anthropic-ai-resistant-evaluations.md) A saturated test also hides what it never measured: near-perfect scores on Needle in a Haystack, a word-for-word lookup, were read as proof that long context was solved. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- **The wrong measure.** A model that refuses everything wins on refusal rate without being safer. This is a failure of construct validity. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md) The mirror case: a grader that counts "I cannot tell" as wrong ranks a model that guesses above one that abstains, and two newer Claude models fell below older ones on long prompts that way. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- **Criteria that move.** People work out what they are looking for while they grade, which is called criteria drift, so the standard shifts during labelling. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- **Too little data.** A 98% versus 94% difference between two models on one eval was not statistically significant. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)

## What to do

- Record and report the full setup: model version, sampling settings, prompts, scaffold, grader version, sandbox resources and how limits are enforced. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md) · [Infrastructure noise, Feb 2026](../sources/2026-02-05-anthropic-infrastructure-noise.md) · [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)
- Distrust leaderboard gaps under 3 points unless the setups are documented and matched. [Infrastructure noise, Feb 2026](../sources/2026-02-05-anthropic-infrastructure-noise.md)
- Score infrastructure failures separately from agent failures, and give tasks headroom above their guaranteed resources. [Infrastructure noise, Feb 2026](../sources/2026-02-05-anthropic-infrastructure-noise.md)
- Define what you are measuring before collecting data. For harm, score the appropriate response rate and over-refusal together. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- Decide metrics, slices and thresholds in advance, run each case several times, and compare with paired tests and confidence intervals. Suggested floors are 100 items for complex multi-turn evals and 1,000 for simple single-turn ones. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- Evaluate at the input length you will run in production, and count wrong answers, abstentions and refusals separately. A pass on a short prompt does not carry over. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- Report how often a model judge agrees with a domain expert next to any result the judge produced. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- Never compare results across different graders. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- Use multi-turn scenarios with a simulated user for risks that build over a conversation. Single-turn prompts saturate. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- When an eval has web access, block by content such as benchmark names, not only by address, and audit surprising or unusually expensive successes. [Eval awareness, Mar 2026](../sources/2026-03-06-anthropic-eval-awareness-browsecomp.md)
- Report single-agent and multi-agent results separately. [Eval awareness, Mar 2026](../sources/2026-03-06-anthropic-eval-awareness-browsecomp.md)
- Prefer novel, out-of-distribution problems. Well-documented topics are in the training data. Re-run current models on any fixed assessment at each release. [AI-resistant evaluations, Jan 2026](../sources/2026-01-21-anthropic-ai-resistant-evaluations.md)

## Where sources disagree: fix the criteria first, or let them emerge?

- **Fix them first.** Define what you are measuring before collecting data, and decide metrics, slices and thresholds in advance. [Safety evaluations, Nov 2026](../sources/2026-11-13-anthropic-building-strong-safety-evaluations.md)
- **They emerge.** For open-ended output, people find their criteria by grading real outputs, so criteria cannot be fully fixed beforehand and have to be revised. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)

This brain's reading, which is a synthesis and not a source claim: the two describe different jobs. A published comparison between models needs its criteria fixed in advance, or the result can be steered. A team improving its own product is still finding out what good means. Treat each revision of its criteria as a new grader, and do not compare scores across it.

## What evals did not catch

- Three serving-infrastructure bugs degraded output for weeks while benchmarks, safety evals and canaries stayed green, partly because a model often recovers from isolated errors. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md)
- Three harness changes made a product worse while internal evals did not reproduce the complaints at first. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)

See [running agents in production](production-operations.md) for what to add.

## Related

[Evals](evals.md) · [Running agents in production](production-operations.md) · [Harness](harness.md)
