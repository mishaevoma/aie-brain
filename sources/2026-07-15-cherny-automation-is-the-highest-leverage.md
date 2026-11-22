---
type: source
title: "Automation is still the highest-leverage work (untitled post)"
author: "Boris Cherny"
publisher: "@bcherny on X"
url: https://x.com/bcherny/status/2077460395279692197
published: 2026-07-15
ingested: 2026-11-17
kind: x-post
read: full
concepts: [compounding, context-layer, instruction-files, knowledge-factory]
---

# Automation is still the highest-leverage work

**In one line:** When an agent keeps fixing the same kind of problem, have it write the lint rule, CI step or skill that removes the problem for good, and treat every rejected pull request as missing automation.

## What it says

- The best engineers always spent time automating their own work: editor automation, lint rules for repeated mistakes, end-to-end tests instead of manual smoke tests. That mattered because it multiplied their output.
- It matters more with agents, for three reasons:
  - Faster infrastructure and developer tooling speed up every agent you run, not only you.
  - Moving a fix into code is cheaper and more complete. An agent can fix an issue each time it sees it, but that costs tokens and misses cases. A lint rule, CI step or routine removes the whole class. He says this is what people mean by "loops": automating a type of busywork instead of solving instances.
  - Automation lets others contribute. New engineers and non-engineers can ship on day one when the agent can navigate the codebase. What blocks them is domain knowledge that lives in people's heads.
- What can be encoded has widened. It used to be limited to what lint rules, types and tests could express. Now nearly all domain knowledge can be captured in code comments, skills, `CLAUDE.md` rules and memories.
- A pull request rejected for using the wrong framework or ignoring the house architecture is a failure of automation, not of the contributor.
- Every team should write the `CLAUDE.md`, `REVIEW.md`, skills and docs that let an agent work productively with no extra context from the person prompting.

## What to do with it

- When you correct an agent twice for the same thing, stop and encode it: a lint rule or test if it can be checked mechanically, otherwise a rule or skill.
- Prefer deterministic checks over instructions where both are possible. Checks cost no tokens and do not get forgotten.
- Read review comments and rejections as a backlog of missing automation.
- Aim for the zero-context test: could someone unfamiliar with the codebase get a correct change merged by prompting alone?

## Terms

- **Loops** — here, automating an entire category of recurring work, as opposed to handling each occurrence.
- **Domain knowledge as infrastructure** — conventions and context written down where agents and checks can use them.

## Caveats

- A reflective post from the lead of Claude Code, with no data.
- It does not address the opposite risk covered elsewhere in this brain: instruction files and rule sets that grow until they hurt.
