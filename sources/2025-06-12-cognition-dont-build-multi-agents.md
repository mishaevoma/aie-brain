---
type: source
title: "Don’t Build Multi-Agents"
author: "Walden Yan"
publisher: Cognition
url: https://cognition.com/blog/dont-build-multi-agents
published: 2025-06-12
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, multi-agent-systems]
---

# Don’t Build Multi-Agents

**In one line:** Agents that split work among subagents break because each one acts on context the others cannot see, so the default should be one agent with one continuous context.

## What it says

- **Context engineering**, getting the right information in front of the model automatically, is called the main job of engineers who build agents and the core of reliability for agents that run a long time.
- The tempting design is fragile: an agent splits a task, starts a subagent per part and merges the results. In the example, a Flappy Bird clone comes back as a background in another game's style and a bird that does not fit it.
- Passing each subagent the original task is not enough, because the task was shaped by earlier turns and tool calls. **Principle 1:** share context, and share full agent traces, not only individual messages.
- Subagents working in parallel still cannot see each other's work, and make assumptions that conflict. **Principle 2:** actions carry implicit decisions, and conflicting decisions carry bad results.
- Rule out by default any architecture that breaks either principle. The simplest that keeps both is a single-threaded linear agent. When a task overflows the window, add a model that compresses the history into key details, events and decisions. This is hard to get right, and Cognition fine-tuned a smaller model for it.
- Two examples. As of June 2025, Claude Code's subagents never ran in parallel with the main agent and usually answered a question instead of writing code, which keeps their exploration out of the main history. The 2024 practice of a large model describing an edit for a small **edit apply model** failed on small ambiguities, and one model now usually does both.
- Agents that talk to each other to settle conflicts were not reliable in 2025. OpenAI's Swarm and Microsoft's AutoGen are named as libraries that push the wrong idea. The author expects collaboration to become workable as single agents get better at communicating with people.

## What to do with it

- Start with one agent and one continuous context. Add a subagent where the subtask is a well-defined question whose answer can come back as a summary.
- When you delegate, pass the trace that led to the task, not a one-line brief.
- Do not let parallel workers make decisions that have to agree, such as style, interfaces and naming, unless something settles those first.
- Treat history compression as a component of its own, and evaluate it.

## Terms

- **Edit apply model** — a small model that rewrites a file from a larger model's description of the change.

## Caveats

- June 2025, from Cognition, which sells the coding agent Devin. The author calls the theory unfinished. It is an argument from experience with one worked example and no measurements.
- Anthropic's [multi-agent research system](2025-06-13-anthropic-multi-agent-research-system.md), published a day later, reports the opposite for broad research, and itself calls work that needs shared context a poor fit. A later note has 16 agents building a compiler in parallel, coordinated through git and a test harness instead of conversation ([C compiler](2026-02-05-anthropic-building-c-compiler.md)).
