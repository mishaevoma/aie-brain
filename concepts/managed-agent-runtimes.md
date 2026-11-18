---
type: concept
title: "Managed agent runtimes"
updated: 2026-11-18
reviewed: 2026-11-18
status: contested
---

# Managed agent runtimes

**Definition:** A managed agent runtime is a hosted service that runs part of an [agent platform](agent-platforms.md) for you: the loop, the session history, the sandboxes, or all of them. Model labs launched theirs in 2026, Anthropic's in April and OpenAI's in public beta in September. [Plumbing wars, Apr 2026](../sources/2026-04-28-proctor-plumbing-wars.md) · [OpenAI Agents API, Nov 2026](../sources/2026-11-17-openai-agents-api-architecture.md) Clouds rent isolated machines and the services around them. [AgentCore, Jun 2026](../sources/2026-06-08-aws-hosting-coding-agents-on-agentcore.md) The question they raise is whether to build or rent, and how much.

## Why it matters

The parts of a platform are a standing engineering project, and a rented runtime replaces them for a fee. In exchange you give up some control: over which models the loop can call when the runtime comes from a model lab, over where the session is stored, and over what you can inspect. A cloud runtime can host any model. [Plumbing wars, Apr 2026](../sources/2026-04-28-proctor-plumbing-wars.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md) · [AgentCore, Jun 2026](../sources/2026-06-08-aws-hosting-coding-agents-on-agentcore.md)

## What is for rent

| Level | You run | The vendor runs |
|---|---|---|
| Fully hosted | Your application | The loop, the session history, sandboxes, credential handling |
| Your sandbox | Workers in your network that execute the tool calls | The loop and the session history |
| The whole service on your side | Server, database, workers, and where model requests go | Supplies the software, in private beta |
| Your harness on rented machines | The harness, the model route, the network rules for shell traffic | An isolated machine per session with a workspace that outlives it, identity, a tool gateway, tracing |
| Nothing rented | Containers, session storage and all the rest | Only the model API |

Sources, in row order: [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md) · [OpenAI Agents API, Nov 2026](../sources/2026-11-17-openai-agents-api-architecture.md) and [Cursor, Sep 2026](../sources/2026-09-02-cursor-self-hosted-machines.md) · [Self-hosted Managed Agents, Nov 2026](../sources/2026-11-12-anthropic-self-hosted-managed-agents.md) · [AgentCore, Jun 2026](../sources/2026-06-08-aws-hosting-coding-agents-on-agentcore.md) · [Agent SDK hosting, Nov 2026](../sources/2026-11-17-anthropic-agent-sdk-hosting.md).

## What to do before renting

- Read what "durable" covers. One cloud separates three things: work that outlives the client's connection, work that survives the loss of its process, and a stream that clients can rejoin. Its recovery reruns the handler from the top, so checkpoints and repeat-safe side effects stay with you. [Foundry docs, Oct 2026](../sources/2026-10-14-microsoft-foundry-hosted-agent-resilience.md)
- Rebuild client state from the listed history, never from the stream or webhooks alone. A stream may carry only what is emitted after it opens. [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md)
- Find the limits before a long task does: how long a machine may run, the idle timeout, and how long a sandbox or workspace is kept. [AgentCore, Jun 2026](../sources/2026-06-08-aws-hosting-coding-agents-on-agentcore.md) · [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md) · [OpenAI Agents API, Nov 2026](../sources/2026-11-17-openai-agents-api-architecture.md)
- Check what still leaves your network at each level. With a self-hosted sandbox, conversation history, tool results, skills and memory stores still go to the vendor. [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md) · [Cursor, Sep 2026](../sources/2026-09-02-cursor-self-hosted-machines.md)
- Price the waiting, which vendors bill differently. Anthropic and OpenAI charge only while a session runs. AgentCore charges the CPU actually used plus the peak memory so far. Foundry bills CPU and memory during active sessions. [Plumbing wars, Apr 2026](../sources/2026-04-28-proctor-plumbing-wars.md) · [OpenAI Agents API, Nov 2026](../sources/2026-11-17-openai-agents-api-architecture.md) · [AgentCore, Jun 2026](../sources/2026-06-08-aws-hosting-coding-agents-on-agentcore.md) · [Foundry docs, Oct 2026](../sources/2026-10-14-microsoft-foundry-hosted-agent-resilience.md)
- Set network policy and a budget explicitly on every session. A default can be unrestricted. [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md)
- Keep your own copy of the session log and memory, with a readable twin of anything only the provider can decrypt. [Your harness, your memory, Apr 2026](../sources/2026-04-11-chase-your-harness-your-memory.md) · [Session portability, Jul 2026](../sources/2026-07-30-earendil-session-you-cannot-take-with-you.md)
- If you host the Claude Agent SDK yourself, plan for one process per session with its transcript, memory files and working directory on local disk. The store that mirrors transcripts elsewhere is best-effort, and after a resume it holds the only durable copy. [Agent SDK hosting, Nov 2026](../sources/2026-11-17-anthropic-agent-sdk-hosting.md)

## Where sources disagree: build or rent

- **Rent.** For a team committed to Claude, months of plumbing are replaced by a fee per active session-hour, and what sets a product apart is what the agent does, not how it runs. For everyone else, the same author says, it depends. [Plumbing wars, Apr 2026](../sources/2026-04-28-proctor-plumbing-wars.md) · [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md)
- **Build.** A team that tried the rented options first gives three reasons: freedom to change model provider, speed of changing the platform next to its product teams, and owning the traces. Others add that a hosted agent means sending code out or letting a third party in, and that a vendor's limits on sandbox resources, lifetime and concurrency would have become their product's limits. [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) · [Sierra, Jul 2026](../sources/2026-07-29-sierra-agency-sandboxes-for-agents.md)
- **What building costs.** Cognition, which sells a managed coding agent, counts over a year for its machines and over three quarters for orchestration. Ramp says version one of its platform took 6 weeks, that coding agents made the build cheap, and that it still needs experienced engineers on call. [Cognition, Apr 2026](../sources/2026-04-23-cognition-what-we-learned-building-cloud-agents.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md)
- **What locks you in.** Stored state: sessions, memory, and items only the provider can decrypt. Model APIs were easy to switch while they were stateless. [Your harness, your memory, Apr 2026](../sources/2026-04-11-chase-your-harness-your-memory.md) · [Session portability, Jul 2026](../sources/2026-07-30-earendil-session-you-cannot-take-with-you.md)

This brain's reading, which is a synthesis and not a source claim: most voices here sell a runtime, a harness or a product built on one. The positions still follow a pattern. Rent when one lab's models are enough and the session may sit on its servers, or rent from a cloud and attach the runtime to your own network, as one team did. [Axonius, Aug 2026](../sources/2026-08-18-aws-axonius-multi-tenant-agents.md) Build when you need to switch model providers, change the platform at your product's pace, read every trace, or keep code and customer data away from any third party. In both cases keep the session log yourself.

## Related

[Agent platforms](agent-platforms.md) · [Durable execution](durable-execution.md) · [Agent identity and tenancy](agent-identity.md) · [Memory](memory.md) · [Harness](harness.md)
