---
type: concept
title: "Side effects and approvals"
updated: 2026-11-18
reviewed: 2026-11-18
status: evolving
---

# Side effects and approvals

**Definition:** A *side effect* is anything an agent does that changes the world outside its own run: a message sent, a payment, a deletion, a merge. Each one raises three questions: who approves it, what happens if it runs twice, and how it is undone.

## Why it matters

A durable runtime remembers how far a run got. It does not stop a tool call from running twice, because the call can succeed just before the crash that loses its record. [What survives failure, Nov 2026](../sources/2026-11-04-temporal-deciding-what-survives-failure.md) · [Running durable agents, Oct 2026](../sources/2026-10-15-vercel-running-durable-agents.md) And an agent that has damaged something is the wrong party to repair it, because its picture of the world may have drifted from the real one. [Remediation, Jul 2025](../sources/2025-07-28-vanlightly-remediation.md)

## What to do

**Before it runs**

- Decide approval from context, not from the tool name alone. One product lets its agent delete what it created earlier in the conversation and asks before deleting anything that already existed. [Linear, Aug 2026](../sources/2026-08-10-linear-how-we-built-linear-agent.md)
- For long and costly runs, put the decision at the plan: strategy, estimated cost and a budget, approved before anything executes. [Meta, Mar 2026](../sources/2026-03-17-meta-ranking-engineer-agent.md)
- Where writes can wait, let the agent only stage them, and apply them after it exits through deterministic checks on type, count and content. [GitHub, Mar 2026](../sources/2026-03-09-github-agentic-workflows-security.md)
- Authorize the approver in your own code, and send confirmations for a shared agent to its owner. [Running durable agents, Oct 2026](../sources/2026-10-15-vercel-running-durable-agents.md) · [Notion, Feb 2026](../sources/2026-02-27-notion-security-in-custom-agents.md)

**While it waits**

- Build a pause as stop and resume, not as a waiting process: save the run, release the compute, and continue when the answer arrives as an event. [LangGraph interrupts, Nov 2026](../sources/2026-11-12-langchain-langgraph-interrupts.md) · [Always-on agents, Nov 2026](../sources/2026-11-13-anthropic-building-always-on-agents.md)
- Register the wait before showing the request, and give it a deadline and an escalation path. A wait held in memory vanishes silently in a crash. [Running durable agents, Oct 2026](../sources/2026-10-15-vercel-running-durable-agents.md) · [Temporal multi-agent, Aug 2026](../sources/2026-08-06-temporal-durable-flexible-multi-agent-systems.md)
- Deliver a person's stop to the code that orchestrates the run, never through the model. [Temporal multi-agent, Aug 2026](../sources/2026-08-06-temporal-durable-flexible-multi-agent-systems.md)
- Place side effects after the pause, because code that ran before it can run again on resume. Deduplicate them anyway: a node that fails after the approval is retried. [LangGraph interrupts, Nov 2026](../sources/2026-11-12-langchain-langgraph-interrupts.md)

**If it runs twice**

- Give each tool a *replay policy*: declare whether it may run twice, and rerun only those tools after an interruption. Replay here means running the tool again, not rerunning workflow code as on [durable execution](durable-execution.md). [Pi Durable, Oct 2026](../sources/2026-10-01-earendil-pi-durable.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md)
- Never guess about the others. Record the outcome as unknown and tell the model, which can check the current state before trying again, though the state may not show how far a command got. [Pi on Temporal, Oct 2026](../sources/2026-10-08-temporal-immortal-life-of-pi.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md)
- Send an *idempotency key* with every side effect, and deduplicate at the receiver on a business identifier. A key taken from the step is stable across retries but differs between runs, so only a business identifier catches a second run, and the receiver must enforce both. [Running durable agents, Oct 2026](../sources/2026-10-15-vercel-running-durable-agents.md) · [What survives failure, Nov 2026](../sources/2026-11-04-temporal-deciding-what-survives-failure.md)

**After it went wrong**

- For every action that changes something, decide beforehand how it is reversed, and keep that path outside the agent: versions, backups it cannot alter, a delete that can be undone during a grace period, an owner who can remove what the agent posted. [Remediation, Jul 2025](../sources/2025-07-28-vanlightly-remediation.md) · [Railway, Apr 2026](../sources/2026-04-29-railway-ai-wants-to-nuke-your-database.md) · [Notion, Feb 2026](../sources/2026-02-27-notion-security-in-custom-agents.md)
- Expect no rollback across systems. [Determinism, Nov 2025](../sources/2025-11-24-vanlightly-determinism-in-durable-execution.md) Write an undo (a *compensation*) for each step. When a step gives up, run the undos in reverse order and include the failed step, because whether it took effect is unknown. This pattern is called a saga. Its source shows it for a fixed workflow; undoing steps that a model chose is not addressed. [Fault tolerance, Jun 2026](../sources/2026-06-04-langchain-fault-tolerance-in-langgraph.md)
- Check that the safeguards of the human interface also bind the API. One platform's dashboard held a volume deletion for 48 hours while its API ran the same deletion at once, for an agent that had found an account-wide token on disk. [Railway, Apr 2026](../sources/2026-04-29-railway-ai-wants-to-nuke-your-database.md)

## What is unsettled

- Three projects hand a call of unknown outcome to the model to resolve. [Pi Durable, Oct 2026](../sources/2026-10-01-earendil-pi-durable.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md) · [Pi on Temporal, Oct 2026](../sources/2026-10-08-temporal-immortal-life-of-pi.md) None reports how often the model resolves it correctly. That observation is this brain's reading.
- No source here covers an approval that goes stale: the state it was given for changes before the action runs.

## Related

[Durable execution](durable-execution.md) · [Human judgment](human-judgment.md) · [Permissions and sandboxing](sandboxing-and-permissions.md) · [Agent identity and tenancy](agent-identity.md) · [Background agents](background-agents.md) · [Tool design](tool-design.md)
