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

## [2026-11-17] edit | Changes after the first review of a whole design

An agent used the brain to review a product design end to end and reported what made the brain hard to use. These edits answer that report. Nothing about the design itself is recorded here.

- `brain-consult`: a procedure for reviewing a whole design by walking a playbook, with a verdict of aligned, gap or silent for each step. It also says where each kind of give-back goes, asks for the brain's version in answers that will be kept, and says how to use the brain when it is not on the machine. `brain-root.sh` reads `AIE_BRAIN` and fails with instructions when it finds no brain.
- `index.md`: a "By decision" section, from a question to the pages that answer it, split into building a product and setting up coding agents.
- `concepts/retrieval.md`, `concepts/context-engineering.md`: the 2024 advice to put a small corpus whole into a cached prompt and the 2025 and 2026 advice to load on demand now stand side by side, followed by this brain's reading of when each applies.
- Whose models a figure comes from: a rule in `AGENTS.md`, applied to lines on `concepts/memory.md`, `concepts/tool-design.md`, `concepts/retrieval.md`, `concepts/multi-agent-systems.md` and `concepts/sandboxing-and-permissions.md`, and said once for the whole brain in `overview.md`.
- `tools/lint.py --ages`: for each concept page and playbook, how many cited lines rest only on sources older than a year, with the oldest and newest source date. `brain-lint` and `brain-refresh` now use it.
- `overview.md`, `watchlist.md`: four gaps the review exposed: durable execution, serving many customers, model gateways, and agents that operate an application's interface.
- `AGENTS.md`: nothing from a private project goes into this repository.
- `README.md`: reviewing a design, using the brain without installing it, citing the version read.
- Considered and left out: a folder for filed answers. Most answers are about a private project, and the general part of an answer already has a home: a concept page, a playbook, or the lists of gaps.

## [2026-11-17] lint | After the edit

- `tools/lint.py --sync` passes with no errors and no warnings. It moved one backlink: the contextual retrieval note is now also used by the context engineering page.
- `--ages` at its default of 365 days: 81 of 384 cited lines rest only on sources older than a year. Tool design (11 of 16 lines) and context engineering (10 of 17) lean on old sources the most.
- The figures on the edited lines were confirmed in their source notes. They were not checked again against the original articles.

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

Built in parallel with the edit above, from the same starting point, and merged with it afterwards. Where both had built the same thing, the names already published were kept: the `AIE_BRAIN` variable, the "By decision" section of `index.md` (it took over the rows of this change's decision table), and `--ages` with `--old-days` in the lint. `--old-days` now also sets the age at which a concept page whose newest source is old raises a warning.
