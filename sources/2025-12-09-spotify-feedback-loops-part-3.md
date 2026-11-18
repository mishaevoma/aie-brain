---
type: source
title: "Background Coding Agents: Predictable Results Through Strong Feedback Loops (Honk, Part 3)"
author: "Max Charas, Marc Bruggmann"
publisher: Spotify Engineering
url: https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3
published: 2025-12-09
ingested: 2026-11-17
kind: article
read: full
concepts: [background-agents, verification]
---

# Background Coding Agents: Predictable Results Through Strong Feedback Loops (Honk, Part 3)

**In one line:** An unattended agent becomes predictable when verification is a tool it must pass before it may open a pull request, and when pushing, messaging and prompt-writing happen outside it.

## What it says

- Three failure modes, in rising order of harm: no pull request is produced; a pull request fails CI; a pull request passes CI and is wrong. The last one erodes trust and is hard to spot across thousands of repositories.
- **Verifiers.** Independent checks (format, build, test) that switch on according to what the repository contains, for example a Maven verifier when a `pom.xml` is present. The agent sees a single MCP tool for verification and does not know what runs behind it.
- Verifiers also shrink output. They extract the relevant error lines on failure and return a very short message on success, which protects the context window.
- All relevant verifiers run again automatically before a pull request may be opened, through Claude Code's stop hook. If one fails, no pull request is opened.
- **Judge.** After the deterministic checks, a model compares the diff with the original prompt, to catch changes outside the task such as refactoring or disabling flaky tests. Across thousands of sessions it vetoes about a quarter, and after a veto the agent corrects course about half the time. There are no evals for the judge yet.
- **A narrow agent.** It sees the codebase, edits files and calls verifiers. Pushing code, talking to users in Slack and writing prompts belong to the surrounding infrastructure. Its container has few permissions and few binaries, and can reach almost nothing else.
- Stated limits: verifiers run only on Linux x86, so iOS and ARM64 systems are not covered; the agent does not yet react to CI checks on the pull request; there are no structured evals.

## What to do with it

- Expose verification as one tool, and also enforce it as an exit condition.
- Summarise check output before it reaches the model.
- Add a scope judge that sees only the prompt and the diff.
- Keep privileged actions (push, messaging) in the platform, outside the agent's reach.

## Terms

- **Verifier** — an automatically selected check behind a single verify tool.
- **Judge** — a model that vetoes diffs which leave the scope of the prompt.

## Caveats

- From December 2025, about code migrations run on Claude Code. The judge figures are internal metrics with no measured error rate.
- Continues [part 1](2025-11-06-spotify-background-coding-agent-part-1.md).
