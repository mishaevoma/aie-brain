---
type: concept
title: "Agent interfaces"
updated: 2026-11-22
reviewed: 2026-11-22
status: evolving
---

# Agent interfaces

An agent interface is where people give work, receive results, answer questions and review proposed actions. A **conversation** is the thread they interact with. A **session** holds the agent's execution state and intermediate calls. Suh proposes making those separate platform objects. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md)

## Why it matters

Background agents can produce work faster than people can review it. LangChain reports replacing a slow Slack review backlog with a custom screen, and treating each check-in as a cost to the person's attention. [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md)

## What to do

- Make contacting a person an explicit tool call. Store the waiting state and resume the run when the answer arrives. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Make review items quick to judge. Lead with a short account of the result and the action needed, deliver it where the work began, and measure the share of check-ins people act on. [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md)
- Evaluate a conversation layer that receives deliberate messages from the agent, with session traces available for debugging. Suh proposes this as the primary interface for his platform vision. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md)
- For unattended work, consider an inbox of approvals and questions with apps for reviewing intermediate results. This is Suh's proposal, and LangChain's experience supports making review a deliberate part of the product. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md) · [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md)

## Editable apps

Suh uses **app (artifact)** for a customizable interface whose code lives in the user's filesystem. Even the conversations page could be forked and changed by an agent. He expects embedded apps, apps with chat alongside, terminal-style panes, canvases, windows and panels to coexist. The proposal makes tenant-specific review workflows part of the platform's extension model. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md)

His claim that these platforms will absorb vertical SaaS is a market prediction. This brain's reading is to test the concrete need for customer-specific interfaces and the cost of maintaining them. The source provides no comparative usability study or production outcomes. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md)

## Relation to shared run history

Harvey describes one run reached from several surfaces, while Suh argues for a conversation separate from execution internals. This brain's reading is that a shared execution record can support a conversation view and a debugging view, each exposing the information its reader needs. The source of truth and what the interface displays are separate design decisions. [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md)

## Related

[Agent platforms](agent-platforms.md) · [Background agents](background-agents.md) · [Harness](harness.md) · [Human judgment](human-judgment.md) · [Side effects and approvals](side-effects.md)
