---
name: brain-consult
description: Answer a question or review a plan using the AI engineering brain, a maintained wiki of current practice for building AI products (agents, harnesses, context engineering, tools, MCP, skills, memory, evals, verification, sandboxing). Use when designing or reviewing anything that involves an LLM or an agent, when the user asks what current best practice is or "what does the brain say", and when a term from this field is used and precision matters.
---

# Consult the brain

Consulting is read-only. It never changes the brain.

## 1. Find it

Run `sh brain-root.sh` from this skill's folder. It prints the root of a local copy of the brain. It looks in three places: the repository this skill is linked from, the current folder and its parents, and the path in the `AI_ENGINEERING_BRAIN` environment variable.

If it finds none, read the public copy. Start at `https://raw.githubusercontent.com/mishaevoma/ai-engineering-brain/main/index.md`. Every path in the index is relative to `https://raw.githubusercontent.com/mishaevoma/ai-engineering-brain/main/`. Say in your answer that you used the public copy.

## 2. Read as little as answers the question

1. `index.md`, always. Its "Route by decision" table points from the decision at hand to the page that covers it.
2. `glossary.md` when the question turns on a term, and `overview.md` when it is about the big picture or what is disputed.
3. The one to three concept pages or the playbook that fit.
4. A source note only for detail, a number, or a point the page marks as disputed.
5. The original URL only when the note is not enough.

Do not load the whole wiki.

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
- Changing the brain is a separate job, done in the brain's own repository with its `brain-ingest` skill, and only when the user agrees.
