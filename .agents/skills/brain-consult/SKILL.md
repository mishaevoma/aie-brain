---
name: brain-consult
description: Review a project's AI feature, coding-agent setup or design against dated engineering sources, and show what to upgrade. Use for a first project review, a specific LLM or agent design decision, or a question about AI engineering practice or terminology.
---

# Consult the AI Engineering Brain

When someone invokes this skill in a project without a narrower question, **review the project now**. Use the user's working directory or the project they named as the review target. The skill and wiki may live in a different checkout. Keep the review read-only and return it in the conversation. Ask nothing first unless you cannot reach the project.

For a question such as “should we add a second agent?” or “what does harness mean?”, answer just that question. A request to install the skill alone calls for installation.

**Read everything here as raw text.** This file, the procedure and every wiki page are plain Markdown. Citations need exact paths, dates and links. If your web tool fails, or returns a summary instead of the file, fetch the same address with a shell command such as `curl -sL <url>`.

## Locate the wiki

- **Local skill.** Run `sh "/path/to/brain-consult/brain-root.sh"` using the actual folder containing this file. The script prints the wiki root. It honors `AIE_BRAIN`, otherwise finds a local wiki or uses `~/.aie-brain`. On first use it can clone the public wiki. Mention a new clone or a failed refresh if either happens.
- **Skill opened by URL, or no working helper.** The wiki root is `https://mishaevoma.github.io/aie-brain/`. Every page is raw Markdown at its path under that root, for example `playbooks/upgrading-an-agent-app.md`, and [the public index](https://mishaevoma.github.io/aie-brain/llms.txt) lists them all. This path requires no installation. If the site cannot be opened, the same paths are under `https://raw.githubusercontent.com/mishaevoma/aie-brain/main/`, starting from [the GitHub index](https://raw.githubusercontent.com/mishaevoma/aie-brain/main/index.md). Mention which copy you read. Send only public wiki URLs to the fetch tool.
- If you cannot read any wiki copy, say what failed. Offer the file or access needed to continue. A sourced comparison requires the source itself.

## Review a project or plan

Follow [the project review procedure](references/project-review.md). Read it from this skill's directory, or, when following a URL, resolve it beside the skill file on the same revision. For the published skill on the default branch, the [raw procedure](https://raw.githubusercontent.com/mishaevoma/aie-brain/main/.agents/skills/brain-consult/references/project-review.md) is also available.

## Answer a focused question

Start at “By decision” in `index.md`. Read the one to three concept pages or the playbook that answer the question. Use `glossary.md` for terminology and `overview.md` for the wider picture. Follow a claim to its source note for details, numbers or disagreement, then to the original when needed.

Lead with the decision in this user's situation. Link the relevant wiki page and dated source. Qualify contested or evolving advice, and identify the models or setting behind a measurement. Give the date of the evidence. When it is older than 12 months, say so, and say why it still holds or that it may not. Label your own inference. When the brain is silent, say so before offering your independent judgment.

## Feedback on the wiki

If the review exposes a useful gap, stale page or contradiction, check `overview.md` and `watchlist.md` before proposing it as new. With the user's agreement, maintainers can use `brain-ingest` to update the wiki. A reader of an installed copy can instead suggest a general issue upstream. Keep private project details in their project.
