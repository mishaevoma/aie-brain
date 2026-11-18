---
type: concept
title: "Running agents in production"
updated: 2026-11-17
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
- Keep a durable session log and a stateless loop. Creating sandboxes only when needed cut median time to first token by about 60% in one hosted service. [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Store each run as one thread of events and read its state from that: the current step, whether it is waiting, how often it has retried. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Trace decision patterns for debugging without reading conversation content. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md)

**Scale the surroundings**

- Before adding agents, check whether source control, CI and review can take ten times the change volume. At one company merged changes went from about 2,500 a day to over 30,000 in four months, and the limit became infrastructure, not coding. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)
- Expose repository queries as APIs so agent jobs do not need full checkouts. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)
- Expect conflicts and catch regressions after merge. Merge queues and global locks did not hold at that volume. [Source control, Oct 2026](../sources/2026-10-13-anthropic-redesigning-source-control.md)

**Stay observable**

- Plan security monitoring early. Isolating an agent in a virtual machine can hide its activity from the tools an enterprise already uses. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

- Decide who may read conversations. One practice traces decision patterns without reading content. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) Another makes reading whole interactions, with all their context on one screen, the central habit. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md) This brain's reading: which applies depends on what your users have agreed to.

**Internal agents**

- Build on an existing agent SDK and add your own knowledge, connections and skills. [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md)

## Related

[Evals](evals.md) · [Trusting eval numbers](eval-validity.md) · [Harness](harness.md) · [Long-running agents](long-running-agents.md) · [Permissions and sandboxing](sandboxing-and-permissions.md)
