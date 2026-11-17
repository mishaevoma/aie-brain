---
type: source
title: "Standardize project context with AGENTS.md and Agent Skills"
author: "Dejan Bosanac"
publisher: "Red Hat Developer"
url: https://developers.redhat.com/articles/2026/07/27/standardize-project-context-agentsmd-and-agent-skills
published: 2026-07-27
ingested: 2026-11-17
kind: article
read: full
concepts: [compounding, context-layer, instruction-files, skills]
---

# Standardize project context with AGENTS.md and Agent Skills

**In one line:** keep a short, hand-edited AGENTS.md for always-on context that points to deeper docs, and put situational procedures in Agent Skills that load only when needed.

## What it says

- Context is the main lever on coding-agent results. Two open specs address it: AGENTS.md and Agent Skills.
- **AGENTS.md** is a predictable, agent-neutral home for project context, like a README for agents: setup, tools, where tests are and how to run them, where design docs live.
- Don't keep parallel `CLAUDE.md` / `GEMINI.md` copies. Most agents read AGENTS.md; Claude Code does not, so make a `CLAUDE.md` containing `@AGENTS.md` with Claude-only additions below.
- AGENTS.md rides along with every prompt. Keep it under 150 lines (30 to 50 for small repos). Test each line: would deleting it cause a mistake the agent wouldn't otherwise make? If not, delete it.
- Edit the output of an agent's `init` command: drop what the model can infer, add silent invariants, unusual conventions and past gotchas. Cited ETH Zurich research found generic auto-generated context files can hurt performance.
- Use AGENTS.md as an index: an "orientation table" mapping topics to files (`README.md`, `ARCHITECTURE.md`, `specs/README.md`). When the agent repeats a mistake, add the fix.
- A **skill** is a folder with a `SKILL.md` whose YAML front matter requires `name` and `description`; the description decides relevance. Optional `scripts/`, `references/`, `assets/` are read only when referenced.
- **Progressive disclosure:** only names and descriptions load up front.
- Skills trigger from intent ("let's commit this") or as slash commands (`/pre-commit-check`). Write steps tool-neutrally ("Run linting") and teach only project-specific practice.
- Discovery is unstandardized; the emerging convention is `.agents/skills/`, symlinked for agents that look elsewhere.
- Sharing: a separate repo cloned, symlinked or used as a submodule (scales poorly), or plug-ins and marketplaces. Claude Code uses `.claude-plugin/plugin.json`, a repo-root `marketplace.json`, `/plugin marketplace add`, `/plugin install dev@skill-workshop`. Cursor and Gemini CLI differ. Red Hat's **Lola** (`lola install`) versions skills across assistants.

## What to do with it

- Make AGENTS.md the single source and import it from `CLAUDE.md`.
- Prune with the would-it-cause-a-mistake test; stay under 150 lines.
- Turn repeated procedures into tool-neutral skills with precise descriptions in `.agents/skills/`.

## Terms

- **AGENTS.md** — a dedicated, predictable file of always-on context and instructions for coding agents.
- **project context** — orientation information, like a README for agents.
- **skill** — a folder containing `SKILL.md`, per the open Agent Skills spec for task-specific instructions.
- **progressive disclosure** — metadata up front, full content on demand.
- **plug-in / marketplace** — a named bundle of skills / a git repo listing plug-ins for one-command install.

## Caveats

- Does not define "agent" or "harness".
- Mid-2026 snapshot; discovery, packaging and AGENTS.md support may have changed.
- Promotes Red Hat's Lola; the ETH Zurich study (arXiv 2602.11988) was not read here.
- Part one of a series; skill writing and trigger testing come later.
