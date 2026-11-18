---
type: source
title: "Durable, flexible multi-agent systems"
author: "Melanie Warrick"
publisher: Temporal
url: https://temporal.io/blog/durable-flexible-multi-agent-systems
published: 2026-08-06
ingested: 2026-11-17
kind: article
read: full
concepts: [side-effects]
---

# Durable, flexible multi-agent systems

**In one line:** Treat a person as a slow asynchronous API: an operator's interruption is a signal to the workflow that bypasses the model, an agent's question is a tool that suspends on a signal, and waits and timeouts live in recorded history, not memory.

## What it says

- **The demo.** Three agents run a delivery fleet, built on Google ADK, on LangGraph and on the two combined, with Temporal recording every model and tool call as an Activity.
- **A human interrupts.** When an operator alters an order in transit, the Workflow holds on `wait_condition` until that operator's decision arrives as a Temporal Signal. The gate is workflow code, not an LLM tool: a person's stop is never routed through a model.
- **The agent asks a human.** `ask_human` is one tool among the agent's others, called on its own judgement. Where other tools run as Activities, this one triggers LangGraph's `interrupt()`; the Workflow parks until a Signal arrives, then resumes the graph with the answer. The dashboard, a Temporal client, sends that Signal when the operator approves.
- **Durable timeouts.** `wait_condition` takes a timeout, and Temporal's Timers survive a crash as the wait does. The timeout plus a branch gives escalation to a backup after four hours, or automatic rejection after a day.
- **Why the wait must be durable.** Approvals take hours or days while clusters deploy daily and Workers crash. A wait held in process memory vanishes silently: nobody is paged, and no eval catches it because the trace just ends. A parked Workflow uses no compute; its pending decision sits in the Event History.
- **What a crash costs.** Temporal records progress at the edge of each Activity, not within a model call. A finished call returns its recorded result on replay: no new request, no second charge. A call still running when the Worker died cannot pick up mid-token; the Activity retries from the start and is paid for again. So any tool that changes the outside world needs an idempotency key or a guard against duplicates.
- **Operations.** Model calls starved driver navigation until each got its own Task Queue. Endless loops use Continue-as-New past a history threshold, carrying live state forward.
- **When to skip it.** Workflow code must be deterministic, Temporal runs beside the application, and its concepts take learning. The post grants that agents which neither wait on anything slow nor must outlive a crash may not need this yet.
- LangGraph's `interrupt()` is durable only with a persistent checkpointer; the demo's is in-memory, so Temporal's history preserves the pause.

## What to do with it

- Deliver stop, cancel and change requests to orchestration code, never through the model.
- Give the agent an ask-a-human tool, implemented as a durable wait with a timeout and an escalation branch.
- Add an idempotency key to every tool with a side effect.

## Terms

- **Signal** — a message sent from outside to a running Workflow.
- **Continue-as-New** — starting a fresh Workflow Execution with carried-over state so history stays bounded.

## Caveats

- By a Temporal developer advocate, about a demo; no production data or measurements.
- The rule against routing a stop through a model is stated, not argued.
