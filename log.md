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

## [2026-11-17] edit | Install in one line, MIT licence, social preview image

- LICENSE
- README.md
- .agents/skills/brain-consult/SKILL.md
- .agents/skills/brain-consult/brain-root.sh
- .github/social-preview.html
- .github/social-preview.png
- tools/lint.py

The README now opens with the install: `git clone` into `~/.aie-brain` plus one line for `AGENTS.md`, then `npx skills add mishaevoma/aie-brain`. `brain-root.sh` clones the brain on first use, into `~/.aie-brain` or into `AIE_BRAIN`, and brings that copy up to date at most once a day. Files use the repository's new name, `aie-brain`.

- Checked: the script in a throwaway home under three shells (33 checks), and one first use by a fresh agent that had only the installed skill folder. Its remarks on wording went into `SKILL.md`.
- Not checked: `npx skills add` itself was not run. The skill folder was compared with the installer's own rules instead.

## [2026-11-17] ingest | Nine sources from outside Anthropic

- README.md
- glossary.md
- index.md
- overview.md
- watchlist.md
- concepts/ (15 files)
- playbooks/building-an-agent-product.md
- sources/ (9 files)

- The notes: Chip Huyen on agents (January 2025), 12-factor agents (March 2025), Hamel Husain's field guide (March 2025) and the FAQ entry on error analysis he wrote with Shreya Shankar (June 2025), Cognition against multi-agent designs (June 2025), Simon Willison on the lethal trifecta and on the term context engineering (June 2025), Drew Breunig on fixing a context (June 2025), and Chroma's context rot report (July 2025).
- How they were read: all nine in full, from saved copies of the pages. Five by the maintaining agent. Four long ones by reader agents with a second pass over every figure, after which the maintaining agent checked a sample of each note's figures against the saved text. Charts were not visible in the saved copies, so the Chroma note gives directions and the few rates stated in prose.
- Disagreements now recorded side by side: one agent or several (`concepts/multi-agent-systems.md`), adopt a harness or own the loop (`concepts/harness.md`), fix eval criteria first or let them emerge (`concepts/eval-validity.md`), where evals start and what a grader returns (`concepts/evals.md`), what counts as an agent (`concepts/agents-and-workflows.md`), and a small corpus sent whole against selection (`concepts/retrieval.md`).
- One new page, `concepts/error-analysis.md`, since the idea has a name and two notes behind it and would have overgrown the evals page. `concepts/evals.md` moved from `settled` to `evolving`. "An existing harness before your own" left the list of what the sources agree on in `overview.md` and became a live debate.
- Anthropic now accounts for 29 of 59 sources. All nine additions are older than a year, so `--ages` went from 81 of 384 cited lines resting only on old sources to 148 of 454.

## [2026-11-18] ingest | Agent platforms and durable runtimes (79 sources)

- considered.md
- glossary.md
- index.md
- overview.md
- watchlist.md
- concepts/ (16 files)
- playbooks/building-an-agent-product.md
- sources/ (80 files)

Research into how agents run in production, as of November 2026: durable execution, agent platforms, managed runtimes, background agents, identity and tenancy. About 600 pages were captured in six discovery passes; 79 became source notes and 49 went to `considered.md` with a reason. 78 notes rest on a full reading of the source, most of them from a saved capture, and one on part of a specification. 52 were drafted by subagents and checked by the session that wrote this entry, and a script compared each note's figures, date and authors with the capture and looked for copied runs of nine or more words. Six reviewers then checked every cited line of the new and edited pages against its notes, and their 87 findings were applied: mostly figures without the company they were measured at, dropped qualifiers, and two vendors' advice merged into one. Undated documentation is dated by the day it was read, 17 November 2026, and says so under Caveats.

- New concept pages: agent platforms, durable execution, side effects and approvals, managed agent runtimes, background agents, agent identity and tenancy.
- Edited: harness, agents and workflows, verification, long-running agents, running agents in production, permissions and sandboxing, multi-agent systems, human judgment, MCP, memory. The product playbook gains a step, "Decide where it runs".
- `overview.md`: a sixth layer for the agent platform, two items of consensus, three live debates, additions to the timeline, and a revised list of gaps. `glossary.md`: 37 terms. `watchlist.md`: feeds, open leads and gaps for this area.
- Left open: eleven concept pages are over the guide of about 600 words, the longest about 810.

## [2026-11-18] edit | Launch a sourced project review from a URL or an installed skill

- AGENTS.md
- README.md
- index.md
- .agents/skills/brain-consult/SKILL.md
- .agents/skills/brain-consult/brain-root.sh
- .agents/skills/brain-consult/references/project-review.md
- site/agentfiles.py

## [2026-11-18] edit | Check the public review entry point before merge

- README.md
- .github/workflows/lint.yml
- site/test_review_publication.py

## [2026-11-18] edit | Show the first review and put the change beside its check

- README.md
- .agents/skills/brain-consult/references/project-review.md

## [2026-11-19] edit | Project review shows what to upgrade, with an eval suite

- AGENTS.md
- README.md
- index.md
- .agents/skills/brain-consult/SKILL.md
- .agents/skills/brain-consult/references/project-review.md
- .github/review-demo.gif
- evals/ (120 files)
- playbooks/upgrading-an-agent-app.md
- site/agentfiles.py
- site/quartz.config.yaml
- site/test_review_publication.py
- tools/lint.py

## [2026-11-19] edit | Scorecard from the published review, with the README example and GIF from that run

- README.md
- .github/review-demo.gif
- evals/ (32 files)

## [2026-11-19] edit | Demo GIF shows three real upgrades, with a memory fixture behind the third

- README.md
- .github/review-demo.gif
- evals/ (11 files)

## [2026-11-19] edit | Demo GIF names the primitive and the gist of each upgrade

- README.md
- .github/review-demo.gif
- evals/README.md
- evals/demo/demo.html
- evals/demo/make_gif.py
- evals/demo/showcases.json

## [2026-11-19] edit | Drop the review demo GIF

- README.md
- .github/review-demo.gif
- evals/README.md
- evals/demo/demo.html
- evals/demo/make_gif.py
- evals/demo/showcases.json

## [2026-11-19] edit | README shows the concept graph as a dependency wheel

- README.md
- .github/knowledge-graph.gif
- evals/README.md
- site/graph_gif.html
- site/graph_gif.py

## [2026-11-22] ingest | How to build a knowledge factory

- glossary.md
- index.md
- overview.md
- watchlist.md
- .github/knowledge-graph.gif
- concepts/compounding.md
- concepts/context-layer.md
- concepts/knowledge-factory.md
- concepts/llm-wiki.md
- concepts/memory.md
- concepts/retrieval.md
- concepts/skills.md
- sources/ (9 files)

## [2026-11-22] edit | Link directly to original sources from GitHub Pages

- index.md
- site/agentfiles.py
- site/quartz.config.yaml
- tools/lint.py

## [2026-11-22] ingest | Agent platform of 2027

- glossary.md
- index.md
- overview.md
- watchlist.md
- concepts/ (11 files)
- playbooks/building-an-agent-product.md
- sources/2025-03-30-humanlayer-12-factor-agents.md
- sources/2026-04-07-harvey-building-spectre.md
- sources/2026-07-27-rivet-harness-outside-the-sandbox.md
- sources/2026-11-12-openai-securing-persistent-agents.md
- sources/2026-11-17-langchain-proactive-agents.md
- sources/2026-11-22-suh-agent-platform-2027.md
