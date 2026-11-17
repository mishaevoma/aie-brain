---
name: brain-consult
description: Answer a question or review a plan using the AI engineering brain, a maintained wiki of current practice for building AI products (agents, harnesses, context engineering, tools, MCP, skills, memory, evals, verification, sandboxing). Use when designing or reviewing anything that involves an LLM or an agent, when the user asks what current best practice is or "what does the brain say", and when a term from this field is used and precision matters.
---

# Consult the brain

## 1. Find it

If the current project has `index.md`, `glossary.md` and `concepts/` at its root, you are in the brain. Otherwise run `sh brain-root.sh` from this skill's folder. It prints the brain's root, following the link this skill was installed through.

## 2. Read as little as answers the question

1. `index.md`, always. Add `glossary.md` when the question turns on a term, and `overview.md` when it is about the big picture or what is disputed.
2. The one to three concept pages or the playbook that fit.
3. A source note only for detail, a number, or a point the page marks as disputed.
4. The original URL only when the note is not enough.

## 3. Answer

- Lead with what to do in the user's situation, then the reasoning.
- Cite the pages you used by path, and give the date of each source you lean on.
- Say so when a page is marked `contested` or `evolving`, and when the newest source on a point is more than about six months old.
- Keep what the brain says separate from your own judgement, and label each.
- If the brain is silent, say that first. Then answer from general knowledge, labelled as such, and name a source worth ingesting.
- Use glossary terms as defined. If the user is using a term differently, point it out.

## 4. Give back

- Mention any gap, stale page or contradiction the question exposed.
- If your answer is a synthesis worth keeping, offer to file it as a page.
- Change the brain only when the user agrees, and then follow `brain-ingest` or edit the page and append to `log.md`.
