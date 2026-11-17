---
type: source
title: "Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet"
author: "Erik Schluntz"
publisher: Anthropic
url: https://www.anthropic.com/research/swe-bench-sonnet
published: 2025-01-06
ingested: 2026-11-17
kind: article
read: full
concepts: [agents-and-workflows, eval-validity, harness, tool-design, verification]
---

# Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

**In one line:** a minimal scaffold (short prompt, a Bash tool, a string-replace edit tool) got the upgraded Claude 3.5 Sonnet a state-of-the-art SWE-bench Verified score, and most of the design effort went into the tool interfaces.

## What it says

- SWE-bench gives the agent a Python environment and a repo checkout from just before a real GitHub issue was fixed, then grades with the unit tests from the fixing PR. SWE-bench Verified is a 500-problem, human-checked subset.
- The score belongs to the whole agent (model plus scaffolding); the same model can score very differently under different scaffolds.
- With this scaffold: Claude 3.5 Sonnet (new) 49%, previous state of the art 45%, Claude 3.5 Sonnet (old) 33%, Claude 3 Opus 22%.
- The model gets maximum control; the loop runs until it stops or exceeds its 200k context. The prompt only sketches a workflow: explore, write a reproduction script, edit, rerun, consider edge cases.
- Edit tool `str_replace_editor` offers `view`, `create`, `str_replace`, `insert`, `undo_edit`. An edit applies only if `old_str` matches exactly once; otherwise the model gets an error and retries. This proved the most reliable way to edit.
- Paths must be absolute, because the model lost track of relative paths after changing directory. Tool descriptions were tested for misreadings and revised.
- The newer model self-corrects more and tries new approaches instead of repeating mistakes.
- Challenges: successful runs often took hundreds of turns and over 100k tokens; some failures were environment or grading glitches; hidden tests let the model believe a band-aid fix worked; it could not view images, hurting Matplotlib tasks.

## What to do with it

- Start agents with a thin scaffold and general tools before adding orchestration.
- Design model-facing tools as carefully as a human UI, and test descriptions for misreadings.
- Make tools fail loudly and recoverably, and remove footguns such as relative paths.
- Name the scaffold whenever you report a benchmark score.

## Terms

- **scaffolding** — code around the model that builds prompts, parses output and runs the loop.

## Caveats

- January 2025, Claude 3.5 Sonnet; scores long superseded. A later note reports frontier models above 80% and near saturation (2026-01-09 demystifying evals).
- Anthropic sells the model benchmarked. No byline; acknowledgements credit Erik Schluntz with the agent and the post.
- Sandbox resources are not reported; a later note shows they can shift agentic coding scores (2026-02-05 infrastructure noise).
