# AI Engineering Brain

A wiki of current practice for building AI products, written and maintained by AI agents and read by both agents and people. Every claim links to a dated source.

## Install

Clone it, then add one line to `AGENTS.md`. This works in any coding agent that reads an instruction file and can open files: Codex, Cursor, OpenCode, Claude Code and others.

```bash
git clone https://github.com/mishaevoma/aie-brain ~/.aie-brain
```

```markdown
For anything involving LLMs or agents, consult the AI engineering brain: follow ~/.aie-brain/.agents/skills/brain-consult/SKILL.md.
```

The line can go in one project's `AGENTS.md` or in your agent's global instruction file. As of November 2026, Claude Code reads `AGENTS.md` only in a project that has no `CLAUDE.md`. Where there is one, put the line there.

Or install the consult skill and let it fetch the wiki:

```bash
npx skills add mishaevoma/aie-brain
```

The [`skills`](https://github.com/vercel-labs/skills) installer asks which agents to set up, then copies `brain-consult` into the skill folder of each. Add `-g` to install it for every project. The first time the skill runs, it clones this repository into `~/.aie-brain`.

Either way, the skill brings the copy in `~/.aie-brain` up to date when it runs, at most once a day. Set `AIE_BRAIN` to keep the brain somewhere else, or to point the skill at a clone you maintain yourself, which it never touches.

Then ask your agent "what does the brain say about evals?" or "review this design against the brain".

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

**Review a design.** Ask the agent to review an architecture or a repository setup against the brain. It walks the matching playbook step by step and says, for each step, whether the design agrees with the brain, falls short of it, or lies outside what the brain covers (`brain-consult`, "Review a whole design").

**Connect it another way.** Link the consult skill from a clone instead of copying it, and one `git pull` updates the skill and the wiki together:

```bash
ln -s ~/.aie-brain/.agents/skills/brain-consult ~/.claude/skills/brain-consult
```

In Claude Code, `claude --add-dir ~/.aie-brain` adds the folder to a single session. And nothing has to be installed at all: an agent that is only given this repository's address can clone it, read `AGENTS.md`, then `index.md`, and follow `.agents/skills/brain-consult/SKILL.md` as written.

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
