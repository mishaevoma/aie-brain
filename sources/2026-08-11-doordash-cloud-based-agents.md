---
type: source
title: "Delegating Engineering Work To Cloud-Based Agents"
author: "Santosh Banda, Jeffrey Hwang, Siddarth Kodwani"
publisher: DoorDash
url: https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/
published: 2026-08-11
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms, agents-and-workflows, background-agents, managed-agent-runtimes, mcp]
---

# Delegating Engineering Work To Cloud-Based Agents

**In one line:** DoorDash's internal agent platform is four reusable primitives (a sandbox, a tool gateway, a declarative playbook and several ways to invoke it), built in-house so that neither its code nor a path into its systems goes to a third party.

## What it says

- Flux is DoorDash's cloud agent platform for engineers, launched in the first quarter of 2026. In one month it completed 130,000 engineering tasks. Each week it runs more than 25,000 automated code reviews and more than 10,000 invocations of over 300 distinct playbooks.
- Three limits of agents on laptops drove it: fixed resources and availability (work stops when the lid closes), broad credentials with a large blast radius, and fragmented execution that nobody can monitor or audit.
- Why in-house: a hosted coding agent forces a choice between sending sensitive code and context to a third party and opening a path from that third party into internal systems. The hard part was not getting an agent to write code. It was giving the agent the right environment, tools, permissions and constraints. The primitives are kept modular so that a third-party part can be swapped in where that is better.
- The four primitives:
  - **Sandboxes.** Isolated cloud sandboxes on Firecracker microVMs, each provisioned with the repositories, tools, secrets and dependencies the task needs. One session can change several repositories and open several pull requests. The service-level objective for full setup (start the microVM, clone, install build tools, configure the agent harness) is under five seconds at the 95th percentile.
  - **MCP gateway.** Agents reach internal systems only through an in-house gateway. A playbook declares the tools it needs and gets permissions scoped to that task. Every action is logged. The gateway is the single point for authentication, authorization, usage tracking and policy.
  - **Playbooks.** A reusable unit of agent work in one YAML file: task, inputs, context, skills, tools, permissions, validation, expected outputs and safety boundaries. A playbook mixes agentic steps with deterministic ones, and logic can move between the two as requirements change.
  - **Invocation surfaces.** The same playbook runs from Slack, GitHub, cron, the command line or a skill.
- Lessons about adoption:
  - Start narrow to earn trust. Code review came first because it is frequent, measurable and easy for engineers to judge, and it let the team tune quality, latency and cost before expanding.
  - Make the work visible. The first Slack integration gave each run a private channel, which helped individuals and built no team habit. Moving runs into public threads changed adoption.
  - Reusable workflows do not appear on their own. Workshops and hackathons were needed to turn repeated work into playbooks.

## What to do with it

- Build primitives that compose, and let teams define workflows on them, instead of building one workflow at a time.
- Declare the tools and permissions a task needs in the task definition, and grant only those for that run.
- Send every agent tool call through one gateway that logs it.
- Launch with one frequent, measurable workflow, and run it where the team can watch.

## Terms

- **Playbook** — a declarative, reusable definition of a unit of agent work, including its tools, permissions and validation.
- **Invocation surface** — a place from which a playbook can be started, such as chat, the code host, a schedule or the command line.

## Caveats

- Self-reported in August 2026, in a post on the company's careers site. The counts are tasks and invocations, with no success rate, cost or review burden.
- It names the four primitives and defers their internals to later posts. Session state and recovery after a failure are not described.
