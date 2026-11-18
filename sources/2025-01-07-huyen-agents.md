---
type: source
title: "Agents"
author: "Chip Huyen"
publisher: "huyenchip.com"
url: https://huyenchip.com/2025/01/07/agents.html
published: 2025-01-07
ingested: 2026-11-17
kind: article
read: full
concepts: [agents-and-workflows, error-analysis, evals, sandboxing-and-permissions, tool-design]
---

# Agents

**In one line:** An agent is an environment, tools and a model that plans: validate plans before running them, choose tools by experiment, and evaluate by counting each kind of failure.

## What it says

- An agent is anything that senses an environment and acts on it, so its environment and tools define it, and ChatGPT and RAG systems already qualify.
- Agents need stronger models than single calls: at 95% accuracy per step, 10 steps succeed 60% of the time and 100 steps 0.6%. Tools that act raise the stakes.
- Three kinds of tool: knowledge augmentation (retrieval, SQL, web browsing), capability extension (calculator, code interpreter) and write actions. Chameleon, a GPT-4 agent with 13 tools, beat the best published few-shot result on ScienceQA by 11.37% and raised TabMWP accuracy by 17%.
- Write actions need trust: an unreliable model should not start bank transfers. Set the level of automation per action. People can step in at any stage: write the plan, check it, or approve and carry out risky operations.
- Decouple planning from execution: generate a plan, validate it by heuristics (no unknown tool, a step limit) or an AI judge, then run it. Counting generator, validator and executor as agents, the author calls most agents multi-agent. An intent classifier helps pick tools and should label out-of-scope requests IRRELEVANT.
- Whether LLMs can plan is left open: Yann LeCun (2023) says autoregressive ones cannot.
- Better plans come from more examples, clearer tool descriptions, simpler functions, a stronger model or finetuning. Function-calling APIs can guarantee a valid function, not correct parameter values. Plans in natural language survive tool renames but need a translator. Control flow may be sequential, parallel, an if statement or a for loop.
- Reflection, by self-critique or a separate scorer, can follow the request, the plan, each step and the whole run. ReAct interleaves reasoning with actions; Reflexion splits reflection into an evaluator and a self-reflection module. Reflection is easier to add than planning and helps a lot, but costs tokens and latency.
- Choose tools by experiment: published inventories run from 5 tools (Toolformer, on GPT-J) to 1,645 APIs (Gorilla). Compare sets, ablate, replace tools the agent keeps misusing, plot call frequency, and merge tools that usually follow each other (tool transition). In Chameleon GPT-4 used a broader range of tools than ChatGPT. Voyager keeps programs the agent wrote in a skill library.
- Failures to measure: planning (unknown tool, invalid parameters, wrong values, goal or constraint missed, a false claim of completion), tools (wrong output, a missing tool) and efficiency. Time is the constraint evals tend to forget. Test each tool on its own.

## What to do with it

- Validate a plan before executing it, and cap its length.
- Mark each tool read-only or write, and set per action what may run unattended.
- Log every tool call with its parameters and output.
- Remove each tool in turn and drop those not missed.
- Build a planning eval from (task, tool inventory) pairs, count each failure type, and track steps, cost and time per task against a baseline.

## Terms

- **Tool inventory** — all the tools available to an agent.
- **Read-only action / write action** — a tool call that observes the environment / one that changes it.

## Caveats

- January 2025, adapted from the author's book *AI Engineering*; she calls the framework best-effort. Its evidence is research papers from 2022 to 2024 on GPT-4, ChatGPT and GPT-J, not production systems.
- Defines terms more widely than this wiki and than [Building effective agents](2024-12-19-anthropic-building-effective-agents.md): any tool-using system is an agent, any chain of components multi-agent.
- The 60% and 0.6% are arithmetic, assuming independent steps and no recovery.
- Defers memory to a later post and omits sandboxing.
- Later notes run one gated loop, with no plan translator ([Loams](2026-10-18-loams-coding-agent-harnesses.md)).
