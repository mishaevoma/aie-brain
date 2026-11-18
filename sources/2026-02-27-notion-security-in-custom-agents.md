---
type: source
title: "How we built security into Custom Agents"
author: "Sean Keenan, Jacob Brackett"
publisher: Notion
url: https://www.notion.com/blog/how-we-built-security-into-custom-agents
published: 2026-02-27
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, mcp, sandboxing-and-permissions, side-effects]
---

# How we built security into Custom Agents

**In one line:** An agent shared by a team needs its own permission model: start it with no access, grant per resource, add narrow permissions that fit how it is triggered, and give its owner a way to undo what it did.

## What it says

- Most agents are built for one user and inherit that user's permissions. An agent in a collaborative workspace is different: full access is dangerous and no access is useless.
- **Build from nothing.** A Custom Agent starts with no permission to read, write or interact with anything. The contrast drawn is with personal assistants that start broad and depend on safety instructions surviving in the context. Safety is placed in access control and deterministic code, not in the model's judgment.
- **Grant per resource.** View or edit access to specific pages. A first-party Slack integration with fine-grained permissions. A choice of confirming before each email is sent. For MCP integrations, which are not resource-based, a choice of which tools are available and whether each kind of action asks first or is always allowed.
- **Layers at run time.** Permission controls plus mitigations for prompt injection. The system is not designed on the assumption that every injection is caught. External data is tagged and monitored, and when something looks like an attack the agent is stopped and a user is asked to confirm.
- **Warnings.** While configuring a risky agent, the builder sees confirmations that can go as far as requiring a workspace admin's approval. While running, a risky action must be confirmed by an owner of the agent.
- **Remediation.** If the agent posts something wrong, its owner can delete it. Giving people a way to undo damage is named as a requirement alongside prevention.
- What the alpha taught, with more than 3,000 internal agents and more than 25,000 created by alpha customers: early versions nudged people into permissions that were too broad. Agents with wide write access to Slack posted in the company-wide channel. The fix was a new permission, read and reply, which lets an agent answer only in the threads that triggered it.
- That experience is also why some integrations were built first-party. Most MCP servers are designed for a single user and do not handle resource-based permissions or triggers.

## What to do with it

- Give a shared agent its own identity and an empty permission set, and add access one resource at a time.
- Shape permissions around triggers: replying where it was invoked is a different grant from posting anywhere.
- Route confirmations for risky run-time actions to the agent's owner, and configuration risks to an administrator.
- Ship an undo with every outward action the agent can take.

## Terms

- **Build-from-nothing model** — an agent begins with no access and gains it by explicit grant.
- **Read and reply** — a permission to respond only inside the thread that triggered the agent.

## Caveats

- A short vendor post from February 2026 describing a product in beta. It gives no figures for injection attempts caught or missed.
- Its remarks on MCP reflect the protocol as it stood in early 2026.
