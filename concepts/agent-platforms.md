---
type: concept
title: "Agent platforms"
updated: 2026-11-18
reviewed: 2026-11-18
status: evolving
---

# Agent platforms

**Definition:** The shared infrastructure that agents run on once they leave a laptop, also called an *agent runtime*. A [harness](harness.md) makes one agent good. A platform keeps many of them running, for many people, through crashes, deploys and waits.

## Why it matters

Teams that put agents into production end up building the same parts, and a second agent built without them needs a second platform. [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md) The parts can also be rented, which is a decision of its own: see [managed agent runtimes](managed-agent-runtimes.md).

## The parts

| Part | Job |
|---|---|
| Session record | Append-only history of a run. The source of truth, which outlives every process |
| Loop host | Runs the harness on a disposable worker that resumes from the record |
| Sandbox | Where commands and model-written code run |
| Tool gateway | One audited route to other systems, where permissions and policy are checked |
| Credentials proxy | Adds credentials to requests outside the sandbox. Some platforms give the sandbox short-lived, scoped credentials instead |
| Triggers | Chat, the issue tracker, the code host, schedules, events |
| Queue | Admits, orders and limits runs |
| Traces | Every model and tool call of a run, with its cost |

Sources: [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) · [Deep Agents runtime, Apr 2026](../sources/2026-04-20-langchain-runtime-behind-deep-agents.md) · [Sierra Pinecone, Jul 2026](../sources/2026-07-15-sierra-pinecone-wisdom-of-the-workforce.md).

## What to do

- Make the session or run record the durable object, and start a fresh worker from it for each slice of work. [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Run the loop outside the sandbox and reach the sandbox through tool calls, a design called *sandbox as a tool*. A broken sandbox then costs a retry, and credentials and approvals stay out of reach of generated code. One team says this boundary cannot be retrofitted. [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md) · [Rivet, Jul 2026](../sources/2026-07-27-rivet-harness-outside-the-sandbox.md) · [OpenAI Agents SDK, Apr 2026](../sources/2026-04-15-openai-next-evolution-agents-sdk.md)
- Start a sandbox only when a task needs one, from an image, snapshot or warm pool prepared ahead of time. [Atlassian, Aug 2026](../sources/2026-08-26-atlassian-rovo-agent-harness.md) · [Ramp, Jan 2026](../sources/2026-01-12-ramp-background-agent.md) · [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md)
- Release compute while a run waits (hibernation). In a trace study Google cites, coding agents waited on their user for about 80% of a session. Google's cost model has parking pay only below about 4 prompts an hour and from about 37 sessions. [Google, Nov 2026](../sources/2026-11-16-google-agents-are-sessions.md) · [Sierra, Jul 2026](../sources/2026-07-29-sierra-agency-sandboxes-for-agents.md)
- Define each agent as configuration on the platform: Shopify's *profile* bundles a system prompt, skills, extensions, a sandbox policy and model defaults, and DoorDash's *playbook* a reusable task. Serve interactive, event-driven and batch work from the same parts. [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md)
- Let every surface point at the same run, so that chat, the web page and the pull request show one history. [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) Decide what a message that arrives mid-run does. For this *double-texting* LangChain offers queue (its default, and the safest), reject, interrupt or roll back, and interrupting leaves half-finished tool calls. Ramp calls a message that redirects a running agent *steering*. [Deep Agents runtime, Apr 2026](../sources/2026-04-20-langchain-runtime-behind-deep-agents.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md)
- Wrap vendor harnesses behind your own interface, so that a model or harness can be replaced and a fix ships once. [Sierra Pinecone, Jul 2026](../sources/2026-07-15-sierra-pinecone-wisdom-of-the-workforce.md) · [Spotify, Nov 2025](../sources/2025-11-06-spotify-background-coding-agent-part-1.md) This pulls against sandbox as a tool, because Claude Code and Codex expect to run inside the sandbox. Sierra runs them there. [Rivet, Jul 2026](../sources/2026-07-27-rivet-harness-outside-the-sandbox.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md)

## Where the loop runs

| Shape | Suits | Watch for |
|---|---|---|
| An actor per agent, asleep when idle | Many agents that mostly wait | Recovery is code you write, and the process can be evicted at any moment |
| A workflow per session | Recovery to the exact step, long waits | Determinism rules, history limits, and a price per step on metered plans |
| Functions with a queue and a session log | Ordinary serverless hosting | Time limits. You build the leases and the requeueing |
| A machine per session | An unmodified harness that needs a full computer | Caps on session length, and snapshots that keep only files unless taken at the hypervisor |

Sources, in row order: [Project Think, Apr 2026](../sources/2026-04-15-cloudflare-project-think.md) and [Cloudflare docs, Oct 2026](../sources/2026-10-27-cloudflare-long-running-agents.md) · [Temporal harness, Aug 2026](../sources/2026-08-20-temporal-agent-harness.md), [Pydantic AI docs, Nov 2026](../sources/2026-11-17-pydantic-durable-execution.md) and [Diagrid pricing, Sep 2026](../sources/2026-09-17-diagrid-durable-execution-pricing.md) · [Cramer, Jul 2026](../sources/2026-07-02-cramer-building-an-intern.md) · [AgentCore, Jun 2026](../sources/2026-06-08-aws-hosting-coding-agents-on-agentcore.md), [Sprites block device, Oct 2026](../sources/2026-10-22-fly-sprites-block-device.md) and [Cognition, Apr 2026](../sources/2026-04-23-cognition-what-we-learned-building-cloud-agents.md). The grouping into four shapes is this brain's reading.

Decide the form before the engine: work that starts and ends is a *session*, and a thing whose identity outlives any task is an *actor*. [Three forms, Dec 2025](../sources/2025-12-10-vanlightly-three-durable-function-forms.md) Mapping an agent run to a session and a standing agent to an actor is this brain's reading. How each shape records progress is on [durable execution](durable-execution.md).

## Where sources disagree

- **Should an endless agent loop be a workflow?** One actor vendor says no: replay keeps growing, every deploy lands mid-run, and a workflow cannot hold a live connection. [Rivet, Jul 2026](../sources/2026-07-27-rivet-harness-outside-the-sandbox.md) Vercel's own benchmark later put the overhead late in a 1,020-step run at 70 ms at p75, for one workload in one region on one day. [Workflow SDK 5, Nov 2026](../sources/2026-11-12-vercel-workflow-sdk-5.md) This brain's reading: that answers the cost of replay, not the other two objections.
- **Is the sandbox disposable?** Shopify, Harvey, Stripe and Anthropic's hosted agents treat it so. [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md) Fly.io and Cognition argue for a durable machine that is snapshotted and woken, Cognition's with memory included. [Code And Let Live, Jan 2026](../sources/2026-01-09-fly-code-and-let-live.md) · [Cognition, Apr 2026](../sources/2026-04-23-cognition-what-we-learned-building-cloud-agents.md) Google and Sierra keep an idle sandbox's state and free its machine. [Google, Nov 2026](../sources/2026-11-16-google-agents-are-sessions.md) · [Sierra, Jul 2026](../sources/2026-07-29-sierra-agency-sandboxes-for-agents.md)

## Related

[Managed agent runtimes](managed-agent-runtimes.md) · [Durable execution](durable-execution.md) · [Background agents](background-agents.md) · [Agent identity and tenancy](agent-identity.md) · [Harness](harness.md) · [Permissions and sandboxing](sandboxing-and-permissions.md)
