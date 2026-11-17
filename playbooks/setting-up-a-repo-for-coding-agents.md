---
type: playbook
title: "Setting up a repository for coding agents"
updated: 2026-11-17
---

# Setting up a repository for coding agents

What to put in a repository so that an agent, in any tool, can do correct work with no extra context from the person prompting. Do the steps in order; each is useful on its own.

## 1. One short instruction file

- Create `AGENTS.md` at the root. Put in build and test commands, conventions the agent cannot infer, warnings, and a table pointing to deeper documents. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md)
- Keep it under 150 lines. Apply the deletion test to every line. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- If a tool wants its own filename, make that file an import of `AGENTS.md`, not a copy. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Lütke, Aug 2026](../sources/2026-08-25-lutke-agents-md-split-brain.md)
- Write it by hand, or edit a generated draft hard. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Theo, Jul 2026](../sources/2026-07-28-theo-rewriting-agents-md-by-hand.md)

Detail: [instruction files](../concepts/instruction-files.md).

## 2. A way to verify

- Add a `verify` skill that says how to start, drive and inspect the app. Make it fast and reliable. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Make sure tests, build and linter run with one command each, and list them in the instruction file. [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md) · [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Fix or delete flaky tests before agents rely on them. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

Detail: [verification](../concepts/verification.md).

## 3. Skills for procedures

- Move anything procedural out of the instruction file into `.agents/skills/`, one folder per procedure, with a description that says when to use it. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md) · [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Put deterministic steps in scripts inside the skill. [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- Link the folder for tools that look elsewhere. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)

Detail: [skills](../concepts/skills.md).

## 4. Checks the change cannot edit

- Encode house rules as lint rules, tests and CI steps wherever a machine can check them. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
- Keep review guidance in a file that is read from the base branch. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- Introduce a new gate in observe mode first. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

Detail: [compounding](../concepts/compounding.md).

## 5. Permissions and boundaries

- Turn on the sandbox, with network denied by default and an allow-list. [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- Pre-approve the safe read-only commands you keep being asked about. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md)
- Remember that anyone who can edit the repository's instruction files can instruct your agent. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md) · [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

Detail: [permissions, sandboxing and containment](../concepts/sandboxing-and-permissions.md).

## 6. A pruning routine

- Every so often, remove unused skills and MCP servers, deduplicate instruction files, and split any that have grown. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md)
- Delete as readily as you add. [Theo, Jul 2026](../sources/2026-07-28-theo-rewriting-agents-md-by-hand.md) · [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)

## 7. Test the setup

- Ask someone who does not know the codebase to get a small change merged by prompting alone. Each place they get stuck is something to encode. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
- When the agent repeats a mistake, add the fix to the right place: a check if possible, otherwise the instruction file or a skill. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)

Detail: [context layer](../concepts/context-layer.md).
