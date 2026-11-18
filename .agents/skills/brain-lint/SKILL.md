---
name: brain-lint
description: Health-check the AI engineering brain. Finds broken links, pages missing from the index, stale or contradictory pages, glossary terms that drifted, and claims without sources. Use when the user asks to lint, check, audit or clean up the brain, before committing a batch of changes, and after any large ingest.
metadata:
  internal: true
---

# Lint the brain

## 1. Mechanical checks

Run `python3 tools/lint.py --sync` from the brain's root. Fix every error. Read every warning and either fix it or note why it stands. The top of `tools/lint.py` lists what it checks.

`--sync` rewrites the generated parts: each source note's `concepts:` list and the source list in `index.md`. Never edit those by hand.

## 2. Checks that need judgement

- **Pages flagged as not reviewed, or resting on old sources.** Run `python3 tools/lint.py --ages`. It lists, for each page, how many cited lines rest only on sources older than a year, with the oldest and newest source date. For each page the script flags, and for the pages at the top of that list, re-read the page against the recent notes on its topic, fix what no longer holds, then set `reviewed:` to today. Do not set it without re-reading. Where no newer source exists, say on the page that the advice is old, and add the topic to `watchlist.md`.
- **Contradictions.** Two pages that state opposite things without marking the disagreement.
- **Unsupported claims.** A sentence outside "What to do" with a number or a strong claim and no link to a source note. Synthesis is allowed when it is labelled as this brain's reading.
- **Missing pages.** A term used on three or more pages with no glossary entry, or an idea several sources share that has no concept page.
- **Glossary drift.** A glossary line that no longer matches the definition at the top of its concept page.
- **Overgrown pages.** A concept page past about 600 words of prose: tighten or split it. `AGENTS.md` past 80 lines: move procedure into a skill.
- **Partly read sources.** Notes marked `read: partial` or `summary-only`: finish reading them if the original is now reachable.
- **Overview and routing.** Does `overview.md` still describe what the concept pages say? Does "By decision" in `index.md` still point to the right pages?
- **The ledger.** Is anything in `considered.md` now worth ingesting because the brain's scope has grown?

## 3. Spot-check the facts

Pick three numbers from concept pages and confirm each in its source note. Pick one source note and confirm two of its claims against the original.

## 4. Report and log

Fix what is mechanical. List what needs the owner's decision. Then run `python3 tools/lint.py --sync --log "lint | <one-line result>"`.
