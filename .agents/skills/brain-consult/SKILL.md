---
name: brain-consult
description: Answer a question, or review a plan or a whole design, using the AI engineering brain, a maintained wiki of current practice for building AI products (agents, harnesses, context engineering, tools, MCP, skills, memory, evals, verification, sandboxing). Use when designing or reviewing anything that involves an LLM or an agent, when the user asks what current best practice is or "what does the brain say", and when a term from this field is used and precision matters.
---

# Consult the brain

Consulting is read-only. It never changes the brain.

## 1. Find it

Run the `brain-root.sh` that sits beside this file: `sh <this skill's folder>/brain-root.sh`. It works from any current folder. It prints the root of a copy of the brain on this machine. Do all your reading from that folder.

Where it looks:

- If `AIE_BRAIN` is set, that folder is the brain's home and nothing else is tried.
- Otherwise: the repository this skill sits in or is linked from, then the current folder and its parents, then `~/.aie-brain`.

If there is no copy yet, which is the case the first time a copied install of this skill runs, the script clones `https://github.com/mishaevoma/aie-brain` into `~/.aie-brain`, or into `AIE_BRAIN` when that is set, and says so. Tell the user when that happens: a new folder has appeared on their machine. The copy in `~/.aie-brain`, and any copy the script cloned, is brought up to date at most once a day.

If the script fails, it says why. Then:

1. Run the clone yourself: `git clone --depth 1 https://github.com/mishaevoma/aie-brain ~/.aie-brain`. A sandbox that blocks the network or the home folder needs the user's approval for this.
2. If this machine cannot hold a clone, read the public copy with your fetch tool. Start at `https://mishaevoma.github.io/aie-brain/llms.txt`. It is the index, with a link to every page as raw markdown. Say in your answer that you used the public copy.

Nothing else needs installing. This file is the whole procedure, and reading it is enough to follow it.

## 2. Read as little as answers the question

1. `index.md`, always. Its "By decision" section goes from a question to the pages that answer it. Add `glossary.md` when the question turns on a term, and `overview.md` when it is about the big picture or what is disputed.
2. The one to three concept pages or the playbook that fit.
3. A source note only for detail, a number, or a point the page marks as disputed.
4. The original URL only when the note is not enough.

Do not load the whole wiki.

## 3. Review a whole design

A review of an architecture or a repository setup is many questions at once, so the limit of three pages does not apply. Use a playbook as the checklist. One decision inside a design, such as whether to split an agent into several, is a question: answer it with section 2.

1. Pick the playbook: `playbooks/building-an-agent-product.md` for a product, `playbooks/setting-up-a-repo-for-coding-agents.md` for a repository and the coding agents that work in it.
2. Take its steps in order. For each step, read the concept page it names and compare the design with it.
3. Give each step a verdict: **aligned**, **gap**, or **silent** when the brain has no page on it. Keep what is built apart from what is planned. A plan that agrees with the brain is still a gap until it is built.
4. Rank the changes you would make, most important first, each with the page and the source date behind it.
5. End with what the brain cannot judge, so that its silence is not read as approval.

## 4. Answer

- Lead with what to do in the user's situation, then the reasoning.
- Cite the pages you used by their path inside the brain, and give the date of each source you lean on.
- Say so when a page is marked `contested` or `evolving`, and when the newest source on a point is more than about six months old.
- Say whose models or product a figure was measured on when the user runs something else. Most figures here come from one vendor.
- Keep what the brain says separate from your own judgement, and label each.
- If the brain is silent, say that first. Then answer from general knowledge, labelled as such, and name a source worth ingesting.
- Use glossary terms as defined. If the user is using a term differently, point it out.
- If the answer will be kept, name the version of the brain it read: the output of `git -C <brain root> log -1 --format='%h %cs'`.

## 5. Give back

- Mention any gap, stale page or contradiction the question exposed. Check the last section of `overview.md` and `watchlist.md` first, so you do not report what is already listed.
- Offer to file each one where it belongs:
  - A gap goes under "What this brain does not cover yet" in `overview.md`, and into `watchlist.md` as something to look for.
  - Two pages that pull apart are reconciled on the concept page: both positions with their sources and dates, then a line labelled as this brain's reading.
  - A synthesis worth keeping becomes a section on a concept page, or a playbook when it is shaped like a task.
- Keep anything about the user's own project in that project. This repository is public: record what you learned in general terms, with no names, architecture or data from the work you were consulting for.
- Where a change goes depends on whose copy you are reading. In the brain's own repository, changing it is a separate job, done with its `brain-ingest` skill and only when the user agrees. A copy the script cloned is for reading: do not edit it, because local changes stop its updates. From there, offer to report the gap as an issue at `https://github.com/mishaevoma/aie-brain/issues`, in general terms, and open it only when the user agrees.
