---
type: source
title: "Equipping agents for the real world with Agent Skills"
author: "Barry Zhang, Keith Lazuka, Mahesh Murag"
publisher: Anthropic
url: https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills
published: 2025-10-16
ingested: 2026-11-17
kind: article
read: full
concepts: [context-engineering, mcp, skills]
---

# Equipping agents for the real world with Agent Skills

**In one line:** package domain know-how as folders of instructions, scripts and resources that a general agent loads in stages, only when a task needs them, instead of building separate specialized agents.

## What it says

- An **Agent Skill** is a directory containing a `SKILL.md` file. The file begins with YAML frontmatter with two required fields, `name` and `description`, followed by instructions. It can bundle further files and code. The post compares it to an onboarding guide for a new hire.
- **Progressive disclosure** is the core design:
  - Level 1: at startup only the `name` and `description` of each installed skill go into the system prompt, enough for the agent to know when a skill applies.
  - Level 2: when a skill looks relevant, the agent reads the full `SKILL.md`, for example through a Bash tool call.
  - Level 3 and beyond: linked files such as `reference.md` or `forms.md` are opened only if the task needs them.
- Because the agent reads files from a filesystem on demand, a skill can bundle a practically unlimited amount of material without filling the context window.
- Skills can include scripts the agent runs as tools. Code is cheaper and more deterministic than generating the same result token by token; sorting is the example. The PDF skill (in the public `anthropics/skills` repo) includes a Python script that extracts a PDF's form fields, so the agent never has to load the script or the PDF into context.
- **Authoring advice**: start from evals and add skills where the agent struggles. Split a long `SKILL.md` into referenced files, keeping rarely combined content apart. Say whether a script is to be run or read. Watch real usage, especially whether `name` and `description` make the skill trigger. Ask Claude to write successes and mistakes back into the skill.
- **Security**: a skill can carry malicious instructions or exfiltrating code. Install only from trusted sources, and audit others first, including scripts, dependencies and any calls to outside network sources.
- Skills are available in Claude.ai, Claude Code, the Claude Agent SDK and the Claude Developer Platform. The post presents them as a complement to MCP: MCP connects tools, while skills teach multi-step workflows that use those tools. Anthropic hopes agents will eventually create, edit and evaluate their own skills.

## What to do with it

- Move procedural knowledge out of system prompts and into skills that load on demand. Keep the always-loaded part down to name plus description.
- Write the `description` as a trigger condition, and test that the skill fires when it should.
- Put deterministic steps (parsing, extraction, sorting) into bundled scripts instead of prose instructions.
- Treat third-party skills like third-party code: review before installing.

## Terms

- **Agent Skill** — a folder with a `SKILL.md` (name, description, instructions) plus optional files and scripts that an agent loads dynamically.
- **Progressive disclosure** — loading context in layers (metadata, then body, then linked files) as relevance becomes clear.

## Caveats

- A Dec 18, 2025 update on the page says Agent Skills were published as an open standard (agentskills.io). The original post describes them only as an Anthropic feature.
- This is a product launch by the vendor. It reports no quantitative results.
- Skills assume a filesystem and code execution, which brings the sandboxing costs raised in the 2025-11-04 code-execution note. That note also shows agents saving their own code as skills.
