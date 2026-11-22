---
type: concept
title: "Background agents"
updated: 2026-11-22
reviewed: 2026-11-18
status: evolving
---

# Background agents

**Definition:** An agent that runs unattended in the cloud, is started from chat, a ticket, a schedule or an event instead of an open terminal, and comes back with something a person can review: a pull request, a report, a question. Also called a cloud agent. One that starts itself from events and schedules and decides when to involve a person is called a *proactive agent*.

## Why it matters

Unattended agents let one engineer run several sessions in parallel, and they move the bottleneck to that person's attention. [Dropbox, May 2026](../sources/2026-05-21-dropbox-introducing-nova.md) · [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md) Where companies publish figures, they are large: over 1,300 merged pull requests a week written only by the agent at Stripe, about 30% of the pull requests merged to Ramp's frontend and backend repositories, one in eight merged pull requests co-authored by the agent at Shopify, 130,000 engineering tasks in a month at DoorDash. [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md) · [Ramp, Jan 2026](../sources/2026-01-12-ramp-background-agent.md) · [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) Nobody watches the run, so isolation, verification and limits must do what a supervising person did.

## What to do

**Shape the run**

- Separate the conversation that clarifies a task from the run that carries it out. One company has an interactive agent gather the details and write the prompt, then hands it to the unattended one. [Spotify, Nov 2025](../sources/2025-11-06-spotify-background-coding-agent-part-1.md)
- Let isolation carry the safety. Stripe's agent runs with full permissions and no prompts, because its machine has no production access and a mistake stays inside it. [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md) Spotify narrows the agent instead: its container has few permissions, and pushing code and messaging people are done by the platform around it. [Spotify, Dec 2025](../sources/2025-12-09-spotify-feedback-loops-part-3.md)
- Wrap the agent in fixed steps and cap its loops: required checks as code, a limit on rounds of fixing, and a hand-back to a person at the limit. [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md) · [Dropbox, May 2026](../sources/2026-05-21-dropbox-introducing-nova.md)
- End every run in something reviewable, published under the identity of the person who asked. A pull request opened as the app lets people approve their own changes. [Ramp, Jan 2026](../sources/2026-01-12-ramp-background-agent.md)

**Trigger it where the work is**

- Start runs where the context already is: a chat thread whose content carries into the session, a comment on a pull request, the issue tracker. [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [Dropbox, May 2026](../sources/2026-05-21-dropbox-introducing-nova.md) · [Ramp, Jan 2026](../sources/2026-01-12-ramp-background-agent.md) · [Sierra Pinecone, Jul 2026](../sources/2026-07-15-sierra-pinecone-wisdom-of-the-workforce.md)
- Run in the open. One company's agent takes no direct messages, and its public transcripts are mined to improve it. Another saw adoption change when runs moved to public threads. [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md)
- Support three kinds of trigger: outside events, schedules a developer sets, and schedules the agent sets for itself. On LangChain's hosted product more than 70% of runs now start from a schedule. [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md)
- Send every trigger, a person's answer included, through a durable inbox with one active worker, starting with one inbox per user. Direct calls let simultaneous events start competing runs, and a crash loses the event. [Always-on agents, Nov 2026](../sources/2026-11-13-anthropic-building-always-on-agents.md)
- Consider tenant-defined **listeners** or **monitors** when a trigger needs custom filtering or batching. Suh proposes agents creating subscriptions to external streams and using code or a model to turn events into signals. This extends the existing trigger taxonomy, with implementation and delivery guarantees left open. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md)

**Protect the queue**

- Separate accepting a task from starting it (admission control). Harvey's cluster filled when one engineer started about 950 tasks from the command line in about 3 hours. It then added a fair queue: interactive work first, a concurrency limit per person, and a visible place in line. [Harvey talk, Nov 2026](../sources/2026-11-11-harvey-harness-has-to-finish-the-job.md)
- Attach a repeated trigger to the run that is already handling it. An alert storm at the same company started around 900 tasks in 4 hours, all chasing one bug. [Harvey talk, Nov 2026](../sources/2026-11-11-harvey-harness-has-to-finish-the-job.md)
- Give every automation a cut-off after consecutive failures, a budget and an expiry date. [Harvey talk, Nov 2026](../sources/2026-11-11-harvey-harness-has-to-finish-the-job.md)

**Spend attention carefully**

- Treat each check-in as a cost. Send few, lead with a headline and an explicit ask, and deliver them where people already work. Track the share that people act on. [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md) · [Always-on agents, Nov 2026](../sources/2026-11-13-anthropic-building-always-on-agents.md)
- Widen autonomy one kind of action at a time, once people stop correcting it. [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md)
- Launch with one frequent, measurable workflow, and measure outcomes such as the share of sessions that end in a merged pull request. [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) · [Ramp, Jan 2026](../sources/2026-01-12-ramp-background-agent.md)

Suh's proposed review inbox collects approvals, questions and apps that need human action. It serves the person reviewing work. The durable inbox above queues events for execution. This distinction is this brain's reading, and the interface choices are on [agent interfaces](agent-interfaces.md). [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md) · [Always-on agents, Nov 2026](../sources/2026-11-13-anthropic-building-always-on-agents.md)

## What is changing

- The coding agent moved off the laptop, for reasons companies repeat: limited resources and uptime, credentials that are too broad, and work nobody else can see or audit. One builder calls the months of agents on laptops a brief reversal of the long move to the cloud. [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) · [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md)
- The limit moves to merging. At Harvey pull requests rose about 60% in a month and a merge went from 15 to 30 minutes to over an hour, which the speaker calls unsolved. [Harvey talk, Nov 2026](../sources/2026-11-11-harvey-harness-has-to-finish-the-job.md) See [running agents in production](production-operations.md).

## Related

[Agent platforms](agent-platforms.md) · [Durable execution](durable-execution.md) · [Side effects and approvals](side-effects.md) · [Agent identity and tenancy](agent-identity.md) · [Verification](verification.md) · [Permissions and sandboxing](sandboxing-and-permissions.md) · [Human judgment](human-judgment.md)
