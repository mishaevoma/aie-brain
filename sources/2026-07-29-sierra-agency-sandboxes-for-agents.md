---
type: source
title: "Agency: Secure, scalable sandboxes for agents"
author: "Rohith Ravi"
publisher: Sierra
url: https://sierra.ai/blog/agency-secure-scalable-sandboxes-for-agents
published: 2026-07-29
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms, managed-agent-runtimes]
---

# Agency: Secure, scalable sandboxes for agents

**In one line:** Sierra's agent runners talk to applications only through queues, so an idle runner can be shut down and rebuilt by replaying its ordered output log from the last checkpoint.

## What it says

- **Control plane and runners.** Agency sits under Sierra's internal cloud agent, Pinecone, and its customer-facing agent-building agent, Ghostwriter. A stateless control plane on Kubernetes exposes APIs such as `CreateRunnerInstance`, authenticates callers with IAM, keeps runner state in DynamoDB and turns each runner definition into a pod. Stateful runners are those pods: dedicated compute, usually a Persistent Volume, with a laptop-class target (8+ cores, 24GiB RAM).
- **No secrets in the sandbox.** Agents get no API keys or other secrets by default, since a jailbroken agent could exfiltrate them. An LLM proxy outside the sandbox adds real keys at call time and counts tokens, independent of the agent. A filtering egress proxy limits reachable hosts. The container is hardened (non-root, no capabilities, read-only root filesystem), each runner type has its own IAM roles, pods run on isolated node pools, and every control-plane call carries the pod's identity, against impersonation.
- **Why hibernate.** Unattended agents mostly wait for user input: counts of runner instances active in the last 8 hours and the last 8 days usually differ by 2 to 4 orders of magnitude. Stopping idle runners lets a small node pool give each a large machine.
- **Queues, not connections.** Applications never reach a runner directly. A runner is a finite state machine: the application writes to its input queue and consumes its output queue. With in-memory queues (Elasticache Redis Streams) and events capped at a few hundred KiB, round trips take 8ms at p50 and 40ms at p99 when both sides are online.
- **Resume by replay.** Each runner is a singleton and the only writer to its output queue, so that queue is a strictly ordered, append-only log. It emits checkpoint events periodically and restores itself by replaying the log from the latest one, then returns to the input queue. Checkpoint and delta contents are the application's choice, opaque to the control plane.
- **Why build.** Agent sandboxes were not yet well understood, so a vendor's assumptions would have become product limits: providers often capped resources per sandbox, lifetime and concurrency. Keeping customer data from a third-party vendor also sped approval by strict customers. Owning the stack let "Ephemeral Sessions", the only sessions that may load customer data, ship in under a week.

## What to do with it

- Put queues between an application and its runners, and make each runner the single writer of a checkpointed output log, so it can be stopped and rebuilt by replay.
- Keep model keys in a proxy outside the sandbox and meter tokens there.

## Terms

- **Runner hibernation** — stopping an idle runner (a stateful pod where an agent works) and restoring it on demand.

## Caveats

- Self-reported by Sierra, July 2026. No resume times, fleet sizes, costs or failure rates.
- Durability of the in-memory log is unexplained; the companion [Pinecone](2026-07-15-sierra-pinecone-wisdom-of-the-workforce.md) post says durable events and checkpoints are stored separately.
- No VM-level isolation is mentioned. [Cognition](2026-04-23-cognition-what-we-learned-building-cloud-agents.md) argues containers are unsafe for agents and cannot pause; this design counters only the latter.
