---
type: playbook
title: "Reviewing agent work"
updated: 2026-11-17
---

# Reviewing agent work

A checklist for the person, to use on anything that matters. Scale it to the stakes: where being wrong is cheap, delegate fully and skip most of this. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

## Before you start the agent

- [ ] Write down what you expect the answer or approach to be, even roughly. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Write the brief in your own words: who it is for, what is out of scope, what done means. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Decide what evidence will count as verified: a passing test, a screenshot, a log. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Make sure the agent can produce that evidence itself. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- [ ] If the area is unfamiliar, ask the model what you are missing before committing to an approach. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

## When it reports back

- [ ] Read the commands it ran and their output before the summary. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] For each green check, say what it proved and what it did not. If you cannot say what the checks would miss, ask for a real review. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Ask for the list of decisions and assumptions it made. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Read the diff as if a person you do not know wrote it. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Ask "did I miss anything?" and have a fresh-context reviewer look. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md) · [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md)
- [ ] Spot-check sources and at least one number that a conclusion depends on. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Check that it did not change the tests or the rules that judge it. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md) · [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)

## Before you ship

- [ ] Can you explain the change, with the agent's help if needed? If not, you do not own it yet. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Would you defend it in front of the person who will maintain it? [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] Was it run end to end, not only unit-tested? [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md) · [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)

## Afterwards

- [ ] If you corrected something for the second time, encode it as a check, a rule or a skill. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
- [ ] If something missed your bar, record why where the agent will see it next time. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- [ ] If finished work is piling up faster than you can review it, tighten the checks or run fewer agents. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

Detail: [human judgment](../concepts/human-judgment.md), [verification](../concepts/verification.md), [compounding](../concepts/compounding.md).
