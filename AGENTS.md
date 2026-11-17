# AI Engineering Brain

A wiki of current practice for building AI products. Agents write and maintain it. The owner and their agents read it.

## Mission

1. Help the owner build AI products: turn current practice into concrete decisions.
2. Keep the working agent current, with dated and sourced practices and concepts.
3. Be the shared vocabulary between the owner and their AI coding tools, at the level of ideas and trade-offs.

## Layout

| Path | Holds | Rule |
|---|---|---|
| `index.md` | Every page, one line each, and a table from decisions to pages | Read first |
| `overview.md` | The stack, consensus, live debates, gaps | Update when the picture changes |
| `glossary.md` | One line per term | Use these terms as defined |
| `concepts/` | One page per idea | Every claim links to a source note |
| `playbooks/` | Task-shaped guides | Built from concept pages |
| `sources/` | One note per source: our summary plus the link | Named `YYYY-MM-DD-who-slug.md` |
| `considered.md` | Sources looked at and left out, with the reason | Check it before proposing a source |
| `raw/` | Local full-text captures, gitignored | Read-only for agents |
| `log.md` | Append-only history | Written by `tools/lint.py --log` |
| `watchlist.md` | Feeds, people and open leads | Update on refresh |
| `tools/lint.py` | Checks, generated parts, log entries | Run before every commit |

## Reading

- Reading is read-only. Change the brain only when asked to ingest, lint or refresh it, or when the owner agrees to an edit.
- Route by the decision at hand. Go from the table in `index.md` to a concept page or playbook, then to a source note, then to the original URL. Stop as soon as you can answer. Do not preload the wiki.
- Cite the pages you used and give the date of anything time-sensitive. This field changes monthly.
- A newer source outweighs an older one unless the page says otherwise. Check a page's `status` (`settled`, `evolving`, `contested`) before relying on it.
- If the brain is silent or out of date, say so. Do not fill the gap from memory without labelling it.
- Use glossary terms as defined. If the owner uses a term differently, point it out and reconcile.

## Writing

- Your own words only. Sources are other people's copyrighted work and this repository is public: summarise and link, never copy. Coined terms and short phrases are fine.
- Keep numbers, product names and technique names exact, and rely only on what you actually read.
- Cite as `[Short title, Mon YYYY](../sources/file.md)`, so the date of every claim is visible.
- Record disagreement side by side with dates. Do not overwrite one position with another.
- Keep concept pages at the level of ideas, trade-offs and decisions. Version-specific detail belongs in source notes.
- Label synthesis that goes beyond the sources as this brain's reading.
- Pages carry two dates. `updated:` changes with any edit. `reviewed:` changes only when you have re-read the whole page against the newest sources on its topic.
- After any change, add new pages to `index.md` and run `python3 tools/lint.py --sync --log "<operation> | <title>"`. It regenerates the generated parts, runs the checks and writes the `log.md` entry. Fix what it reports.
- Plain markdown, relative links, kebab-case filenames. Keep this file under 80 lines; procedures go in skills.

## Skills

Procedures live in `.agents/skills/` (linked from `.claude/skills/`) and load when needed.

- `brain-consult`: answer a question or review a plan against the brain. Read-only, and installable in other projects.
- `brain-ingest`: add a source and fold it into the wiki, or record that it adds nothing.
- `brain-lint`: health check, mechanical and by judgement.
- `brain-refresh`: look for new material from the watchlist.
