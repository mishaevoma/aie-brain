---
type: concept
title: "Compounding: turning corrections into infrastructure"
updated: 2026-11-17
status: evolving
---

# Compounding: turning corrections into infrastructure

**Definition:** Converting each correction, review comment or failure into something durable (a lint rule, a test, a hook, an instruction or a skill) so the same problem does not have to be solved twice.

## Why it matters

An agent can fix an issue every time it sees it, but that costs tokens each time and misses cases. Encoded once, the whole class of issue goes away, for every agent you run and for every person who joins. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)

## What to do

- When you correct an agent for the same thing twice, stop and encode it. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md) · [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Choose the most deterministic form that works:
  1. A lint rule, test or CI step, when a machine can check it. It costs no tokens and does not get forgotten. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
  2. A hook, when it must run at a fixed point. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
  3. A skill, when it is a procedure. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
  4. A line in an instruction file, when it is a short fact needed everywhere. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Read review comments and rejected pull requests as a backlog of missing automation. A rejection for using the wrong framework is a failure of automation, not of the contributor. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
- Turn misses into rules with a bar. One team requires a pattern to appear in at least two pull requests and be visible in a diff, has three agents try to disprove it, and has a person approve it. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Keep your corrections. Each edit you make to agent output is a test case. Saved as gold cases and yes/no checks, they let a skill be improved against your taste. [Shipper, Nov 2026](../sources/2026-11-15-shipper-compounding-skills.md)
- Record why something missed your bar, in shared configuration, a hook or a test. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- File good answers back into the knowledge base, so questions add to it. [Karpathy, 2 Apr 2026](../sources/2026-04-02-karpathy-llm-knowledge-bases.md) · [Karpathy idea file, Apr 2026](../sources/2026-04-04-karpathy-llm-wiki-idea-file.md)
- Keep traces. They are the raw material for improving the model, the harness or the context. [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)

## The same idea, one level up

- Harness: run the agent on tasks, store the logs, and have a coding agent read them and propose harness changes. [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)
- Prompts: with a rich eval suite, a model can edit its own system prompt until a failing eval passes, with the rest of the suite guarding against regressions. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)

## The counterweight: prune

Rules, tests and instruction files only grow if you let them, so tidy them on a routine. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md) Remove unused skills and servers, split oversized files, and delete lines that no longer prevent a mistake. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md) · [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Theo, Jul 2026](../sources/2026-07-28-theo-rewriting-agents-md-by-hand.md)

## Test of success

Could someone who does not know the codebase get a correct change merged by prompting alone? [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)

## Related

[Verification](verification.md) · [Skills](skills.md) · [Instruction files](instruction-files.md) · [Memory](memory.md) · [Evals](evals.md)
