---
type: source
title: "Opening the door to agent autonomy: The architecture behind Rovo’s agent harness"
author: "Dylan Hwang, Muhammed Sit, Alexander Sumer, Alex Chen, Shubham Goel, Steven Yoo"
publisher: Atlassian
url: https://www.atlassian.com/blog/rovo/agent-autonomy
published: 2026-08-26
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms, multi-agent-systems]
---

# Opening the door to agent autonomy: The architecture behind Rovo’s agent harness

**In one line:** Atlassian runs Rovo's agent in a control plane and treats the sandbox as a replaceable place to execute code, without direct external network access, so a sandbox crash costs a retry and every tool call from code passes a permission check.

## What it says

- **Split plane.** Rovo Chat's new harness runs the agent in a control plane, to which the user connects, and executes code in a separate data plane of sandboxes. One scaled service handles events for millions of users, and an agent can respond without a sandbox.
- **The rejected alternative** was a monolith with the harness inside the sandbox. It was dropped over resilience: if the sandbox crashed, the user would see the whole agent crash, and storing the conversation and recovering quickly became open questions. With the split, the agent retries transparently on a new container.
- **A sandbox starts only when needed.** For light informational questions the control plane calls tools directly and statelessly. The agent picks the stateful sandbox for deep data analysis, where code does the iteration and pagination.
- In Atlassian's internal evaluations on a representative set of complex Jira-related queries, code mode beat a baseline harness with standard meta-tools: latency down by over 50%, token use down 55%, accuracy up 30%.
- Tools ship as a versioned Python package refreshed on warm start (start-up under 100ms), with a run-time manifest of the APIs enabled for the user.
- **Callback bridge.** A tool call from sandbox code, to a native tool or a remote MCP server, is routed back through the control plane and an internal server, which validates the user's permissions and authenticates the request before any external API is called. The sandbox needs no direct external network access.
- **Sub-agents**, once single-use and synchronous, are now each a hidden Rovo Chat conversation with a durable handle, asynchronous execution, its own history and optional access to the shared sandbox. Each can outlive the parent's turn, be polled or sent follow-ups, and wake the parent through a dedicated notification loop on completion.
- **Checkpoints** snapshot execution state at milestones. A script that fails at step 10 of 11 is rolled back and retried without repeating finished steps, which would create duplicates or "Entity Already Exists" errors.

## What to do with it

- Keep the loop and the conversation outside the sandbox, and start a sandbox only for work that needs code.
- Deny the sandbox external network access and route its tool calls through a service that checks the user's permissions.
- Model a background sub-agent as a durable conversation with a handle and a wake-up path to its parent.
- Checkpoint scripts whose steps create things.

## Terms

- **Code mode** — the model writes code that calls tools; the post also says "programmatic tool calling".
- **Callback bridge** — the return path for tool calls made by sandbox code.

## Caveats

- The vendor's own account, August 2026. The three percentages come from unpublished internal evaluations: no models, sample size or absolute values.
- Nothing on where conversations are stored, how the sandbox is isolated, how checkpoints work or how often sandboxes fail. Its diagrams were not read.
