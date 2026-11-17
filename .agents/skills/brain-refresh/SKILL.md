---
name: brain-refresh
description: Look for new material for the AI engineering brain from its watchlist of blogs and people and from its open leads, then propose what to ingest. Use when the user asks what is new, asks to refresh or update the brain, or when the newest source note is more than about two weeks old.
---

# Refresh the brain

## 1. Find the starting point

Read `watchlist.md`. Find the last `refresh` or `ingest` entry in `log.md` (`grep "^## \[" log.md | tail`). Everything published after that date is a candidate.

## 2. Collect candidates

- Check each feed and person on the watchlist for items since that date. X needs a real browser.
- Check the open leads: things earlier sources cited that have not been ingested.
- Skip anything already in `sources/` (search for the URL).

## 3. Rank

Keep an item if it changes a practice, defines a term the brain uses, adds evidence, or contradicts a page. Drop announcements with no content, reposts, and takes that add nothing to an existing note.

Run `python3 tools/lint.py --ages` and look at the pages whose advice rests mostly on old sources. An item that brings newer evidence to one of them ranks above one that adds to a page already well sourced. So does an item that fills a gap listed in `watchlist.md`.

## 4. Propose

Show the owner the shortlist: title, author, date, link and one line on why it earns a place. Ingest only what they approve, one source at a time, with `brain-ingest`. If the owner has asked for unattended refresh, ingest the top items and report afterwards.

## 5. Record

Update the "last checked" date in `watchlist.md`, remove leads that are now ingested, add new ones, and append `## [YYYY-MM-DD] refresh | <n> candidates, <m> ingested` to `log.md`.
