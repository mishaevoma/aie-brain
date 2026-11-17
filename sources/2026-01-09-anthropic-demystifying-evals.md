---
type: source
title: "Demystifying evals for AI agents"
author: "Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe"
publisher: Anthropic
url: https://www.anthropic.com/research/demystifying-evals-for-ai-agents
published: 2026-01-09
ingested: 2026-11-17
kind: article
read: full
concepts: [eval-validity, evals, harness]
---

# Demystifying evals for AI agents

**In one line:** start an agent eval suite early with a few dozen real failure cases, grade outcomes rather than exact paths, mix code, model and human graders, and keep reading transcripts so you know the eval measures what you think it does.

## What it says

- Vocabulary: a **task** has inputs and success criteria; a **trial** is one attempt; **graders** score aspects of a trial; the **transcript** is the full record; the **outcome** is the final environment state (the booking exists in the database, not the agent saying it booked); the **evaluation harness** runs and scores tasks; the **agent harness** is the scaffold under test.
- Without evals, teams learn of regressions from complaints and cannot tell change from noise. Claude Code, Descript and Bolt added evals as usage grew; Bolt built its system in 3 months.
- Three grader families: code-based (tests, string match, static analysis, state checks) are fast, objective and brittle; model-based (rubrics, pairwise, multi-judge) are flexible, non-deterministic and need calibration; human graders are the gold standard but slow and costly.
- **Capability evals** should start with low pass rates; **regression evals** should sit near 100%. Capability tasks that saturate can graduate into the regression set.
- By agent type: coding agents suit test-based grading plus a rubric for code quality (SWE-bench Verified, Terminal-Bench); conversational agents need a simulated user and multi-part success such as resolved ticket, turn limit and tone (τ-Bench, τ2-Bench); research agents need groundedness, coverage and source-quality checks (BrowseComp); computer-use agents need checks on real backend state (WebArena, OSWorld).
- Non-determinism: **pass@k** is the chance of at least one success in k tries; **pass^k** is the chance all k succeed. At 75% per trial, pass^3 is about 42%. Use pass^k when users need consistency.
- Roadmap: begin with 20–50 simple tasks from real failures; turn manual pre-release checks and support tickets into tasks; write unambiguous tasks with a reference solution that passes every grader; balance cases where a behaviour should and should not happen (web search evals covered both).
- Harness hygiene: start each trial clean. Claude gained an unfair edge in some internal evals by reading git history left by earlier trials; trials that fail on the same environment limit (e.g. memory) are not independent.
- Grader practice: prefer deterministic graders; grade outputs, not step sequences; give partial credit; calibrate LLM judges against human experts, offer an "Unknown" option and judge each rubric dimension separately; make graders hard to game.
- Broken evals mislead: Opus 4.5 scored 42% on CORE-Bench until grading and scaffold fixes raised it to 95%. A 0% pass rate over many trials usually means a broken task. Opus 4.5 "failed" a τ2-bench task by finding a policy loophole that served the user better.
- Watch saturation (Qodo found one-shot evals missed Opus 4.5's gains on longer tasks). A central team should own infrastructure while product people contribute tasks.
- Evals are one layer alongside production monitoring, A/B tests, user feedback, transcript review and human studies. Appendix frameworks: Harbor, Braintrust, LangSmith, Langfuse, Arize (Phoenix, AX); task quality matters more than the tool.

## What to do with it

- Write your first 20–50 eval tasks now, from real bugs and support tickets.
- Grade the end state, not the agent's claim or its exact steps.
- Keep capability and regression suites separate and track both.
- Report pass^k for customer-facing reliability, not only pass@1.
- Isolate every trial's environment and resources.
- Read failing transcripts before trusting a score.

## Terms

- **pass@k / pass^k** — at-least-one-success versus all-succeed over k trials.
- **eval-driven development** — writing evals for capabilities before the agent can pass them.

## Caveats

- January 2026; model examples (Opus 4.5) and benchmark numbers will age.
- The article gives two starting points for SWE-bench Verified progress (40% and about 30%), both ending above 80%.
- Anthropic sells the models and Claude Code discussed; the framework list is not a review of those tools.
- Later notes add resource noise (2026-02-05) and eval-awareness risks (2026-03-06).
