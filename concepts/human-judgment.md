---
type: concept
title: "Human judgment and oversight"
updated: 2026-11-18
reviewed: 2026-11-17
status: evolving
---

# Human judgment and oversight

**Definition:** What stays with the person when agents do the work: stating intent, deciding what counts as done, checking evidence, and answering for what ships.

## Why it matters

Agent output is now mostly correct and always polished, so it stops inviting a second look. You can run many agents but you have one pair of eyes. Accountability for what ships stays with a person however much of the work was delegated. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

## The spectrum

[Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

- **Offloading**: you delegate the task and keep ownership of the result. Healthy.
- **Deferral**: the output becomes your input without being treated as a hypothesis.
- **Cognitive surrender**: the output becomes your position and you feel no need to check it.

The test of ownership: can you explain the answer, even with the agent's help? You do not need the whole system in your head. You need to be able to rebuild understanding of the part in question, and to know what you do not know. The cost of sliding down the spectrum is comprehension debt: everything looks clean until someone has to change the system and nobody understands it. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

## What to do

**Before**

- Form a view before you ask. If you have none, ask the model what you are missing (a blind-spot pass). [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Write the brief yourself: audience, what is out of scope, what done means. An agent will not push back on a vague request, and what you leave unstated becomes intent debt that only you can pay. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Delegate fully where being wrong is cheap. Keep the reasoning where others carry the consequences. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Ask to see the plan. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) · [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md)

**After**

- Read the evidence before the summary. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Ask the agent to list the decisions and assumptions it made. Over a long session it makes many quiet ones. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Review intent and architecture, and expect to say no more often. On one team where a model wrote most of the code, engineers set the architecture and regularly rejected approaches. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)
- Let failures route your attention: checks that still fail after a few rounds, and changes that match a known risk. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

**When a product's output is what is judged**

- Let the domain expert judge outputs and edit prompts directly, instead of briefing engineers who translate. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- Ask for the verdict and the reason in writing. Writing the critique makes experts state standards they had not put into words. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
Which actions need a person's approval, and how an approval can wait for days, is on [side effects and approvals](side-effects.md).

**As a habit**

- Watch the orchestration tax: the gap between what your agents produce and what you would put your name on. If work piles up unchecked, tighten the checks or slow down. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Do some real work without an agent regularly, and decide on purpose which skills you are willing to lose. Supervising agents needs the skills that fade when unused. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Schedule checking as real work. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

## How oversight is changing

- From approving each step to watching and interrupting. Experienced users auto-approve about twice as often as new ones and interrupt more. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Per-action prompts are being replaced by boundaries and classifiers, because people approve nearly everything. See [permissions and sandboxing](sandboxing-and-permissions.md). [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- Approval does not disappear. For a few high-stakes actions, such as sending external email or changing production data, quick access to a person is what makes it acceptable to give the agent the tool. The request goes out as a tool call and is answered where the person already works. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Unreviewed autonomous code is still a security risk. Keep a person before deployment. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)
- From prompting each run to being asked by agents that start themselves. Each check-in costs attention, and one measure is the share of check-ins a person acts on. [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md) See [background agents](background-agents.md).

## Related

[Verification](verification.md) · [Compounding](compounding.md) · [Permissions and sandboxing](sandboxing-and-permissions.md) · [Side effects and approvals](side-effects.md) · [Background agents](background-agents.md) · [Agent identity and tenancy](agent-identity.md)
