# AI Engineering Brain

A wiki of current practice for building AI products. Agents write and maintain it. The owner and their agents read it.

## Mission

1. Help the owner build AI products: turn current practice into concrete decisions.
2. Keep the working agent current, with dated and sourced practices and concepts.
3. Be the shared vocabulary between the owner and their AI coding tools, at the level of ideas and trade-offs.

## Layout

| Path | Holds | Rule |
|---|---|---|
| `index.md` | Every page, one line each | Read first |
| `overview.md` | The stack, consensus, live debates, gaps | Update when the picture changes |
| `glossary.md` | One line per term | Use these terms as defined |
| `concepts/` | One page per idea | Every claim links to a source note |
| `playbooks/` | Task-shaped guides | Built from concept pages |
| `sources/` | One note per source: our summary plus the link | Named `YYYY-MM-DD-who-slug.md` |
| `raw/` | Local full-text captures, gitignored | Read-only for agents |
| `log.md` | Append-only history | Add an entry for every ingest, lint and refresh |
| `watchlist.md` | Feeds, people and open leads | Update on refresh |
| `tools/lint.py` | Mechanical checks | Run before every commit |

## Reading

- Go from `index.md` to a concept page or playbook, then to a source note, then to the original URL. Stop as soon as you can answer.
- Cite the pages you used and give the date of anything time-sensitive. This field changes monthly.
- A newer source outweighs an older one unless the page says otherwise. Check a page's `status` (`settled`, `evolving`, `contested`) before relying on it.
- If the brain is silent or out of date, say so. Do not fill the gap from memory without labelling it.
- Use glossary terms as defined. If the owner uses a term differently, point it out and reconcile.

## Writing

- Your own words only. Sources are other people's copyrighted work and this repository is public: summarise and link, never copy. Coined terms and short phrases are fine.
- Keep numbers, product names and technique names exact, and rely only on what you actually read.
- Say whose models or product a figure was measured on, on the concept page and not only in the source note.
- Nothing from a private project goes in. This repository is public: record what a consult taught you in general terms, with no names, architecture or data from the project.
- Record disagreement side by side with dates. Do not overwrite one position with another.
- Keep concept pages at the level of ideas, trade-offs and decisions. Version-specific detail belongs in source notes.
- Label synthesis that goes beyond the sources as this brain's reading.
- On any change: bump `updated:`, add new pages to `index.md`, append to `log.md`, then run `python3 tools/lint.py --sync` and fix what it reports.
- Plain markdown, relative links, kebab-case filenames. Keep this file under 80 lines; procedures go in skills.

## Skills

Procedures live in `.agents/skills/` (linked from `.claude/skills/`) and load when needed.

- `brain-consult`: answer a question, or review a plan or a whole design, against the brain.
- `brain-ingest`: add a source and fold it into the wiki.
- `brain-lint`: health check, mechanical and by judgement.
- `brain-refresh`: look for new material from the watchlist.
