---
type: source
title: "Agents are sessions, not requests: size GKE node pools for AI agent sessions"
author: "Drake Williams, Ivan Nardini"
publisher: "Google Developers Blog"
url: https://developers.googleblog.com/en/agents-are-sessions-not-requests-size-gke-node-pools-for-ai-agent-sessions/
published: 2026-11-16
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, production-operations]
---

# Agents are sessions, not requests: size GKE node pools for AI agent sessions

**In one line:** A coding-agent session mostly waits for its user, so park the idle sandbox in object storage and free its machine: nearly 40% off the node bill at 2 prompts an hour in Google's cost model, nothing above about 4.

## What it says

- **Evidence.** A July 2026 trace study (Banruo Liu and colleagues) has agents waiting on the user about 80% of a typical multi-prompt session; a turn averages about 6.5 minutes of agent work. The authors assume 2 prompts an hour across an 8 hour workday: 22% of it is work.
- **Baseline.** One Pod per session holds 1 vCPU and 1 GiB all day. A `c3-standard-4` node fits 3, so 100 coding agents need 34 nodes, about USD 1,288 a month (on-demand list prices, `us-central1`). Scale-to-zero frees nodes but loses the process and its memory.
- **Parking.** In Agent Substrate (1.0, generally available on GKE) `SuspendActor` writes an idle actor, one agent's sandbox, to object storage and releases its worker, a reusable sandbox from a warm pool of Pods. A later request restores the actor on a warm worker. Memory is snapshotted by default, files as the fallback.
- **Who suspends.** Not the platform: the harness or a fronting service must call the suspend API after an idle timeout. If idle actors occupy every worker, a request needing another actor is held up to 5 seconds by default, then gets HTTP 503.
- **Parked cost.** With a 2 minute idle timeout a session occupies a worker nearly 29% of its open time. The 99th percentile of simultaneous holders plus 15% headroom is 15 nodes, plus one always-on control-plane node: 16 against 34, nearly 40% off the node bill, with the pool full about once in 3,000 turns.
- **Sensitivity.** At 2.5 prompts an hour that pool is full for 3% of turns. At 4, agents work 44% of each hour, the pool is 27 nodes and the saving 4%; above about 4, one Pod per session is cheaper. Its fixed control plane means parking pays only from about 37 coding sessions. Run all 730 hours of a month, the pool costs nearly twice the baseline: scale it to zero after hours.
- **Overcommit.** Pods requesting 0.25 vCPU under a 1 vCPU limit pack 12 to a node: 9 nodes for the 100 agents, fewer than parking, but with contended CPU.

## What to do with it

- Measure prompts per hour from gateway logs; parking stops paying near 4.
- Size the warm pool for sessions holding a worker in the busiest hour, not open sessions.
- Put the idle-timeout suspend call in the harness, handle the 503, and compare designs at equal CPU guarantees.

## Terms

- **Parking** — snapshotting an idle sandbox and freeing its machine while the session stays open.

## Caveats

- By Google staff promoting GKE, Agent Substrate and AX; beyond the study, the figures come from their cost model, not a measured fleet.
- The authors call the prompt rate their least certain input; 2 prompts an hour is an assumption, and pool sizing assumes independent sessions.
- The parked pool's monthly bill is only in a table image, not read here.
