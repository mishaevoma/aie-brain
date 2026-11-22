---
type: source
title: "12-Factor Agents - Principles for building reliable LLM applications"
author: "Dex Horthy"
publisher: "HumanLayer"
url: https://github.com/humanlayer/12-factor-agents
published: 2025-03-30
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-interfaces, agents-and-workflows, context-engineering, harness, human-judgment, long-running-agents, multi-agent-systems, production-operations, sandboxing-and-permissions, tool-design]
---

# 12-Factor Agents - Principles for building reliable LLM applications

**In one line:** reliable agents are mostly ordinary software around short model loops; own the prompt, context window, control flow and state so a run can pause for a person and resume.

## What it says

- From talks with at least 100 SaaS builders: teams adopt a framework, reach 70-80% quality, find 80% too low for customer-facing features and start over, because improving means reverse-engineering it.
- An agent is a prompt, a switch statement, accumulated context and a loop. Run as a plain loop over a "bag of tools" it gets lost as context grows: builders dropped it past 10-20 turns, and 90% success is not shippable. Products that work are mainly deterministic code with **micro agents** inside: short loops, 5-10 steps in one example.
- **Factors 1 and 4** (Natural Language to Tool Calls; Tools are just structured outputs): the model turns a request into JSON, and deterministic code decides how to carry it out.
- **Factors 2 and 3** (Own your prompts; Own your context window): write prompts as code with tests and evals (shown in BAML). Context need not be a message list: typed events can be packed into one user message with XML-style tags, dropping resolved errors and filtering sensitive data.
- **Factors 5, 6 and 12** (Unify execution state and business state; Launch/Pause/Resume with simple APIs; Make your agent a stateless reducer): keep one serialisable thread of events as the source of truth, and infer step, waiting status and retries from it. Runs start through a simple API and resume from webhooks.
- **Factor 8** (Own your control flow): code decides after each model output whether to continue, wait or seek approval. The key is a pause between tool selection and tool invocation; without it you hold the task in memory, allow only low-stakes calls, or let the agent act unreviewed.
- **Factors 7 and 11** (Contact humans with tool calls; Trigger from anywhere, meet users where they are): asking a person (`request_human_input`) and finishing (`done_for_now`) become structured outputs, so the model always emits JSON. The run pauses, notifies them and resumes on the reply. Runs start from Slack, email, SMS, crons or events; **outer loop agents** (event-started) may work 5, 20 or 90 minutes before needing someone. Quick access to people makes high-stakes tools acceptable, such as sending external email or changing production data.
- **Factors 9 and 10** (Compact Errors into Context Window; Small, Focused Agents): feed tool errors back so the model can self-correct, cap attempts at about 3, then escalate. Keep each agent to 3-10, maybe 20 steps, widening scope as models improve; the techniques are expected to outlast model gains.
- **Appendix ("factor 13"):** fetch in code whatever the model would almost certainly ask for.

## What to do with it

- Before adopting a framework, check you can edit its exact prompt and pause between tool choice and execution.
- Store each run as one serialisable thread of events.
- Give the model "ask a person" and "done" outputs; let code decide which actions wait for approval.
- Keep loops short inside deterministic code, pre-fetch the certain calls, and cap consecutive tool errors.

## Terms

- **Execution state / business state** — where a run stands (step, waiting, retries) / what it has done so far.

## Caveats

- First committed 30 March 2025; the repository was last changed on 2025-09-21. Its step limits date from then: a [March 2026 note](2026-03-24-anthropic-harness-design-long-running-apps.md) describes builds lasting hours.
- The author builds HumanLayer and calls factor 11 its pitch. Evidence is anecdotal, not measured.
- MCP is skipped on purpose; sandboxing, cost, timeouts and repeat-safe writes are absent. Factor 12 is images only.
- It rejects the plain tool loop of [Building effective agents](2024-12-19-anthropic-building-effective-agents.md) and favours owning the loop; a [2026 note](2026-10-22-theo-what-is-a-harness.md) says adopt a harness. [Cognition](2025-06-12-cognition-dont-build-multi-agents.md) prefers one continuous thread to small agents. Its thread anticipates [Managed Agents](2026-04-08-anthropic-managed-agents.md).
