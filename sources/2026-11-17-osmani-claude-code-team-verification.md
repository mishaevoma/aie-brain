---
type: source
title: "How the Claude Code team thinks about verification"
author: "Addy Osmani"
publisher: "@addyosmani on X"
url: https://x.com/addyosmani/status/2122590683055993308
published: 2026-11-17
ingested: 2026-11-17
kind: x-article
read: full
concepts: [compounding, evals, human-judgment, knowledge-factory, multi-agent-systems, skills, verification]
---

# How the Claude Code team thinks about verification

**In one line:** Verification loops are what let you run many agents at once, so treat the checks as a system of their own: fast, hard to fool, out of reach of the change they judge, and tuned against the bugs that actually hurt you.

## What it says

- About 90% of the Claude Code team's code is written and reviewed by Claude. Without verification loops a person can supervise one or two agents; with them, dozens or hundreds.
- In an internal test on structured file generation, a separate grader checking output against a rubric raised task success by up to 10 points over a plain prompting loop, most on the hardest problems.
- Tests, benchmarks and specs are now cheap to ask an agent for, and once written they run as ordinary software without spending many tokens.
- Flaky tests teach the agent to re-run instead of fix. Slow tests get run less often, which makes failures harder to pin down.
- Three kinds of test are worth the investment:
  - **End-to-end tests** of real user flows. Hard to fool, clear done criteria, and they can show a screenshot of what broke. Unit tests can pass while the feature is broken.
  - **Property tests** (fast-check, Hypothesis, proptest): state something that must always hold and generate thousands of inputs against it. Typical properties: round-trip, invariants, idempotency, equivalence with a slow correct version.
  - **Differential tests** for migrations: run old and new systems on the same random or production-sampled inputs and compare, ignoring irrelevant differences and keeping a list of approved changes.
- How the team works:
  - Verifying means running the change end to end, the way a QA engineer would: browser extension for web, simulator MCP for mobile, computer use for desktop, a local run for backend.
  - A `verify` skill, kept near the code it covers, records how to start and drive the app. Claude runs it before committing.
  - Claude tries to fix failing checks. If one still fails after three rounds, it stops and a person steps in.
  - The owners of the code write its checks, and a check that pulls in a reviewer says why.
  - A reliability checklist has 39 items, each with a trigger readable from a diff. Usually 3 to 10 apply to a given change.
  - One reviewer tuned through a `REVIEW.md`, run over several rounds that build on earlier findings, beats stacking a second reviewer on top.
  - A change cannot edit its own checks: `REVIEW.md` is read from the base branch. Reviews are tied to a specific commit.
  - Cheap checks run first. Tests, build and linter run locally before a pull request is opened.
  - New gates start in observe mode (off, observe, enforce). Commits are stamped with how they were verified, including "none".
- They review the reviewers: reverts, changes rejected by maintainers, and a size-matched set of clean changes as a control. The code review eval is built from past incidents, each with a one-sentence answer key, with separate tuning and test sets and recall measured at each stage of the pipeline.
- Misses become rules. A pattern qualifies if it appeared in at least two pull requests and can be seen in a diff; three agents try to disprove it and a person approves it. Rules and tests are pruned on a routine.

## What to do with it

- Give every agent task a way to run the real thing, and package it as a `verify` skill.
- Prefer end-to-end, property and differential tests over piles of generated unit tests.
- Fix or delete flaky tests. Do not let the agent skip, sleep or retry around them.
- Keep the rules that gate a change on a branch the change cannot touch.
- Set a round limit (they use three) after which a failing check goes to a person.
- Roll out a new gate in observe mode and read what it would have blocked before enforcing it.
- Measure your reviewer against real past bugs, with a clean control set, and stop tuning when you start fitting the eval.

## Terms

- **Verification loop** — the agent changes something, runs a check, reads the result and tries again before a person looks.
- **Differential test** — the old system acts as the oracle for the new one.
- **Observe mode** — a gate that logs what it would block without blocking.

## Caveats

- Published the day it was ingested; describes one team's practice with Claude Code features (`/verify`, `/code-review`, `/goal`, hooks). The author works on that team.
- The 10-point figure is from an internal test with no method given.
