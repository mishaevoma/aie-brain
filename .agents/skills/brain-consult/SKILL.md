---
name: brain-consult
description: Review a project's coding-agent setup, AI product, or design against dated engineering sources. Use for a first project review, a specific LLM or agent design decision, or a question about AI engineering practice or terminology.
---

# Consult the AI Engineering Brain

When someone invokes this skill in a project without a narrower question, **review the project now**. Use the user's working directory or the project they named as the review target. The skill and wiki may live in a different checkout. Keep the review read-only and return it in the conversation.

For a question such as “should we add a second agent?” or “what does harness mean?”, answer just that question. A request to install the skill alone calls for installation.

## Locate the wiki

- **Local skill.** Run `sh "/path/to/brain-consult/brain-root.sh"` using the actual folder containing this file. The script prints the wiki root. It honors `AIE_BRAIN`, otherwise finds a local wiki or uses `~/.aie-brain`. On first use it can clone the public wiki. Mention a new clone or a failed refresh if either happens.
- **Skill opened by URL, or no working helper.** Fetch [the public index](https://mishaevoma.github.io/aie-brain/llms.txt) and follow its raw Markdown links. This path requires no installation. If the site is unavailable, read [the GitHub index](https://raw.githubusercontent.com/mishaevoma/aie-brain/main/index.md) and resolve its links relative to that file. Mention which copy you read. Send only public wiki URLs to the fetch tool.
- If you cannot read any wiki copy, say what failed. Offer the file or access needed to continue. A sourced comparison requires the source itself.

## Review a project or plan

Follow [the project review procedure](references/project-review.md). Read it from this skill's directory, or, when following a URL, resolve it beside the skill file on the same revision. For the published skill on the default branch, the [raw procedure](https://raw.githubusercontent.com/mishaevoma/aie-brain/main/.agents/skills/brain-consult/references/project-review.md) is also available.

## Answer a focused question

Start at “By decision” in `index.md`. Read the one to three concept pages or the playbook that answer the question. Use `glossary.md` for terminology and `overview.md` for the wider picture. Follow a claim to its source note for details, numbers or disagreement, then to the original when needed.

Lead with the decision in this user's situation. Link the relevant wiki page and dated source. Qualify contested or evolving advice, call out supporting evidence older than about six months, and identify the models or setting behind a measurement. Label your own inference. When the brain is silent, say so before offering your independent judgment.

## Feedback on the wiki

If the review exposes a useful gap, stale page or contradiction, check `overview.md` and `watchlist.md` before proposing it as new. With the user's agreement, maintainers can use `brain-ingest` to update the wiki. A reader of an installed copy can instead suggest a general issue upstream. Keep private project details in their project.
