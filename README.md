# ai-engineering-brain

A wiki of current practice for building AI products, written and maintained by AI agents and read by both agents and people.

It exists for three things:

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
index.md       every page, one line each
overview.md    the stack, consensus, live debates, gaps
glossary.md    the shared vocabulary
concepts/      one page per idea, every claim linked to a source note
playbooks/     task-shaped guides built from the concepts
sources/       one note per source: our own summary plus the link
raw/           local full-text captures (gitignored)
log.md         what was ingested and changed, and when
watchlist.md   where new material comes from
tools/lint.py  mechanical health checks
.agents/skills procedures: consult, ingest, lint, refresh
```

This is the LLM wiki pattern: raw sources, a wiki the agent owns, and a schema file that tells it how to maintain the wiki. See [concepts/llm-wiki.md](concepts/llm-wiki.md).

## Using it

**Ask it a question.** Open this folder in a coding agent and ask. The agent reads `index.md`, then the pages that fit, and answers with citations. The `brain-consult` skill describes how.

**Review a design.** Ask the agent to review an architecture or a repository setup against the brain. It walks the matching playbook step by step and says, for each step, whether the design agrees with the brain, falls short of it, or lies outside what the brain covers (`brain-consult`, "Review a whole design").

**Use it from another project.** Either add the folder to a session:

```bash
claude --add-dir /path/to/ai-engineering-brain
```

or install the consult skill for every session. The skill finds the brain through the link:

```bash
ln -s /path/to/ai-engineering-brain/.agents/skills/brain-consult ~/.claude/skills/brain-consult
```

For tools without skills, add one line to that project's `AGENTS.md`: "For anything involving LLMs or agents, consult the AI engineering brain at /path/to/ai-engineering-brain, starting at index.md."

Nothing has to be installed. An agent that is only given this repository's address can clone it, read `AGENTS.md`, then `index.md`, and follow `.agents/skills/brain-consult/SKILL.md` as written. If the skill folder was copied instead of linked, set `AIE_BRAIN` to the clone so the skill can find it.

**Cite it.** The brain changes. An answer that will be kept should name the version it read, which `git log -1 --format='%h %cs'` prints.

**Add a source.** Give the agent a link, or drop a file into `raw/`, and say "ingest this". It writes the source note, updates every page the source touches, and logs the change (`brain-ingest`).

**Keep it fresh.** Ask "what's new?" and the agent checks the watchlist and proposes what to ingest (`brain-refresh`). Ask it to lint and it looks for broken links, stale pages and contradictions (`brain-lint`).

**Read it yourself.** On GitHub, or open the folder as an Obsidian vault.

## What is in it

Seeded on 17 November 2026 with 50 sources: all 29 articles on Anthropic's engineering blog, plus 21 articles, posts and one video from Addy Osmani, Boris Cherny, Theo Browne, Dan Shipper, Harrison Chase, Andrej Karpathy, Google, Red Hat, Loams and others. From these: 20 concept pages, 3 playbooks, and a glossary of about 80 terms.

## What to keep in mind

- **Summaries, not copies.** The sources are other people's copyrighted work and this repository is public. Each note is a short summary in our own words with a link. Read the original for anything that matters.
- **Models wrote this.** Source notes were written by AI agents, most of them reading articles through a fetch tool, with two passes per article. Each note says how much of the original it is based on. Check numbers against the original before you rely on them.
- **It has a slant.** Most sources come from Anthropic or from people who build on Claude. The gaps are listed at the end of [overview.md](overview.md).
- **It dates quickly.** Every source note carries its publication date and every concept page the date it was last updated. `python3 tools/lint.py --ages` shows which pages rest on old sources.

## Checks

```bash
python3 tools/lint.py
```

Standard library only. Add `--sync` to regenerate the source list in `index.md` and the backlinks in source notes.

```bash
python3 tools/lint.py --ages
```

Prints, for each concept page and playbook, how many of its cited lines rest only on sources older than a year, with the oldest and newest source date. Every page carries the date it was last edited, which says nothing about how old its evidence is. This report does.
