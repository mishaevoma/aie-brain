---
type: source
title: "Critical thinking when agents do the work"
author: "Addy Osmani"
publisher: "@addyosmani on X"
url: https://x.com/addyosmani/status/2117512471930167377
published: 2026-11-03
ingested: 2026-11-17
kind: x-article
read: full
concepts: [compounding, context-engineering, human-judgment, multi-agent-systems, verification]
---

# Critical thinking when agents do the work

**In one line:** Agents remove the friction that used to force you to think, so you have to build the thinking back in on purpose, mainly by forming a view before you ask and by checking evidence instead of summaries.

## What it says

- Agent output is now mostly correct and always well written, so it no longer invites a second look. You can run many agents, but you still have one pair of eyes.
- There is a spectrum of handing work over. **Cognitive offloading**: you delegate the task and keep ownership of the result. **Deferral**: the output becomes your input without being treated as a hypothesis. **Cognitive surrender** (a term from Steven Shaw and Gideon Nave at Wharton): the output becomes your position and you feel no need to check it. People slide down the spectrum in small, reasonable-looking steps.
- The cost shows up later as cognitive debt, or comprehension debt in code: everything looks clean and tests pass, until someone has to change the system and nobody understands it.
- You do not need the whole system in your head. The Claude Code team rebuilds understanding of a slice on demand by asking the agent to explain it. The test of ownership is whether you can explain the answer, even with the agent's help.
- Delegate fully where being wrong is cheap. Keep the reasoning where other people carry the consequences: what to build, who a change affects, whether it is safe to ship.
- A green check proves one property. Agents make tests cheap, so there is a lot of green, and a test written with the same misunderstanding as the feature passes.
- Review turns into rubber-stamping when you only look for what you already expected. The agent also makes many silent decisions over a long session: defaults, scope, how it resolved conflicting requirements.
- **Orchestration tax**: the gap between what your agents produce and what you would put your name on. If finished work piles up faster than you can check it, another session does not help.
- **Intent debt**: goals and constraints you never stated. An agent will not push back on a vague request. It fills the gaps and returns something that looks finished.
- Polish is no longer a signal of quality. Accountability for what ships stays with a person, and supervising agents needs the same skills that fade when you stop using them (Anthropic's "paradox of supervision").

## What to do with it

- Before a non-trivial task, write down what you expect the answer to be. If you have no idea, ask the model for a blind-spot pass: give it what you know and ask what you are missing.
- Define "verified" before the work starts. Make the finish line something tangible: a passing test, a screenshot, a log or trace. Read the command and its output before the summary.
- When a check goes green, ask what it proved and what it did not. If you cannot say what the checks would miss, ask for a real review.
- Ask the agent to list the decisions and assumptions it made. Then quiz yourself on the change; some people merge only after passing a quiz the agent wrote.
- Build a fresh-context self-critique step into the loop so it runs every time, and still ask "did I miss anything?" at the end.
- Write the brief yourself: audience, what is out of scope, definition of done. After two rounds of corrections, rewrite the prompt instead of patching it. Do not let agents work from summaries of summaries.
- When something misses your bar, record why in shared config, a hook or a test so the lesson sticks.
- Once a week do one real task without an agent. Once a month list what you have stopped doing and decide which of those you accept losing.

## Terms

- **Cognitive surrender** — adopting the agent's output as your own view without checking it.
- **Comprehension debt / cognitive debt** — the growing gap between what the system does and what its owners understand.
- **Intent debt** — unstated goals, constraints and rationale that only the requester can supply.
- **Orchestration tax** — output produced by agents minus output you can actually stand behind.
- **Blind-spot pass** — asking a model to find your unknown unknowns before you commit to an approach (credited to Thariq Shihipar).

## Caveats

- An opinion essay, not a study. The author works on Claude Code at Anthropic.
- The habits are personal practice and scale with stakes; the article itself says not to apply all of them everywhere.
- Companion piece on the mechanics of verification: the author's 17 Nov 2026 article on how the Claude Code team verifies work.
