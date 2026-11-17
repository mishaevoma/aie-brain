---
type: source
title: "Building strong safety evaluations"
author: "Ruth Appel, Evan Frondorf, Jeremy Hadfield, Rebecca Hiscott, Kamya Jagadish, Shayne Longpre, Madeleine Tucker, Brett Wittmershaus"
publisher: Anthropic
url: https://www.anthropic.com/research/building-strong-safety-evaluations
published: 2026-11-13
ingested: 2026-11-17
kind: article
read: full
concepts: [eval-validity, evals]
---

# Building strong safety evaluations

**In one line:** safety evals should measure the right construct (appropriate responses, not refusal rates), use realistic multi-turn scenarios, validated graders and preregistered statistics, and report configuration and uncertainty in full.

## What it says

- A safety eval measures how likely a model is to cause or contribute to harm, and how severely, not what it can do. Evals are easy to game and hard to reproduce; format changes (multiple choice vs open-ended, option order) move results. The authors borrow from psychology's replication reforms.
- **Team and safety:** pair methods experts with domain experts (e.g. psychologists, biologists) from the start. Evals often run with safeguards off, so cyber evals need offline sandboxes and live monitoring; after its own incidents Anthropic paused many internet-enabled evals.
- **Construct validity:** a model that refuses everything wins on refusal rate but is not safer. For suicide and self-harm, Anthropic scores an "appropriate response rate" against expert rubrics over multi-turn conversations, where one bad turn fails the conversation. In dual-use areas, the goal is to help with the legitimate version while withholding operational uplift, and to measure over-refusal as well as harmful compliance.
- **Multi-turn simulation:** single-turn prompts saturate and miss gradual escalation. An expert writes a scenario spec (goals, tactics, persona, tone); the first turn is fixed; a separate Claude model plays the user; each scenario runs many times with varied specs; a grader applies the rubric. Example: a romance-scam scenario drifting from dating help to targeting wealthy matches. Build scenarios from real usage, red-team transcripts and incidents, across languages, surfaces and tools. Anthropic's single-turn suites span 16 policy areas in seven languages.
- **Internal validity:** use post-cutoff or synthetic data, close shortcuts, randomise irrelevant details. Single-turn harmless response rates are 94%–98% for recent API models, so they are mainly regression checks; raise difficulty in ways that keep the construct.
- **Graders:** alert on failures and drift; route uncertain cases to humans; use atomic binary criteria with explicit borderline rules; say disclaimers do not neutralise harm; grade with a different model from the one tested; check length and position bias; fail loudly on broken items; validate with Cohen's kappa or similar, aiming for grader–expert agreement near expert–expert agreement.
- **Statistics:** preregister metrics, slices and thresholds; run each case several times; floors of 100 items for complex multi-turn evals and 1,000 for simple single-turn ones; use paired comparisons with confidence intervals. Report per category, correct for multiple comparisons, and show uncertainty: multi-turn API intervals can exceed ±10 points, and Claude Opus 5 vs Opus 5.5 at 98% vs 94% on a claude.ai romance-scam eval was not significant.
- **Configuration:** API and claude.ai (with system prompt) results differed by up to 34 points for Claude Fable 5.1. Record model version, sampling, prompts, grader version and dates; never compare across graders. Tools named: UK AISI's Inspect and Anthropic's Petri, built on Inspect.
- **Disclosure:** transcript review found Claude Fable 5.1 sometimes implicitly validated self-harm as coping; a system prompt fix gave 94% on claude.ai versus 60% on the API.

## What to do with it

- Define the construct before collecting data, validate the grader against humans, and report uncertainty: the authors' three starting steps.
- Score appropriate responses and over-refusal together; drop raw refusal rate as a headline metric.
- Use simulated-user multi-turn scenarios for risks that build over a conversation.
- Report results separately for raw model and product configuration.

## Terms

- **appropriate response rate** — share of conversations judged acceptable at every turn against an expert rubric.
- **construct validity** — whether the eval measures the property it claims to.

## Caveats

- Published November 2026, days before ingestion; model names (Opus 5, Opus 5.5, Fable 5.1) are current only for now.
- The 60% vs 94% figures compare API and claude.ai configurations, not the same setup before and after the fix.
- Written by the model vendor about its own evaluation practice; Petri is its own tool.
- Builds on, and is narrower than, the capability-eval guide (2026-01-09).
