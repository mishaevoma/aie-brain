---
type: source
title: "Ranking Engineer Agent (REA): The Autonomous AI Agent Accelerating Meta’s Ads Ranking Innovation"
author: "Ashwin Kumar, Erwin Gao, Matan Levi, Sheela Yadawad, Sherman Wong, Sneha Iyer, Vinodh Kumar Sunkara"
publisher: Engineering at Meta
url: https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/
published: 2026-03-17
ingested: 2026-11-17
kind: article
read: full
concepts: [production-operations, side-effects]
---

# Ranking Engineer Agent (REA): The Autonomous AI Agent Accelerating Meta’s Ads Ranking Innovation

**In one line:** For work whose steps take hours to weeks, Meta's agent does not stay alive: it passes each wait to a background system, exits and is resumed with the results, inside a plan and compute budget an engineer approved first.

## What it says

- REA is Meta's agent for experimentation on ads ranking models: it generates hypotheses, launches training jobs, debugs failures and iterates. It is built on Confucius, an internal agent framework.
- **Hibernate-and-wake.** A training job takes hours or days, and a whole workflow days to weeks. On launching a job REA hands the wait over to a background system and shuts down to save resources. When the job completes it resumes automatically where it stopped. State and memory persist across rounds.
- **Approval before execution.** REA proposes an exploration strategy with an estimate of total GPU compute cost, and an engineer confirms it before anything runs. Engineers also grant access through preflight checklist reviews. Runs are halted or paused when budget thresholds are reached, and the agent works only on the ads ranking model codebase.
- **Three phases.** Validation tests hypotheses in parallel to set baselines, Combination merges the promising ones, and Exploitation pushes the best candidates within the approved budget.
- **Planner and executor.** An engineer and the hypothesis generator produce a detailed experiment plan in the REA Planner. It is exported to the REA Executor, an agent loop with a wait state: it waits during training runs and resumes with results.
- **Failures inside guardrails.** When infrastructure fails, memory runs out or training becomes unstable, the executor checks a runbook of common failure patterns and prioritises, for example by excluding jobs that plainly ran out of memory or whose loss exploded. It returns results to the planner and does not escalate routine failures.
- **Memory.** An experiment logger writes outcomes, metrics and configurations to a central insight database that the hypothesis generator reads in later rounds.
- **Reported results** from the first production rollout: REA-driven iterations "doubled average model accuracy" relative to baseline approaches, measured over six models. Three engineers delivered launch proposals for eight models, work that historically took two engineers per model. Early adopters went from one model-improvement proposal to five in the same time frame.

## What to do with it

- For jobs lasting hours or more, end the agent process and resume it on a completion event.
- Put the human decision at the plan: strategy, estimated cost and budget, approved before execution.
- Enforce the budget in the runtime, pausing at a threshold.
- Write a runbook of known failures and let the agent handle those without asking.

## Terms

- **Hibernate-and-wake** — the agent shuts down during a long job and is restarted with its state when the job finishes.
- **Preflight checklist** — the review in which engineers grant the agent its access.

## Caveats

- A company post from March 2026 with headline figures and no method: "accuracy" and the baseline are undefined, and six and eight models are small samples. The "5x" label rests on proposals, not launches.
- No detail on how state is stored, what the background system is or which model REA uses.
