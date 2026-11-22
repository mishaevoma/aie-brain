---
type: concept
title: "Permissions, sandboxing and containment"
updated: 2026-11-22
reviewed: 2026-11-17
status: evolving
---

# Permissions, sandboxing and containment

**Definition:** The controls on what an agent may do. A *gate* decides whether a proposed action runs: a person, a rule or a classifier. A *sandbox* limits what any action can reach: files, network, credentials. *Containment* means capping the damage of a failure by construction instead of supervising each step.

## Why it matters

Risk is the likelihood of a failure times its blast radius, and giving an agent more access raises the second. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) In early 2025 the usual control was still a person: risky write actions were approved or carried out by hand. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md) Asking a person to approve each action does not hold up: Claude Code users accepted about 93% of permission prompts, and people who approve nearly everything stop reading what they approve, which is called approval fatigue. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md) · [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)

## What to do

**Build the deterministic boundary first**

- Limit the filesystem and the network together, at the operating-system level so child processes inherit the limits. With only one of the two, a hijacked agent can leak secrets or tamper its way out. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- Deny network by default and send all traffic through a proxy with a domain allow-list. Treat each allowed domain as a capability you are granting. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Keep real credentials outside the sandbox. Give it a scoped stand-in and let a proxy attach the real token after checking the request. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Use a disposable environment per session where data is sensitive. [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Keep the agent loop outside the sandbox, with the session history, credentials and approval checks. Assume that anything reachable from inside will be leaked or abused, and that a check enforced inside can be bypassed. [Rivet, Jul 2026](../sources/2026-07-27-rivet-harness-outside-the-sandbox.md)
- Keep whatever configures the agent out of its reach, since an agent can rewrite its own configuration. OpenAI treats the agent, its environment and its code as untrusted, and runs the gateway that configures the agent apart from the harness. [OpenAI, Nov 2026](../sources/2026-11-12-openai-securing-persistent-agents.md)
- Start from no access and grant capabilities one at a time, instead of starting broad and taking away. [Project Think, Apr 2026](../sources/2026-04-15-cloudflare-project-think.md) · [Notion, Feb 2026](../sources/2026-02-27-notion-security-in-custom-agents.md)

**Then add a gate**

- A model-based gate is a second layer, never the boundary. The classifier behind Claude Code's auto mode misses 17% of real overeager actions at a 0.4% false-positive rate. Every vendor that ships such a gate says the same. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Do not let a detection product stand in for the boundary either. No filter stops injected instructions every time, and one that catches 95% of attacks fails by the standard of application security. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md)
- Make the judge reasoning-blind: show it only the user's words and the proposed action. Hide the agent's reasoning and tool output, so neither can argue its case or carry an injection. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- Use a cheap filter that leans towards blocking, and escalate only flagged cases to a slower pass. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- Return a denial as something the agent can read and route around, and hand back to a person after a set number of denials. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Keep a person's approval for the few high-stakes write actions, and let code, not the model, decide which calls wait for it. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md) · [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md)
- Drop broad allow rules, such as blanket shell access, when approvals are automatic. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)

**Treat content as untrusted**

- Repository instruction files, tool results, web pages, email and data from connectors are all input an attacker can write. A model cannot reliably tell instructions hidden there from yours, which is a prompt injection. It is a different problem from jailbreaking, where someone talks the model itself into misbehaving. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Avoid the lethal trifecta: access to private data, exposure to untrusted content and a way to send data out, all in one agent. For each agent, list which of the three it has, and remove one. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md) · [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Count the routes for exfiltration generously. Any network request can carry data out, and so can an image that loads or a link shown to the user. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md)
- Load no project configuration before the trust decision. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

A boundary limits what an action can reach. Approving, repeating and undoing the actions that get through is on [side effects and approvals](side-effects.md).

**Fit it to the user**

- Match isolation to who is supervising. Developers can handle prompts. Non-developers need a boundary that is always on. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)
- Cut repeated prompts at the source by pre-approving safe read-only commands. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md)
- Review your own proxies and glue code hardest. Standard primitives held up better than custom parts. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

## Evidence

- Moving from prompts to a sandbox cut permission prompts by 84% internally. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- Data theft through injected instructions keeps being shown against shipped products. One list has 14 cases going back to April 2023, and 3 more from the weeks before it was written. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md)
- In an internal test, a pasted prompt sent out cloud credentials 24 times out of 25. Only network and filesystem limits could stop it. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

## Agent-written extensions and protected configuration

Suh's proposed platform lets agents write harness extensions and hooks in independent actor runtimes. OpenAI's deployment puts the gateway that configures an agent beyond its reach and treats its generated code as untrusted. The tension is how much configuration an agent may change. [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md) · [OpenAI, Nov 2026](../sources/2026-11-12-openai-securing-persistent-agents.md)

This brain's reading is to permit extension code only within a boundary enforced by the host, with permission rules, credentials and audit controls outside the writable area. Actor isolation by itself supplies no stated guarantee that those controls cannot be modified. Shared filesystem permissions also need their own enforcement, discussed under [agent identity](agent-identity.md). [Suh, Nov 2026](../sources/2026-11-22-suh-agent-platform-2027.md) · [Rivet, Jul 2026](../sources/2026-07-27-rivet-harness-outside-the-sandbox.md)

## Open problems

Memory poisoning, trust escalation through subagent output, and agent identity. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) Current practice on the last of these is on [agent identity and tenancy](agent-identity.md).

On the provider side, the same principle appears as confidential inference: shrink the code that can see plaintext to one small attested component. [Confidential inference, Jun 2025](../sources/2025-06-18-anthropic-confidential-inference.md)

## Related

[Harness](harness.md) · [MCP](mcp.md) · [Memory](memory.md) · [Side effects and approvals](side-effects.md) · [Agent identity and tenancy](agent-identity.md) · [Agent platforms](agent-platforms.md) · [Running agents in production](production-operations.md)
