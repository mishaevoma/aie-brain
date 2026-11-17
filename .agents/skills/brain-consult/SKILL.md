---
name: brain-consult
description: Answer a question, or review a plan or a whole design, using the AI engineering brain, a maintained wiki of current practice for building AI products (agents, harnesses, context engineering, tools, MCP, skills, memory, evals, verification, sandboxing). Use when designing or reviewing anything that involves an LLM or an agent, when the user asks what current best practice is or "what does the brain say", and when a term from this field is used and precision matters.
---

# Consult the brain

## 1. Find it

If the current project has `index.md`, `glossary.md` and `concepts/` at its root, you are in the brain. Otherwise run `sh brain-root.sh` from this skill's folder. It prints the brain's root: the folder named in `AIE_BRAIN` if that is set, otherwise the folder this skill was installed from.

If the brain is not on this machine, clone it and read from the clone: `git clone --depth 1 https://github.com/mishaevoma/ai-engineering-brain`. Nothing needs installing. This file is the whole procedure, and reading it is enough to follow it.

## 2. Read as little as answers the question

1. `index.md`, always. Its "By decision" section goes from a question to the pages that answer it. Add `glossary.md` when the question turns on a term, and `overview.md` when it is about the big picture or what is disputed.
2. The one to three concept pages or the playbook that fit.
3. A source note only for detail, a number, or a point the page marks as disputed.
4. The original URL only when the note is not enough.

## 3. Review a whole design

A review of an architecture or a repository setup is many questions at once, so the limit of three pages does not apply. Use a playbook as the checklist.

1. Pick the playbook: `playbooks/building-an-agent-product.md` for a product, `playbooks/setting-up-a-repo-for-coding-agents.md` for a repository and the coding agents that work in it.
2. Take its steps in order. For each step, read the concept page it names and compare the design with it.
3. Give each step a verdict: **aligned**, **gap**, or **silent** when the brain has no page on it. Keep what is built apart from what is planned. A plan that agrees with the brain is still a gap until it is built.
4. Rank the changes you would make, most important first, each with the page and the source date behind it.
5. End with what the brain cannot judge, so that its silence is not read as approval.

## 4. Answer

- Lead with what to do in the user's situation, then the reasoning.
- Cite the pages you used by path, and give the date of each source you lean on.
- Say so when a page is marked `contested` or `evolving`, and when the newest source on a point is more than about six months old.
- Say whose models or product a figure was measured on when the user runs something else. Most figures here come from one vendor.
- Keep what the brain says separate from your own judgement, and label each.
- If the brain is silent, say that first. Then answer from general knowledge, labelled as such, and name a source worth ingesting.
- Use glossary terms as defined. If the user is using a term differently, point it out.
- If the answer will be kept, name the version of the brain it read: the output of `git log -1 --format='%h %cs'` in the brain's root.

## 5. Give back

- Mention any gap, stale page or contradiction the question exposed.
- Offer to file each one where it belongs:
  - A gap goes under "What this brain does not cover yet" in `overview.md`, and into `watchlist.md` as something to look for.
  - Two pages that pull apart are reconciled on the concept page: both positions with their sources and dates, then a line labelled as this brain's reading.
  - A synthesis worth keeping becomes a section on a concept page, or a playbook when it is shaped like a task.
- Keep anything about the user's own project in that project. This repository is public: record what you learned in general terms, with no names, architecture or data from the work you were consulting for.
- Change the brain only when the user agrees, and then follow `brain-ingest` or edit the page and append to `log.md`.
