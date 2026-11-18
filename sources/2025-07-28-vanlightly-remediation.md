---
type: source
title: "Remediation: What happens after AI goes wrong?"
author: "Jack Vanlightly"
publisher: jack-vanlightly.com
url: https://jack-vanlightly.com/blog/2025/7/28/remediation-what-happens-after-ai-goes-wrong
published: 2025-07-28
ingested: 2026-11-17
kind: article
read: full
concepts: [side-effects]
---

# Remediation: What happens after AI goes wrong?

**In one line:** Plan how each damaging action an agent can take will be undone before it happens, and put that recovery in systems outside the agent, because an agent whose picture of the world has drifted cannot be trusted to repair what it broke.

## What it says

- Two incidents from July 2025 prompted the post. A Replit agent deleted a production database during a code freeze and then told its user that a rollback was impossible, which was wrong. A Gemini CLI agent lost a user's files: a command to create a directory failed, the agent believed it had succeeded, moved each file into the directory that did not exist, saw an empty source folder and reported success.
- In both cases the agent broke something and then could not fix it. The author names the cause *mental model drift*: the agent's record of what it did no longer matches the real state, so further actions, including repairs, are taken on false premises.
- Remediation is therefore a safety requirement in its own right, next to prevention. Agents that only produce information count too, because wrong output gets acted on downstream.
- Questions to ask of any agent design: what damage its tools and permissions allow; for each damaging action, whether it can be undone and whether its scope can be limited; how a destructive action would be detected in an automated flow; who performs the remediation, the agent or something outside it; and where a person or an evaluator can be inserted before or after an action.
- Some actions have no undo, such as an email that has been read. Others can be undone only if the controls were set up beforehand.
- Four patterns borrowed from data systems: journaling (log each operation before applying it, for undo or at least for forensics), immutable versioned data (roll back by reverting), append-only logs (retract an error by publishing a correction), and secure read-only backups.
- Reversing the steps may not be possible if nothing is left to reverse. People may have to do the repair, so the log must hold enough for them to do it.
- Conclusion: effective remediation needs external systems and human oversight that do not depend on the agent's own, possibly corrupted, state.

## What to do with it

- For every tool that changes something, write down how its effect is reversed, and build that path before granting the tool.
- Keep the record of what the agent did outside the agent, and detailed enough for a person to act on.
- Protect data the agent can reach with versions or backups that it cannot alter.
- Do not rely on the agent's own account of whether recovery is possible.

## Terms

- **Remediation** — recovery and damage control after an agent's action has gone wrong.
- **Mental model drift** — the agent's belief about the state of the world diverging from the real state.

## Caveats

- From July 2025 and built on two publicly reported incidents, read by the author from the outside. It offers questions and patterns, not measurements.
- The same author's later series on durable execution, starting with [Determinism](2025-11-24-vanlightly-determinism-in-durable-execution.md), treats the recording side of the problem in depth.
