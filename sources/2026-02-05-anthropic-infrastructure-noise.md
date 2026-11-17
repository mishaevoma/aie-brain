---
type: source
title: "Quantifying infrastructure noise in agentic coding evals"
author: "Gian Segato"
publisher: Anthropic
url: https://www.anthropic.com/research/infrastructure-noise
published: 2026-02-05
ingested: 2026-11-17
kind: article
read: full
concepts: [eval-validity]
---

# Quantifying infrastructure noise in agentic coding evals

**In one line:** in agentic coding benchmarks, sandbox CPU and RAM, and how strictly limits are enforced, can move scores by more than the gaps between top models.

## What it says

- In agentic evals the runtime is part of the task. Terminal-Bench 2.0 recommends per-task CPU and RAM, but a recommended spec is not consistent enforcement.
- Anthropic's Google Kubernetes Engine runs of Terminal-Bench 2.0 did not match the leaderboard, with up to 6% of tasks failing on pod errors: the spec was both the guaranteed allocation and the hard kill limit, leaving no headroom for spikes. The leaderboard's provider enforces more loosely.
- Across six settings from strict 1x to uncapped (model, harness, tasks fixed), infrastructure errors fell from 5.8% at 1x to 2.1% at 3x (p < 0.001) to 0.5% uncapped.
- Up to about 3x, scores stayed within noise (p = 0.40); headroom mostly rescued runs that would have failed anyway. Beyond that, success rose faster than errors fell: uncapped beat 1x by 6 points (p < 0.01) as agents could install big dependencies and run memory-heavy tests.
- So limits change what is measured: tight ones reward lean strategies, loose ones brute force. In `bn-fit-modify`, models that install pandas, networkx and scikit-learn run out of memory under tight limits; standard-library solutions do not. `rstan-to-pystan` and `compile-compcert` gained notably from memory.
- The direction held across Anthropic models; other vendors were not rigorously tested.
- SWE-bench (227 problems, 10 samples each, RAM up to 5x) moved only 1.54 points.
- Other suspected sources: time limits, cluster health, hardware, concurrency, egress bandwidth, time of day via API latency (anecdotal). Providers can use dedicated hardware; outside evaluators often cannot.

## What to do with it

- Report sandbox resources and enforcement as an experimental variable, like temperature.
- Set a guaranteed allocation and a separate, higher kill threshold per task; calibrate so floor and ceiling scores are within noise. For Terminal-Bench, a 3x ceiling cut infra errors by about two-thirds with no significant score lift. Report the multiplier.
- Score infra failures separately from agent failures.
- Run public coding evals at several times and days and average.
- Distrust leaderboard gaps under 3 points unless setups are documented and matched; binomial intervals alone span 1–2 points.

## Terms

- **infrastructure noise** — score variance from the execution environment rather than model or harness.

## Caveats

- February 2026; tested on Anthropic models only, and the 3x figure is specific to Terminal-Bench 2.0.
- Anthropic competes on the leaderboards it questions.
- Puts numbers on the harness-hygiene advice in the evals guide (2026-01-09).
