---
type: source
title: "A postmortem of three recent issues"
author: "Sam McAllister"
publisher: Anthropic
url: https://www.anthropic.com/research/a-postmortem-of-three-recent-issues
published: 2025-09-17
ingested: 2026-11-17
kind: article
read: full
concepts: [eval-validity, production-operations]
---

# A postmortem of three recent issues

**In one line:** three unrelated serving-infrastructure bugs degraded Claude's output in August–September 2025, and standard evals missed them because the model often recovers from isolated errors and each bug looked different on each platform.

## What it says

- Claude runs on Anthropic's API, Amazon Bedrock and Google Cloud Vertex AI, across Trainium, NVIDIA GPUs and TPUs, so every change must be validated on all of them. Anthropic states it never lowers quality for load or time of day.
- **Routing error (from Aug 5):** some Sonnet 4 requests went to servers configured for the coming 1M-token context window. About 0.8% of requests at first; an Aug 29 load-balancing change pushed it to 16% in the worst hour (Aug 31). About 30% of Claude Code users had at least one misrouted message, and sticky routing kept them there. Bedrock peaked at 0.18%; Vertex AI stayed under 0.0004%.
- **Output corruption (Aug 25):** a TPU misconfiguration made rare tokens likely, e.g. Thai or Chinese characters in English text or code syntax errors. Opus 4.1 and Opus 4 (Aug 25–28), Sonnet 4 (to Sep 2), first-party API only.
- **Approximate top-k miscompilation (Aug 25):** a sampling rewrite removed a December 2024 workaround and exposed a latent XLA:TPU bug that sometimes dropped the most likely token, depending on batch size and configuration; bf16/fp32 precision mismatch (`xla_allow_excess_precision`) was part of the history. Confirmed on Claude Haiku 3.5, likely some Sonnet 4 and Opus 3. Fixed with exact top-k and more fp32, accepting the speed cost.
- Detection failed: benchmarks, safety evals, spot checks and canaries did not show it; privacy controls limited access to conversations; overlapping symptoms made reports contradictory; the team trusted noisy evals and was slow to tie the Aug 29 spike to the load-balancing change.
- Fixes: more sensitive evals, continuous quality evals on real production systems, deployment tests for unexpected characters, and faster privacy-preserving feedback tooling.

## What to do with it

- Run quality evals continuously against the production serving path, not just the model pre-release.
- Make evals sensitive enough to tell a correct inference stack from a subtly broken one.
- Correlate complaint spikes with recent infrastructure changes, and add cheap output sanity checks to deploy gates.
- Test approximate kernels against exact ones across batch sizes and hardware.
- Re-check tuned top-p after a provider changes sampling internals; the post says the fix may shift tokens near the threshold.

## Terms

- **approximate top-k** — a faster top-k meant to be inexact only for unlikely tokens.

## Caveats

- September 2025; models and infrastructure are of that period. Self-reported by the vendor.
- The page dates the sampling change Aug 25 in its summary and Aug 26 in the compiler deep dive.
- The April 2026 postmortem (2026-04-23) covers a different layer, the product harness; the two complement each other.
