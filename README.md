# AI Engineering Brain

Use the brain to review how coding agents work in your repository or how your product uses LLMs. The review pairs evidence from your project with dated engineering sources, then recommends what to change first and how to check the result.

## Review your project

Open your coding agent in the project you want reviewed and paste this prompt.

```text
Review this project using https://mishaevoma.github.io/aie-brain/review.md
```

This works with an agent that can read your project and fetch public Markdown. The review runs in your current session and returns its findings in chat. You can also give it the [skill on GitHub](https://github.com/mishaevoma/aie-brain/blob/main/.agents/skills/brain-consult/SKILL.md).

For a narrower pass, add a focus such as “just the steps from a clean checkout to a passing test” or “what happens if the worker retries a customer action?”

## Install for repeated use

Run this from the project directory.

```sh
npx skills add mishaevoma/aie-brain --skill brain-consult
```

Select your coding agent when prompted. For a user-wide install, add `-g`. Open a new agent session in the project and ask it to use the skill.

```text
Use brain-consult to review this project.
```

To update an existing project install, run `npx skills update brain-consult -p`.

The installed skill locates the wiki on first use. With Git and a POSIX shell, it can clone the wiki into `~/.aie-brain` and reuse it on later runs. You can also point `AIE_BRAIN` at an existing checkout. With web access alone, the agent can read the public wiki.

### Use an instruction file

For an agent that reads project instructions, clone the wiki once.

```sh
git clone https://github.com/mishaevoma/aie-brain ~/.aie-brain
```

Add this line to the project's `AGENTS.md` or the instruction file your agent reads.

```markdown
For an AI engineering question or project review, follow ~/.aie-brain/.agents/skills/brain-consult/SKILL.md.
```

If your team already includes the wiki as a submodule, use its project-relative path in that line.

## What it is for

1. **Building.** Turn what the best practitioners publish into concrete decisions when designing an agent, a tool, an eval or a harness.
2. **Staying current.** Give a coding agent dated, sourced practices instead of whatever its training data happened to contain.
3. **A shared vocabulary.** When a person and their AI tools say "harness", "skill" or "context engineering", they mean the same thing, at the same level of abstraction.

## Where to start

| If you want | Open |
|---|---|
| The big picture in five minutes | [overview.md](overview.md) |
| What a term means here | [glossary.md](glossary.md) |
| Everything, one line per page | [index.md](index.md) |
| A step-by-step guide | [playbooks/](playbooks/) |

## How it is organised

```
AGENTS.md      rules for agents working here (CLAUDE.md imports it)
index.md       every page in one line, and "By decision": from a question to its pages
overview.md    the stack, consensus, live debates, gaps
glossary.md    the shared vocabulary
concepts/      one page per idea, every claim linked to a source note
playbooks/     task-shaped guides built from the concepts
sources/       one note per source: our own summary plus the link
considered.md  sources that were looked at and left out, with the reason
raw/           local full-text captures (gitignored)
log.md         what was ingested and changed, and when
watchlist.md   where new material comes from
tools/lint.py  checks, generated parts and log entries
.agents/skills procedures: consult, ingest, lint, refresh
site/          website build: Quartz settings and two scripts
```

This is the LLM wiki pattern: raw sources, a wiki the agent owns, and a schema file that tells it how to maintain the wiki. See [concepts/llm-wiki.md](concepts/llm-wiki.md).

## Using it

**Ask it a question.** Ask from any project where the brain is installed, or open this folder in a coding agent and ask. The agent reads `index.md`, then the pages that fit, and answers with citations. The `brain-consult` skill describes how.

**Review a design.** Give the agent a design document or a planned change and ask for a review. It compares the decisions in the plan against the relevant playbook, identifies trade-offs, and tells you what evidence would resolve an open question.

**Cite it.** The brain changes. An answer that will be kept should name the version it read, which `git log -1 --format='%h %cs'` prints.

**Add a source.** Give the agent a link, or drop a file into `raw/`, and say "ingest this". It writes the source note, updates every page the source touches, and logs the change (`brain-ingest`).

**Keep it fresh.** Ask "what's new?" and the agent checks the watchlist and proposes what to ingest (`brain-refresh`). What it looks at and leaves out goes into `considered.md`, so nothing is weighed twice. Ask it to lint and it looks for broken links, stale pages and contradictions (`brain-lint`).

**Read it yourself.** On the website, https://mishaevoma.github.io/aie-brain/, which has search, backlinks and previews of cited sources. Or on GitHub, or by opening the folder as an Obsidian vault.

**Read it without cloning.** An agent that can only fetch web pages starts at https://mishaevoma.github.io/aie-brain/llms.txt. Every page is also served as raw markdown at its address plus `.md`.

## What is in it

Seeded on 17 November 2026 with 50 sources: all 29 articles on Anthropic's engineering blog, plus 21 articles, posts and one video from Addy Osmani, Boris Cherny, Theo Browne, Dan Shipper, Harrison Chase, Andrej Karpathy, Google, Red Hat, Loams and others. Nine sources from outside Anthropic were added next: Chip Huyen, HumanLayer's 12-factor agents, Cognition, Drew Breunig, Simon Willison, Chroma, and Hamel Husain with Shreya Shankar. From all of these: 21 concept pages, 3 playbooks, and a glossary of about 90 terms.

## What to keep in mind

- **Summaries, not copies.** The sources are other people's copyrighted work and this repository is public. Each note is a short summary in our own words with a link. Read the original for anything that matters.
- **Models wrote this.** Source notes were written by AI agents, most of them reading articles through a fetch tool, with two passes per article. Each note says how much of the original it is based on. Check numbers against the original before you rely on them.
- **It has a slant.** About half of the sources are Anthropic's, and several of the others come from people who build on Claude. The gaps are listed at the end of [overview.md](overview.md).
- **It dates quickly.** Every source note carries its publication date and every concept page the date it was last updated. `python3 tools/lint.py --ages` shows which pages rest on old sources.

## Checks

```bash
python3 tools/lint.py
```

Standard library only. Add `--sync` to regenerate the source list in `index.md` and the backlinks in source notes. Add `--log "ingest | Title"` to append the `log.md` entry once the checks pass.

The lint enforces the freshness rules: every "What to do" bullet cites a source note, every citation shows the note's publication date, and pages that have not been reviewed for 120 days are flagged.

```bash
python3 tools/lint.py --ages
```

Prints, for each concept page and playbook, how many of its cited lines rest only on sources older than a year, with the oldest and newest source date. Every page carries the date it was last edited, which says nothing about how old its evidence is. This report does.

## Licence

MIT, see [LICENSE](LICENSE). It covers this repository's own text and code. The articles, posts and videos that the source notes summarise and link to remain their authors' work.
