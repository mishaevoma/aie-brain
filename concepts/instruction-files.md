---
type: concept
title: "Instruction files (AGENTS.md, CLAUDE.md)"
updated: 2026-11-17
status: evolving
---

# Instruction files (AGENTS.md, CLAUDE.md)

**Definition:** A markdown file the harness loads into every session to orient the agent in a project: commands, conventions, warnings and pointers to deeper documents. `AGENTS.md` is the vendor-neutral name. `CLAUDE.md` is Claude Code's.

## Why it matters

The file rides along with every prompt, so every line is paid for in every session and competes for the model's attention. A short accurate file helps. A long generated one can make results worse. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)

## What to do

- Keep it short: under 150 lines, and 30 to 50 for a small repository. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Apply the deletion test to each line: would removing it cause a mistake the agent would not otherwise make? If not, remove it. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Use it as an index. A small table from topic to file beats pasting the content in. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md)
- Put in what the agent cannot infer: build and test commands, style rules, repository etiquette, environment quirks, warnings. [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md)
- Grow it from failures you observe. When the agent repeats a mistake, add the fix. Do not write rules for imagined edge cases. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Write at the right altitude: between brittle if-else rules and guidance so vague it assumes shared context. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Write or edit it by hand. From a generated draft, cut what the model can work out and add silent invariants, unusual conventions and past gotchas. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Theo, Jul 2026](../sources/2026-07-28-theo-rewriting-agents-md-by-hand.md)
- Split it when it grows: nested files per directory for area-specific rules, skills for procedures. [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md) · [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md)
- Keep one source of truth. Use `AGENTS.md`, and where a tool needs its own filename make that file an import of the shared one. Two copies drift apart when teammates use different tools, a problem known as split brain. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Lütke, Aug 2026](../sources/2026-08-25-lutke-agents-md-split-brain.md)
- Commit it so the whole team shares it. [Claude Code best practices, Apr 2025](../sources/2025-04-18-anthropic-claude-code-best-practices.md)

## Risks

- These files are loaded into the prompt by design. A repository's instruction file is untrusted input until you trust its authors. [Loams, Oct 2026](../sources/2026-10-18-loams-coding-agent-harnesses.md)
- Project configuration must not take effect before the trust decision. Three bugs let input from an untrusted repository run code before the trust dialog, one of them a hook in the repository's own settings file. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md)

## Where sources disagree

- **Encode more.** Nearly all domain knowledge can now be written down as rules, review guides and skills, and every rejected pull request is a sign of something missing. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md)
- **Load less.** Keep the always-on file small and delete as much as you add. [Red Hat, Jul 2026](../sources/2026-07-27-redhat-agents-md-and-agent-skills.md) · [Cherny, 9 Jul 2026](../sources/2026-07-09-cherny-checkup.md) · [Theo, Jul 2026](../sources/2026-07-28-theo-rewriting-agents-md-by-hand.md)

The two fit together: write more down, but put it where it loads only when needed, or turn it into a check. See [skills](skills.md) and [compounding](compounding.md).

## What is changing

Tool support for `AGENTS.md` was uneven through mid-2026 and was still moving at the time of writing. The note on [Lütke, Aug 2026](../sources/2026-08-25-lutke-agents-md-split-brain.md) records what was checked on 17 Nov 2026.

## Related

[Context layer](context-layer.md) · [Skills](skills.md) · [Context engineering](context-engineering.md) · [Compounding](compounding.md)
