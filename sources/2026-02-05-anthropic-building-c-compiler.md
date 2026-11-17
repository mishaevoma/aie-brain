---
type: source
title: "Building a C compiler with a team of parallel Claudes"
author: "Nicholas Carlini"
publisher: Anthropic
url: https://www.anthropic.com/research/building-c-compiler
published: 2026-02-05
ingested: 2026-11-17
kind: article
read: full
concepts: [human-judgment, long-running-agents, multi-agent-systems, verification]
---

# Building a C compiler with a team of parallel Claudes

**In one line:** Sixteen Claude agents with no orchestrator, coordinating only through git and lock files, built a 100,000-line C compiler that boots Linux. The thing that made it work was the test harness, not the agents' prompts.

## What it says

- Setup: a bash loop restarts Claude Code (permissions skipped, inside a container) whenever a task ends. Each of 16 agents has its own Docker container and clone of a shared bare repo.
- Coordination: an agent claims a task by committing a lock file to `current_tasks/`. A git conflict forces a second claimant elsewhere. Agents merge (Claude handled frequent conflicts), push and release the lock. No messaging between agents, no manager.
- Scale: nearly 2,000 sessions over two weeks, 2 billion input and 140 million output tokens, just under $20,000. Built by Opus 4.6.
- Result: a dependency-free Rust compiler, written offline, that builds Linux 6.9 on x86, ARM and RISC-V, compiles QEMU, FFmpeg, SQLite, postgres and redis, passes about 99% of most suites (GCC torture tests included) and runs Doom. Opus 4 barely managed a working compiler; Opus 4.5 passed test suites but couldn't build real projects.
- Lessons on harnesses:
  - The verifier must be near perfect, or agents solve the wrong problem. Late on, new work kept breaking old features until CI blocked regressions.
  - Write for a reader with no memory: READMEs and progress files, terse console output with details in logs, greppable one-line errors.
  - Agents have no sense of time. A `--fast` mode runs a 1% or 10% test sample, fixed per agent but different across agents.
  - Parallelism needs separable work. The kernel, one huge target, had every agent chasing the same bug. Fix: GCC as a **known-good oracle**, compiling most files with GCC and a random subset with the new compiler, then delta debugging to find failing file pairs.
  - Specialist roles: deduplication, compiler speed, output efficiency, Rust design critique, docs.
- Limits: no 16-bit x86 codegen (GCC handles real-mode boot), GCC's assembler and linker, and optimized output slower than GCC with optimizations off. By the end, fixes regularly broke other features, which the author reads as near the model's ceiling.
- Passing tests can masquerade as finished work; unreviewed autonomous code is a security risk.

## What to do with it

- Spend most effort on tests and CI; they are the spec agents optimize against.
- Shape logs and test output for a context-free reader.
- Try simple coordination (git, lock files) before building an orchestrator.
- When work won't split, use a reference implementation as an oracle.
- Keep human review before deployment.

## Terms

- **Agent teams** — parallel Claude instances on one codebase with no human steering.
- **Known-good oracle** — a trusted implementation used to localize failures.

## Caveats

- A prototype stress test by an Anthropic researcher on Anthropic's own model (Opus 4.6), with a large budget. Later models should move the ceiling.
- The compiler is not a drop-in GCC replacement.
