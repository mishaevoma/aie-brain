---
type: source
title: "Solving the Identity Crisis for AI Agents"
author: "Matt Mathew, Prasad Borole, Meng Huang, Sergey Burykin, Gaurav Goel, Bayard Walsh"
publisher: Uber Engineering
url: https://www.uber.com/us/en/blog/solving-the-agent-identity-crisis/
published: 2026-05-21
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, mcp]
---

# Solving the Identity Crisis for AI Agents

**In one line:** Uber's agents exchange a fresh, minutes-long, single-destination token at every hop, carrying the whole chain of user and agents, so downstream systems can authorise and audit against whoever started the work.

## What it says

- **The gap.** An on-call engineer asks an agent to handle an alert; it delegates to a second agent and that to a third, which opens a pull request showing only itself. Each hop presented a generic service identity: identity models covered humans and workloads, not delegates, and the originating user and intermediate agents were dropped. Audits were incomplete, and downstream systems could not apply the fine-grained policies they already had.
- **Minting.** Only a central Security Token Service (STS) mints agent tokens. The agent SDK authenticates with the workload's SVID from SPIRE and sends local agent metadata, the inbound JWT and the next destination's audience. The STS checks an Agent Registry that this `agent_id` may run on that workload, so a workload cannot impersonate an agent it does not host.
- **Token.** Each JWT serves a single hop: one Audience claim and a time-to-live on the order of minutes, so it cannot be replayed against another service. It embeds the attested actor chain, for example user1, oncall-agent, investigation-agent. Agents cannot reuse the user's raw credentials.
- **Standard.** The exchange follows the idea of OAuth 2.0 Token Exchange (RFC 8693), customised to carry agent identity and provenance. Uber is tracking the IETF WIMSE working group drafts and draft-klrc-aiagent-auth-01.
- **Downstream use.** The receiving agent verifies signature and audience. An MCP Gateway, which mediates agent calls to Uber's systems, verifies the JWT and enforces tool-level policies (access checks, redaction of sensitive data), mandatory for high-risk systems. Policies can evaluate the human initiator and the acting agent together, and each hop is traced with its authorisation decision.
- **Decided against.** A proxy between agents (agentgateway). The logic went into the agent SDK, because Uber's agents had standardised on it and because provenance needs support in the application layer, which is where execution context originates. A standard A2A client now performs the exchange; older agents are being migrated.
- **Figures.** Thousands of internal agents have adopted it, and thousands of services are exposed over MCP. P99 latency of the token exchange call stays under 40 milliseconds, mostly under 10 ms, on a graph for March 30 to April 2.

## What to do with it

- Treat an agent as a delegate: carry the initiating user and every intermediate agent in each credential.
- Mint tokens centrally, bound to the hosting workload, one audience and a few minutes.
- Put the exchange in the SDK developers already use, so the secure path is the default.

## Terms

- **Actor chain** — the ordered record of the user and agents behind a request, embedded in each token.
- **STS** — Security Token Service, the only minter of agent tokens.

## Caveats

- Self-reported by Uber, May 2026, about 2025 work in its internal environment; the post warns that results may differ elsewhere.
- The latency figure covers one token exchange, not the end-to-end overhead of a multi-hop task.
- It covers the identity layer only; dynamic access control and a unified policy enforcement plane are presented as direction.
