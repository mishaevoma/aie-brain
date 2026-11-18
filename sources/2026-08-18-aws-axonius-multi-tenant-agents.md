---
type: source
title: "How Axonius built secure multi-tenant AI agents on Bedrock AgentCore"
author: "Amir Krispin, Dori Shmuel, Omar Sawara, Yossi Lagstein, Yaakov Tayeb"
publisher: AWS Artificial Intelligence Blog
url: https://aws.amazon.com/blogs/machine-learning/how-axonius-built-secure-multi-tenant-ai-agents-on-bedrock-agentcore/
published: 2026-08-18
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, managed-agent-runtimes]
---

# How Axonius built secure multi-tenant AI agents on Bedrock AgentCore

**In one line:** Axonius gives every customer its own agent runtime, so tenant isolation is enforced by IAM and network placement instead of agent code, and pays in per-tenant provisioning, an account quota and many runtimes to operate.

## What it says

- Axonius, which already runs each customer in a dedicated VPC on AWS, weighed three tenancy models for its first agent on Amazon Bedrock AgentCore. Each gives every user session its own microVM.
- **Pool.** One shared runtime. Each tenant's JWT carries a tenant claim, which agent code reads to pick the tenant environment for tools and data. Onboarding is immediate, but separation rests wholly on application code.
- **Bridge.** A shared runtime whose tool calls pass through an AgentCore Gateway. A Lambda interceptor swaps the JWT for tenant-scoped, short-lived IAM credentials (STS AssumeRole), and Cedar rules allow or deny each call. A routing bug in agent code no longer crosses tenants, but setup is far more complex.
- **Silo.** A dedicated runtime per tenant. IAM resource-based policies on the runtime and its endpoint are the only enforcement point, with no routing logic in the application.
- Axonius chose silo, matching its existing tenant model for sensitive data. Costs listed: a default quota of 1,000 agents per AWS account (adjustable), onboarding delay while a runtime and endpoint are created, and hundreds of runtimes to operate, provisioned and torn down through CloudFormation.
- **Credentials.** The agent holds no long-lived credentials. Per chat message, the Axonius application issues a short-lived impersonation JWT (user, tenant, session and actor IDs), sent in a custom header so it stays out of the agent's saved state. The runtime validates it against the customer's own Axonius instance before the model runs, and tools reuse it, so the agent sees only what that user may see.
- **Network and data.** Each runtime gets a dedicated ENI inside the customer's VPC, so one customer's agent cannot reach another's data over the network. Tenant-specific data in the Bedrock Knowledge Base is separated by metadata filtering.
- **Spend.** CloudWatch tracks input plus output tokens per agent, and IAM role tagging attributes Bedrock cost to a tenant. When a customer exceeds its token budget, a CloudWatch alarm triggers an automated IAM deny policy that blocks further invocations. Cost attribution refreshes once or twice a day; alarms are real time.

## What to do with it

- Decide first where tenant isolation is enforced: agent code, a gateway, or cloud access control.
- With a shared runtime, exchange the user's token for tenant-scoped credentials outside agent code.
- Keep tokens out of the agent's persisted state, and validate them before the model runs.
- Back the budget alarm with a hard stop, and check account quotas before adopting a runtime per tenant.

## Terms

- **Silo, pool, bridge** — dedicated resources per tenant, shared resources, and a mix of the two.

## Caveats

- Co-written by AWS and Axonius staff on an AWS blog; it reads as a case for AgentCore. Only the silo design is reported as deployed, without cost or incident data.
- It does not say whether the knowledge base is shared across customers, or what a user sees once the deny policy applies.
