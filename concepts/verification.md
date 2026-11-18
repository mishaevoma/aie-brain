---
type: concept
title: "Verification"
updated: 2026-11-18
reviewed: 2026-11-17
status: evolving
---

# Verification

**Definition:** Giving an agent a way to check its own work against something real (the running product, tests, an independent grader) and making that evidence, not the agent's summary, the condition for "done".

## Why it matters

The bottleneck has moved from writing code to being sure it is right. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md) Without verification loops a person can supervise one or two agents, because everything has to be checked by hand. With them the number is far higher. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

## What to do

**Define done first**

- Decide what "verified" means before the work starts. Afterwards you will rationalise whatever you got. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Write failing tests first and forbid the agent from changing them, or keep a task list where it may only flip a pass field. [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md) · [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)
- For larger work, have builder and grader agree on completion criteria before each stage. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)

**Run the real thing**

- Verifying means running the change end to end, as a tester would: browser, simulator, or a local run of the service. Package how to do it as a `verify` skill and keep it fast and reliable. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Testing through the interface like a user caught far more than unit tests or direct requests. [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)

**Invest in tests that are hard to fool**

- End-to-end tests of real user flows. Unit tests can pass while the feature is broken. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Property tests: state what must always hold and generate thousands of inputs against it. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Differential tests: run old and new on the same inputs and compare. A trusted implementation also works as a known-good oracle to localise failures. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md) · [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)
- Fix or delete flaky tests. A flaky test teaches the agent to re-run instead of fix. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

**Separate the judge from the judged**

- Use a separate, sceptical evaluator. Agents rate their own work too highly, and a model is a lenient tester until it is tuned. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- Review with a fresh context. [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md) · [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Keep the rules that gate a change where the change cannot edit them, such as on the base branch. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

**Run it as a system**

- Run cheap checks first, before shared review and CI. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Set a round limit, after which a failing check goes to a person. One team uses three. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Cap the expensive rounds separately. One company allows an unattended agent at most two full CI runs, after it has looped on local linters. [Stripe, Feb 2026](../sources/2026-02-19-stripe-minions-part-2.md)
- For an agent nobody is watching, expose the checks as one tool and run them again as a condition for finishing. One team's agent does not know what the tool runs: checks are picked by what the repository contains, and their output is cut to the relevant errors. [Spotify, Dec 2025](../sources/2025-12-09-spotify-feedback-loops-part-3.md)
- Add a judge that sees only the task and the diff, to catch work outside the task. At that company it vetoes about a quarter of sessions, and after a veto the agent corrects course about half the time. The judge itself has no evals yet. [Spotify, Dec 2025](../sources/2025-12-09-spotify-feedback-loops-part-3.md)
- Start a new gate in observe mode and read what it would have blocked before enforcing it. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Measure your checks against real past bugs, with a clean control set. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Read the command and its output before the agent's summary. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)

## Limits

- A green check proves one property. A test written with the same misunderstanding as the feature passes. Ask what the check proved and what it did not. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- The verifier has to be close to perfect, because agents optimise against it. A weak one has them solving the wrong problem. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)
- Tests the agent cannot see can leave it believing a superficial fix worked. [SWE-bench scaffold, Jan 2025](../sources/2025-01-06-anthropic-swe-bench-sonnet.md)
- Passing tests can look like finished work. Keep human review before deployment. [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)

## Related

[Evals](evals.md) · [Compounding](compounding.md) · [Long-running agents](long-running-agents.md) · [Background agents](background-agents.md) · [Human judgment](human-judgment.md) · [Skills](skills.md)
