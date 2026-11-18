---
type: source
title: "What We Learned Building Cloud Agents"
author: "The Cognition Team"
publisher: Cognition
url: https://cognition.com/blog/what-we-learned-building-cloud-agents
published: 2026-04-23
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, long-running-agents, managed-agent-runtimes]
---

# What We Learned Building Cloud Agents

**In one line:** Cognition's case against containerised agents: they share a kernel and cannot pause; Devin snapshots the whole machine at the hypervisor and shuts compute down while waiting on CI or review.

## What it says

- **Shared kernel.** Containers run on one shared kernel, so a compromised session can get at the files, credentials and network connections of every other container. Agents write and run arbitrary code and probe their surroundings, which makes a kernel escape a realistic threat. The post's answer is VM-level isolation, which it calls the industry consensus for untrusted code. Cognition's microVMs, one kernel per session, took over a year of hypervisor work, and also let agents use a full browser and desktop applications.
- **Async gaps.** Between opening a PR, waiting on CI and answering review lie minutes, hours or days. The root complaint: a single container's whole state cannot be reliably snapshotted, switched off and brought back. A containerised agent gets through a wait only by keeping compute running, and a reschedule, timeout or crash ends the session. A single-pass agent is enough for bounded jobs such as dependency upgrades.
- **Snapshot design.** The whole machine is snapshotted by the hypervisor: memory, process trees and filesystem. While the agent is idle its compute is off; a CI result or a review comment wakes the session, which continues from where it stopped. Getting this reliable across thousands of concurrent sessions took longer than any other infrastructure Cognition has built.
- **Orchestration.** Each session needs the right environment, routing and a warm VM pool sized by predicted demand. Cognition's version occupied dedicated engineers for over three quarters and manages thousands of concurrent VMs, including crash recovery.
- **Permissions and audit.** A session should carry the permissions of the engineer who dispatched it into every system it reaches, and each action should land in a tamper-evident audit trail. The post treats identity chaining, access scoping and audit logging as a project in itself, with continuing maintenance.
- **Scope.** Orchestration, governance and integrations are each called a multi-quarter project, and their combined, permanent upkeep is what defeats in-house teams. Stripe's internal MCP server with over 400 tools is cited for integrations. Cognition, over two years in, staffs a team per layer.
- **Adoption.** For Itaú (nearly 17,000 engineers, eleven months of use) it claims migrations 5 to 6x faster, 70% of static-analysis security vulnerabilities auto-remediated and 2x test coverage.

## What to do with it

- Decide early whether agents must wait across CI and review, and how state survives with compute off.
- Treat a shared kernel as a threat when agents run arbitrary code.
- Budget orchestration, governance and integrations as standing projects before choosing to build.

## Terms

- **Async gaps** — waits between steps of engineering work that an agent's state must survive.

## Caveats

- A vendor's build-versus-buy argument: Cognition sells Devin. Durations are self-reported, the one failed in-house attempt it cites is anonymous, and the Itaú figures come without method.
- No snapshot or resume times, costs or failure rates.
- This brain's reading: [Agency](2026-07-29-sierra-agency-sandboxes-for-agents.md) hibernates container-based runners by replaying a log, which contradicts the claim that containerised agents cannot pause. A hypervisor snapshot also keeps live memory and processes.
