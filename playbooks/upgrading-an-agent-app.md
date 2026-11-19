---
type: playbook
title: "Upgrading an existing AI app"
updated: 2026-11-19
reviewed: 2026-11-19
---

# Upgrading an existing AI app

Checks for code that already calls a model. [Building an agent product](building-an-agent-product.md) gives the order of decisions for a new product; this page is for a product that exists. Each check says what to look for in the code and what to change. The order is this brain's reading of where a small change most often pays off: first the checks that tell you whether anything else helped.

## 1. A check that fails when the AI part gets worse

Look for tests that swap the model for a canned reply, tests that are skipped unless a flag is set, and a test command that passes without touching the feature.

- For each green check, say what it proved and what it did not. A test written with the same misunderstanding as the feature passes. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Add a test of a real user flow, end to end. Unit tests can pass while the feature is broken. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Fix or delete flaky tests before anyone relies on them. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

Detail: [verification](../concepts/verification.md).

## 2. A small eval before the next change

Look for quality judged by eye or by complaints, and for labelled examples, support logs or sample files that nothing runs.

- Collect 20 to 50 tasks from real failures, manual checks and support tickets, and grade the end state. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Prefer deterministic graders, and express taste as many small yes/no questions. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md) · [Shipper, Nov 2026](../sources/2026-11-15-shipper-compounding-skills.md)
- With no examples yet, read real interactions first and count what fails. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)

Detail: [evals](../concepts/evals.md), [error analysis](../concepts/error-analysis.md).

## 3. Prompts released and tested like code

Look for a prompt assembled inside a function and edited by hand, with nothing that runs when it changes.

- Rerun the eval suite on every prompt, tool-schema and model change. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)
- Use a broad suite for prompt edits. A narrow one missed a 3% drop from a single system-prompt line. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Ship prompts, tool descriptions, schemas and model settings with the code as one release. [Updating agents safely, Mar 2026](../sources/2026-03-11-restate-updating-agents-safely.md)
- Build the context from structured parts in code and compile the prompt before each call. [How to fix your context, Jun 2025](../sources/2025-06-26-breunig-how-to-fix-your-context.md)

Detail: [evals](../concepts/evals.md), [running agents in production](../concepts/production-operations.md).

## 4. Only the relevant context in each call

Look for a whole history, a whole folder or every search hit pasted into the prompt, and for superseded versions kept beside current ones.

- Send the relevant parts, not everything that fits. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- Cut near-misses first. Stale versions of a fact and look-alike records do more harm than neutral filler. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- Whatever is always loaded costs tokens in every session and spreads its errors. Keep it to a short index and load the rest on demand. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md) · [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)

Detail: [context engineering](../concepts/context-engineering.md).

## 5. Retrieval that is measured

Look for search by embeddings alone, chunks cut at a fixed size with no document name or heading, and a long final list.

- Score retrieval on questions whose answering document you know, before tuning it. Applying the eval advice to retrieval is this brain's reading. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Add keyword search (BM25) beside embeddings. It catches exact identifiers such as error codes. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)
- Before indexing, add a short note to each chunk on where it sits in its document. [Contextual Retrieval, Sep 2024](../sources/2024-09-19-anthropic-contextual-retrieval.md)

Detail: [retrieval](../concepts/retrieval.md).

## 6. Actions that are safe to run twice

Look for one retry wrapper around every tool, a write that is retried after a timeout, and a send or a payment with no key.

- A call can succeed just before the failure that loses its record, so a retry can repeat it. [What survives failure, Nov 2026](../sources/2026-11-04-temporal-deciding-what-survives-failure.md) · [Running durable agents, Oct 2026](../sources/2026-10-15-vercel-running-durable-agents.md)
- Give each tool a replay policy: declare whether it may run twice, and rerun only those. [Pi Durable, Oct 2026](../sources/2026-10-01-earendil-pi-durable.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md)
- Send an idempotency key with every side effect, and deduplicate at the receiver on a business identifier. [Running durable agents, Oct 2026](../sources/2026-10-15-vercel-running-durable-agents.md) · [What survives failure, Nov 2026](../sources/2026-11-04-temporal-deciding-what-survives-failure.md)
- Decide approval from context, not from the tool name alone. [Linear, Aug 2026](../sources/2026-08-10-linear-how-we-built-linear-agent.md)

Detail: [side effects and approvals](../concepts/side-effects.md).

## 7. Tools the model can recover with

Look for an error returned as a bare string, a description a few words long, and model output stored or executed unchecked.

- Make errors say what to do next. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Write each description as you would brief a new hire: formats, jargon, how resources relate. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Treat a tool call as a proposal, and check the arguments in your own code. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md) · [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md)

Detail: [tool design](../concepts/tool-design.md).

## 8. Loops that stop

Look for `while True` around a model call, a critic that can reject for ever, and a loop with no step limit.

- Give every loop a stop condition: an iteration cap, and a breaker for repeated identical calls. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Set a round limit, after which a failing check goes to a person. One team uses three. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

Detail: [agents and workflows](../concepts/agents-and-workflows.md), [verification](../concepts/verification.md).

## 9. No more agents than the task needs

Look for roles that always run in the same order, a planner whose plan never changes the path, and an agent that sees only another agent's summary.

- When the steps are known in advance, write them as a workflow in code and keep a model for the steps that need judgment. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md) · [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md)
- Do not use an agent for every model call. Small generation jobs can go straight to a model API. [Theo, 9 Nov 2026](../sources/2026-11-09-theo-harness-difference-approaching-zero.md)
- Chains drift when each step reads only the previous one's summary. Keep the original material reachable. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Add a separate grader only where the task is beyond what the model does reliably alone. Below that line it only adds cost. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)

Detail: [agents and workflows](../concepts/agents-and-workflows.md), [multi-agent systems](../concepts/multi-agent-systems.md).

## 10. Untrusted text kept apart from private data and a way out

Look for customer or web text placed in the prompt of an app that also reads private data and can send messages.

- Check for the lethal trifecta: private data, untrusted content and a way to send data out. Remove one of the three. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md)

Detail: [permissions, sandboxing and containment](../concepts/sandboxing-and-permissions.md).

## 11. Checks on the path users take

Look for quality that is checked before release only, and for prompt or default changes that ship without a gate.

- Add cheap sanity checks on output to deploy gates. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md)
- Gate changes to system prompts and defaults like a model swap. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)

Detail: [running agents in production](../concepts/production-operations.md).
