---
type: concept
title: "Running agents in production"
updated: 2026-11-18
reviewed: 2026-11-17
status: evolving
---

# Running agents in production

**Definition:** Keeping an AI product's quality steady after launch: catching regressions caused by infrastructure and harness changes, deploying without breaking agents that are mid-task, and scaling the systems around them.

## Why it matters

Quality can fall while the model stays the same, and pre-release evals will not show it. Two published postmortems make the point from different layers. In 2025, three serving bugs (misrouted requests, corrupted output, a sampling miscompilation) degraded responses. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md) In 2026, three harness changes (a lower default effort, a bug that discarded reasoning, a terse-output prompt line) made a coding product feel worse. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)

## What to do

**Catch regressions**

- Run quality evals continuously against the production serving path, not only against the model before release. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md)
- Add cheap sanity checks on output to deploy gates, and correlate spikes in complaints with recent changes. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md)
- Gate harness changes (defaults, context pruning, system prompts) like a model swap, with a broad per-model suite. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Use the exact build you ship, and roll out anything that trades quality for speed gradually, with a soak period. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Let users opt down in reasoning effort instead of lowering the default to save latency. [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Re-check any model judge against a domain expert's labels on fresh production samples. Agreement measured once does not hold as inputs change. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- If you tune sampling parameters, re-check them after a provider changes its internals. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md)

**Deploy and recover**

- Make agents resumable from checkpoints, and tell the agent when a tool fails so it can adapt. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Use a rainbow deployment: shift traffic gradually between versions running side by side, so running agents are not broken mid-task. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)
- Ship prompts, tool descriptions, schemas, guardrails and model settings with the code as one release. A run that resumes on a changed tool description misreads its own history, and nothing fails. [Updating agents safely, Mar 2026](../sources/2026-03-11-restate-updating-agents-safely.md)
- Decide what happens to runs in flight, where vendors differ. Restate keeps every run on the release it started on (version pinning), and moving one is a logged exception. [Updating agents safely, Mar 2026](../sources/2026-03-11-restate-updating-agents-safely.md) Temporal decides by run length against deploy frequency: pin runs that finish before the next deploy, and upgrade and patch longer ones. A run of weeks that hands over to a fresh run can instead stay pinned and change version at the hand-over, a feature in preview in March 2026. [Worker versioning, Mar 2026](../sources/2026-03-30-temporal-worker-versioning-ga.md)
- Remember that a fix never reaches a pinned run. Cancel it and restart on the corrected release, after checking how the new run treats actions already completed. [Running durable agents, Oct 2026](../sources/2026-10-15-vercel-running-durable-agents.md)
- Do not count on the platform to wait. After a deploy a Cloudflare Durable Object now keeps its old code while it waits to hibernate, by default for up to 300 seconds and at most for 24 hours, as a best effort. [Deferred code updates, Oct 2026](../sources/2026-10-30-cloudflare-durable-objects-defer-code-updates.md)
- Keep a durable session log and a stateless loop. Creating sandboxes only when needed cut median time to first token by about 60% in one hosted service. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Store each run as one thread of events and read its state from that: the current step, whether it is waiting, how often it has retried. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Trace decision patterns for debugging without reading conversation content. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)

**Scale the surroundings**

- Before adding agents, check whether source control, CI and review can take ten times the change volume. At one company merged changes went from about 2,500 a day to over 30,000 in four months, and the limit became infrastructure, not coding. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)
- Expose repository queries as APIs so agent jobs do not need full checkouts. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)
- Expect conflicts and catch regressions after merge. Merge queues and global locks did not hold at that volume. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)

**Queue and cost**

- Put admission control in front of agent work before scripts and other agents can start it from a command line. The queue, the limits and the cut-offs are on [background agents](background-agents.md). [Harvey talk, Nov 2026](../sources/2026-11-11-harvey-harness-has-to-finish-the-job.md)
- Know what waiting costs. A sandbox held for a session sits idle for most of it. A workflow engine charges little for the wait, and bills the steps and often the retries. [Google, Nov 2026](../sources/2026-11-16-google-agents-are-sessions.md) · [Diagrid pricing, Sep 2026](../sources/2026-09-17-diagrid-durable-execution-pricing.md)
- Account for cost and usage per run, and cap it with a budget that the runtime enforces. [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md) · [Meta, Mar 2026](../sources/2026-03-17-meta-ranking-engineer-agent.md)

**Stay observable**

- Plan security monitoring early. Isolating an agent in a virtual machine can hide its activity from the tools an enterprise already uses. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Expose each run as a stream of structured events that other services can subscribe to, and keep traces you can read end to end. [Temporal harness, Aug 2026](../sources/2026-08-20-temporal-agent-harness.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md)

- Decide who may read conversations. One practice traces decision patterns without reading content. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) Another makes reading whole interactions, with all their context on one screen, the central habit. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md) This brain's reading: which applies depends on what your users have agreed to.

**Internal agents**

- Build on an existing agent SDK and add your own knowledge, connections and skills. [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md)

## Related

[Evals](evals.md) · [Trusting eval numbers](eval-validity.md) · [Harness](harness.md) · [Long-running agents](long-running-agents.md) · [Durable execution](durable-execution.md) · [Agent platforms](agent-platforms.md) · [Background agents](background-agents.md) · [Side effects and approvals](side-effects.md) · [Permissions and sandboxing](sandboxing-and-permissions.md)
