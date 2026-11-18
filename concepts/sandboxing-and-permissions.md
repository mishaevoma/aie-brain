---
type: concept
title: "Permissions, sandboxing and containment"
updated: 2026-11-17
reviewed: 2026-11-17
status: evolving
---

# Permissions, sandboxing and containment

**Definition:** The controls on what an agent may do. A *gate* decides whether a proposed action runs: a person, a rule or a classifier. A *sandbox* limits what any action can reach: files, network, credentials. *Containment* means capping the damage of a failure by construction instead of supervising each step.

## Why it matters

Risk is the likelihood of a failure times its blast radius, and giving an agent more access raises the second. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) Asking a person to approve each action does not hold up: Claude Code users accepted about 93% of permission prompts, and people who approve nearly everything stop reading what they approve, which is called approval fatigue. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md) · [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)

## What to do

**Build the deterministic boundary first**

- Limit the filesystem and the network together, at the operating-system level so child processes inherit the limits. With only one of the two, a hijacked agent can leak secrets or tamper its way out. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- Deny network by default and send all traffic through a proxy with a domain allow-list. Treat each allowed domain as a capability you are granting. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Keep real credentials outside the sandbox. Give it a scoped stand-in and let a proxy attach the real token after checking the request. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Use a disposable environment per session where data is sensitive. [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)

**Then add a gate**

- A model-based gate is a second layer, never the boundary. The classifier behind Claude Code's auto mode misses 17% of real overeager actions at a 0.4% false-positive rate. Every vendor that ships such a gate says the same. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Make the judge reasoning-blind: show it only the user's words and the proposed action. Hide the agent's reasoning and tool output, so neither can argue its case or carry an injection. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- Use a cheap filter that leans towards blocking, and escalate only flagged cases to a slower pass. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- Return a denial as something the agent can read and route around, and hand back to a person after a set number of denials. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Drop broad allow rules, such as blanket shell access, when approvals are automatic. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)

**Treat content as untrusted**

- Repository instruction files, tool results and data from connectors are all input an attacker can write. Instructions hidden there are a prompt injection. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Avoid the lethal trifecta: access to private data, exposure to untrusted content and a way to send data out, all in one agent. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Load no project configuration before the trust decision. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

**Fit it to the user**

- Match isolation to who is supervising. Developers can handle prompts. Non-developers need a boundary that is always on. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Cut repeated prompts at the source by pre-approving safe read-only commands. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md)
- Review your own proxies and glue code hardest. Standard primitives held up better than custom parts. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

## Evidence

- Moving from prompts to a sandbox cut permission prompts by 84% internally. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- In an internal test, a pasted prompt sent out cloud credentials 24 times out of 25. Only network and filesystem limits could stop it. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

## Open problems

Memory poisoning, trust escalation through subagent output, and agent identity. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

On the provider side, the same principle appears as confidential inference: shrink the code that can see plaintext to one small attested component. [Confidential inference, Jun 2025](../sources/2025-06-18-anthropic-confidential-inference.md)

## Related

[Harness](harness.md) · [MCP](mcp.md) · [Memory](memory.md) · [Running agents in production](production-operations.md)
