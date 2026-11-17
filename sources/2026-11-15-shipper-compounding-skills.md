---
type: source
title: "Turn your daily newsletter edits into AI checks, and watch every frontier model jump 25+ points"
author: "Dan Shipper"
publisher: "Every Frontier"
url: https://frontier.every.to/experiments/turn-your-daily-newsletter-edits-into-ai-checks-and-watch-every-frontier-model-jump-25-points
via: https://x.com/danshipper/status/2122091033001337134
published: 2026-11-15
ingested: 2026-11-17
kind: article
read: full
concepts: [compounding, evals, skills]
---

# Turn your daily newsletter edits into AI checks

**In one line:** A skill gets better with use when you save the corrections you make, turn them into yes/no checks, and iterate the skill against those checks until models pass on the first try.

## What it says

- The announcing post calls these **compounding skills**: skills that improve each time they are used. It credits Mike Taylor (@hammer_mt) with working out the method.
- The problem: getting models to summarise articles in Every's house voice meant typing the same edits into chat for every issue.
- The method:
  1. Save real drafts together with the editor's changes and reactions. The version that was actually published is the **gold case**.
  2. Turn each piece of feedback into a binary check, for example "does the opening say what is being corrected and why the reader should care?" or "does it avoid unexplained agent jargon?". Eight real cases produced 74 checks.
  3. Write the instructions as a reusable skill (`short-idea-summary`).
  4. Run an optimisation loop over the skill, version 1 to version 9. Each version ran in isolated sandboxes with no other context, on four models. A model graded the outputs blind against the checks.
- Results. Version 1, on the first seven cases, scored 34% to 56% depending on the model. Version 9, on all 74 checks, scored 75.7% to 81.1% (56 to 60 checks passed) across Gemini 4 Hydrogen, Claude Opus 5.5, GPT-6 Astra and Claude Sonnet 5.5.
- The post describes the outcome as reaching about 80% of his taste compared with a baseline that had no skill.

## What to do with it

- Keep your corrections. Each edit you make to agent output is a test case you would otherwise throw away.
- Express taste as many small yes/no checks, not one overall score.
- Optimise the skill, not the prompt of the day, and test it in a clean context so it cannot lean on conversation history.
- Check the result on more than one model. A skill that only works on one is fragile.

## Terms

- **Compounding skill** — a skill with a feedback loop attached, so each use can make it better.
- **Gold case** — an example of output you would actually ship, used as the reference.
- **Binary check** — a yes/no question about an output that a model can grade.

## Caveats

- The page shows no publication date beyond "Week 46"; the date above is that of the announcing post.
- Version 1 and version 9 were scored on different sets (seven cases versus all 74 checks), so the gain is not a like-for-like comparison. The grader was one of the models being tested.
- One writing task at one company. Every sells subscriptions to this kind of write-up.
