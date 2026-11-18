---
type: concept
title: "Agent identity and tenancy"
updated: 2026-11-18
reviewed: 2026-11-18
status: evolving
---

# Agent identity and tenancy

**Definition:** Whose authority an agent acts under, which credentials it can use, and how one customer's agents and data are kept apart from another's. Most actions involve three parties: the person who asked, the agent, and the platform that runs it. An agent can also act as itself. *Agent identity* is the agent's own verifiable identity. *Tenant isolation* is the separation between customers.

## Why it matters

At Uber, identity covered people and workloads, not something acting for someone else. When agents handed work to other agents, the system at the end saw a generic service identity, and the person who started the work was lost to audit and to access rules. [Uber, May 2026](../sources/2026-05-21-uber-solving-identity-crisis-for-ai-agents.md) A local agent has the opposite problem: it inherits its user's whole machine, so nobody can say what a run could reach. [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) And an unattended run holds a person's access with nobody watching. [Always-on agents, Nov 2026](../sources/2026-11-13-anthropic-building-always-on-agents.md)

## What to do

**Decide whose authority each action uses**

- Act on behalf of the person where the result should be attributed to them and limited by their rights. Open a pull request with the requester's token, and require the user's own grant for writes even where reads use a shared one. [Ramp, Jan 2026](../sources/2026-01-12-ramp-background-agent.md) · [Cramer, Jul 2026](../sources/2026-07-02-cramer-building-an-intern.md)
- Give a shared or always-running agent its own identity and an empty permission set that grows by explicit grants, so that it can be audited and switched off on its own. [Notion, Feb 2026](../sources/2026-02-27-notion-security-in-custom-agents.md) · [OpenAI, Nov 2026](../sources/2026-11-12-openai-securing-persistent-agents.md)
- Carry the actor chain, the user and every agent in between, in each credential. Mint it centrally for one hop and a few minutes. A tool should not forward the token it received; it should exchange it for a new one. [Uber, May 2026](../sources/2026-05-21-uber-solving-identity-crisis-for-ai-agents.md) · [IETF draft, Nov 2026](../sources/2026-11-02-ietf-ai-identity-management-system.md)
- Withhold write credentials from scheduled runs until you can tell who created the task, because a harmful task could be planted unnoticed. The builder who does this keeps some read access and calls the problem unsolved. [Cramer, Jul 2026](../sources/2026-07-02-cramer-building-an-intern.md)

**Keep credentials out of reach**

- Hold credentials in a vault or broker outside the place where model-written code runs, and attach them at a proxy for the hosts they are meant for. Sierra keeps API keys and secrets out of the sandbox by default, and the IETF draft has the agent never handle the user's credentials. [Sierra, Jul 2026](../sources/2026-07-29-sierra-agency-sandboxes-for-agents.md) · [IETF draft, Nov 2026](../sources/2026-11-02-ietf-ai-identity-management-system.md) Anthropic's hosted agents work this way with exceptions: sandbox code can still use credentials swapped in at egress, and a token obtained by exchange arrives unredacted. [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md)
- Company platforms often accept credentials inside the sandbox instead: injected when a run starts, scoped to that run and short-lived. [Harvey, Apr 2026](../sources/2026-04-07-harvey-building-spectre.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md)
- Check permissions at the point where a tool call leaves the sandbox, in a service the agent cannot change. [Atlassian, Aug 2026](../sources/2026-08-26-atlassian-rovo-agent-harness.md) · [Rivet, Jul 2026](../sources/2026-07-27-rivet-harness-outside-the-sandbox.md)

**Keep tenants apart**

- Treat multi-tenancy as three designs: isolating one user's data from another's, letting the agent use a user's delegated credentials, and deciding who may operate the deployment. [Deep Agents runtime, Apr 2026](../sources/2026-04-20-langchain-runtime-behind-deep-agents.md)
- Choose where isolation is enforced: in application code on a shared runtime (pool), at a gateway that swaps in tenant-scoped credentials (bridge), or in a runtime per customer (silo). Axonius chose the silo and paid in an account quota, onboarding delay and hundreds of runtimes to operate. [Axonius, Aug 2026](../sources/2026-08-18-aws-axonius-multi-tenant-agents.md)
- Cap spend per tenant or per session with a hard stop, not only an alarm. [Axonius, Aug 2026](../sources/2026-08-18-aws-axonius-multi-tenant-agents.md) · [Managed Agents docs, Nov 2026](../sources/2026-11-17-anthropic-managed-agents-overview.md)

**Make it auditable**

- Log every tool call at one gateway with the agent, the person it acted for, the action and the decision. [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) · [IETF draft, Nov 2026](../sources/2026-11-02-ietf-ai-identity-management-system.md)
- Back a sensitive action with a grant from the authorization system. An approval clicked inside the agent's own interface is not authorization by itself. The draft admits that its flow for confirming out of band fits badly when confirmation is needed mid-run. [IETF draft, Nov 2026](../sources/2026-11-02-ietf-ai-identity-management-system.md)

## What is unsettled

- The standards are still drafts. The identity model above rests on a working-group draft and on one company's own token format. [IETF draft, Nov 2026](../sources/2026-11-02-ietf-ai-identity-management-system.md) · [Uber, May 2026](../sources/2026-05-21-uber-solving-identity-crisis-for-ai-agents.md)
- Where credentials should live is argued: outside the sandbox at a proxy, or inside it, scoped and short-lived.
- On tenancy this brain holds one production case. Rate and concurrency limits per customer, noisy neighbours and data residency are not yet covered by a team that runs them. See the [watchlist](../watchlist.md).

## Related

[Permissions and sandboxing](sandboxing-and-permissions.md) · [Side effects and approvals](side-effects.md) · [Agent platforms](agent-platforms.md) · [Background agents](background-agents.md) · [MCP](mcp.md)
