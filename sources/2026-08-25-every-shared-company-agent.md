---
type: source
title: "Every Agent and Headway's Eddy: one shared company agent (untitled post)"
author: "Every"
publisher: "@every on X"
url: https://x.com/every/status/2092356392808263755
published: 2026-08-25
ingested: 2026-11-17
kind: x-post
read: partial
concepts: [context-layer, llm-wiki, production-operations, sandboxing-and-permissions]
---

# Every Agent and Headway's Eddy: one shared company agent

**In one line:** Two companies built a single agent shared by all staff, with company knowledge and system access built in, because nothing off the shelf met their needs.

## What it says

- Every is building "Every Agent": one shared company agent that any colleague can ask for help. It has organisational knowledge and connections to their codebase, payment gateway and analytics platforms.
- They built it themselves because no product had both their requirements and the skills they wanted, such as their editor-in-chief's copy-editing taste.
- Headway, a mental healthcare company with 900 employees, reached the same conclusion and built "Eddy" to meet its compliance and workflow needs.
- Eddy is built on Anthropic's Claude Code SDK and hosted in Headway's own AWS environment. Each conversation runs in a fresh, disposable Docker container so confidential patient information stays private.

## What to do with it

- For an internal agent, start from an existing agent SDK and add your own knowledge, connections and skills.
- Where data is sensitive, give each conversation its own throwaway container.
- Encode specific people's judgement as skills; it is the part you cannot buy.

## Terms

- **Shared company agent** — one agent for the whole organisation with common knowledge and tool access, as opposed to each person configuring their own.

## Caveats

- Only the post was read. The linked Every article about Headway was not, hence `read: partial`.
- Promotional. "Company brain" is the marketing label sometimes used for this idea.
