# Log

Append-only, newest at the bottom. Every entry starts with `## [YYYY-MM-DD] operation | title`, so `grep "^## \[" log.md | tail` shows recent activity. Operations: `init`, `ingest`, `lint`, `refresh`, `edit`.

Entries are written by `python3 tools/lint.py --sync --log "operation | title"`, which lists the files changed since the last commit. Add a line of explanation under an entry by hand when the title is not enough.

## [2026-11-17] init | Repository created

Structure, schema (`AGENTS.md`), four skills (`brain-consult`, `brain-ingest`, `brain-lint`, `brain-refresh`) and `tools/lint.py`.

## [2026-11-17] ingest | Seed: 50 sources

- 29 Anthropic engineering articles, September 2024 to November 2026: every article listed on anthropic.com/engineering on this date.
- 6 other articles: Red Hat, Google, Loams, t3.gg, Every Frontier, and Karpathy's idea file.
- 4 X articles (Osmani twice, Chase twice), 10 X posts, 1 video.
- Read levels: 48 full, 2 partial (the GBrain post and the Every post, where only the post text was read).
- How they were read: web articles through a fetch tool by reader agents, two passes each. X posts, X articles and the video transcript in a browser.
- Compiled from them: 20 concept pages, 3 playbooks, the glossary and the overview.

## [2026-11-17] lint | Seed check

- `tools/lint.py --sync` passes with no errors and no warnings. It checks, among other things, that every figure on a cited line appears in a source note that line cites.
- Spot check against originals: 33 claims from five Anthropic notes (infrastructure noise, agent memory, auto mode, containment, demystifying evals) were re-checked against the articles. 31 confirmed and one was a badly worded check. One was overstated and has been corrected: the containment note said all three pre-trust bugs were settings-file hooks, where the article says only the most direct one was.
- Not checked against originals: the other 28 article notes beyond the readers' own two passes.

## [2026-11-17] edit | Freshness lint, log command, ledger, decision table, installable consult skill

- AGENTS.md
- README.md
- considered.md
- index.md
- .agents/skills/brain-consult/SKILL.md
- .agents/skills/brain-consult/brain-root.sh
- .agents/skills/brain-ingest/SKILL.md
- .agents/skills/brain-ingest/concept-template.md
- .agents/skills/brain-lint/SKILL.md
- .agents/skills/brain-refresh/SKILL.md
- concepts/ (20 files)
- playbooks/building-an-agent-product.md
- playbooks/reviewing-agent-work.md
- playbooks/setting-up-a-repo-for-coding-agents.md
- tools/lint.py
