---
type: source
title: "What We’ve Learned Building Proactive Agents"
author: "Sydney Runkle"
publisher: LangChain
url: https://www.langchain.com/blog/what-weve-learned-building-proactive-agents
published: 2026-11-17
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-interfaces, background-agents, human-judgment, knowledge-factory]
---

# What We’ve Learned Building Proactive Agents

**In one line:** Agents that start themselves from events and schedules move the bottleneck to the person's attention, so the work shifts to memory (knowing what matters) and to check-ins that are rare, quick to review and delivered where people already are.

## What it says

- A proactive agent runs in the background toward a goal. It reacts to three kinds of trigger: real-world events (a new email, a pull request opened), schedules set by the developer (a nightly memory update), and schedules the agent sets for itself (follow up tomorrow, a daily brief someone asked for).
- LangChain runs two internally: a sales agent, and an engineering agent called Robin (formerly Open SWE). On its hosted product, more than 70% of runs now start from a schedule and not from a human prompt.
- Each check-in costs attention. With no prompt at wake-up, what the agent knows about the person's wishes comes from memory.
- Memory has three sources tied to time: a seed from existing material (past), feedback on what the agent proposes (present), and outcomes after it acts (future). The maintenance problems are salience, expiry and duplication. Many such agents run "dreaming", a scheduled job that reads recent traces and updates memory.
- Judge memory by outcomes: the time a draft takes to be approved, reply rates, and the share of check-ins the person acts on.
- Three lessons about the interface:
  - High signal. An event arriving is not a reason to act. The post sorts behaviour into useful action, useful silence, noise and missed opportunity. A separate decision model decides when the engineering agent joins a Slack thread.
  - Built for review. Review is how feedback reaches memory, so every item must be fast to judge. A custom review screen replaced a slow backlog in Slack.
  - Where people work. Reports arrive in the thread that started them, with a headline of one or two sentences and the detail in a reply.
- Autonomy is earned: once the person stops changing what the agent proposes for a kind of item, let it act alone on that kind.

## What to do with it

- Support all three trigger types in the platform, including schedules that the agent creates.
- Track the fraction of check-ins that are acted on, and treat a low value as a defect.
- Lead every report with a short headline and an explicit ask.
- Widen autonomy one action type at a time, as corrections stop.

## Terms

- **Proactive agent** — an agent started by events and schedules, working toward a goal, that decides when to involve a person.
- **Check-in** — a question or approval request that the agent sends unprompted.

## Caveats

- Published on the day it was ingested, by a vendor describing its own agents and product. The 70% figure is for that product.
- No figures on error rates or on how often check-ins were unwanted.
