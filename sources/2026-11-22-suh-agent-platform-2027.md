---
type: source
title: "Agent platform of 2027"
author: "John Suh"
publisher: "@john_ssuh on X"
url: https://x.com/john_ssuh/status/2124336124172935336
published: 2026-11-22
ingested: 2026-11-22
kind: x-post
read: full
concepts: [agent-identity, agent-interfaces, agent-platforms, agents-and-workflows, background-agents, durable-execution, harness, knowledge-factory, memory, multi-agent-systems, sandboxing-and-permissions]
updated: 2026-11-22
---

# Agent platform of 2027

Suh predicts an extensible operating system for agents, combining independent runtimes, shared files, conversations, event listeners, durable workflows and apps users can ask agents to modify.

## What it says

- He expects an independent company to own this application layer, with existing software supplying its data. This is his market prediction.
- **Actors and definitions.** He predicts a move from Temporal-style hosting to independent actor runtimes where harnesses can write extensions and hooks, with different loops sharing a backend. Agent definitions should be separate from instances and sessions. He favours supporting both general agents and bespoke definitions. His reading of *Formalizing Fermat's Last Theorem* is that its shell-and-editor tool set illustrates a preference for focused agents.
- **Computers and files.** Agents should use checkpointed cloud sandboxes from several providers and people's local computers. The number of agents and computers can vary independently. A shared cloud POSIX filesystem holds code, definitions, files and apps. Access control belongs to that filesystem, independently of a computer, and may follow the agent, the person starting a turn, or both. He also proposes directory-level git or jj and `.env` files.
- **Conversations and inboxes.** A conversation should behave like a channel or email thread. Tools publish messages intended for people, while session internals remain available for debugging. A focused inbox gathers approvals, questions and tenant-specific apps for reviewing intermediate work.
- **Listeners.** Agents should create per-tenant subscriptions to WSS, Kafka or change data capture (CDC), filtering events through code or a model into actionable signals. Filters may change for a time window or batch messages across accounts. He presents this as a broader mechanism than the cron jobs and webhook plugins he sees in current products.
- **Workflows.** Agents should write durable workflows per tenant, mixing deterministic and agentic steps on the platform that already handles API and MCP traffic. He prefers custom code to drag-and-drop tools such as n8n and the original Zapier.
- **Apps.** Interfaces, including the conversations page, should be editable artifacts in the user's filesystem. Users could ask agents to adapt them to their business. He expects multiple representations and containers, including embedded apps, an app with chat alongside it, terminal-style panes, infinite canvases, layered windows and resizable panels. He challenges the original vertical SaaS thesis because workflows within one industry still differ by company.
- In a [follow-up on 22 November](https://x.com/john_ssuh/status/2124399508536869160), he calls company knowledge and memory largely solved through dreaming agents over permissioned files. He proposes an append-only `memory_log.md` and a derived `memory_current.md`, with directories for users, organisations, conversations and clients. Search can mirror the filesystem as it grows, with Turbopuffer named. He allows that choosing how dreaming works for a company may remain hard.

## What to do with it

- Use the proposal to review platform extension points, including agent definitions, computers, filesystem permissions, listeners, workflows and editable apps.
- Design deliberate messages and review surfaces for people, with session traces available for inspection.
- Evaluate isolation and recovery separately when considering agents that modify their own harnesses.

## Terms

- **Conversation** — The thread people interact with, distinct from execution state.
- **Listener / monitor** — A tenant-defined event subscription that produces signals for an agent.
- **App (artifact)** — An interface stored as code that the user can customize.

## Caveats

- Read the full caption, all four attached images and the linked follow-up. There is no separate article URL.
- A product vision with no reliability, safety, cost or usability measurements. The author's profile says he is building.
- The Temporal, market and memory claims are his assessments. The Fermat paper and named products were not independently checked. Actor isolation alone establishes no security or recovery guarantee.
