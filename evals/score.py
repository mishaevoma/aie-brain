#!/usr/bin/env python3
"""Check the reviews of one run and write the scorecard.

A person, or an agent that did not write the reviews, grades each finding by hand in
<run>/scores.csv. This script does the parts a machine can do and puts the two together.

  python3 evals/score.py evals/runs/<run>
      Print the mechanical checks for every review in the run.
  python3 evals/score.py evals/runs/<run> --write
      Also write evals/scorecard.md from the checks, <run>/scores.csv and <run>/smoke.csv.

Mechanical checks, per review:
  links       every link to this wiki leads to a page that exists in this checkout
  chain       every cited source note comes with its original publication, and a wiki page
  ages        how old each cited source note is, and whether one older than --old-days is
              labelled as older in the paragraph that cites it
  locations   file:line references point at lines that exist in the fixture
  parts       the labelled parts a finding must carry are present (see evals/README.md)
  tree, time  taken from meta.json, as run.py recorded them

scores.csv has one row per finding: fixture, finding, ids, specific, correct, cited, fresh,
verifiable, actionable, note. Each dimension is 0, 1 or 2. `ids` holds the expected.md IDs the
finding matches, separated by spaces. A review with no finding has no row.

smoke.csv has one row per one-paste smoke check on another agent: agent, model, fixture,
started_without_questions (yes, no, or "not run" for an agent still owed), first_finding_seconds, note.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "evals" / "fixtures"
SITE = "https://mishaevoma.github.io/aie-brain/"
GITHUB = re.compile(r"https://(?:raw\.githubusercontent\.com/mishaevoma/aie-brain/|github\.com/mishaevoma/aie-brain/(?:blob|tree)/)[^/]+/")
URL = re.compile(r"https?://[^\s)>\]\"'`]+")
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
WIKI_PATH = re.compile(r"(?:^|[\s(`/])((?:concepts|playbooks|sources)/[a-z0-9-]+\.md)")
LOCATION = re.compile(r"([\w./-]+\.(?:py|md|csv|json|toml|yml|yaml|txt)|Makefile):(\d+)")
OLDER = re.compile(r"\bolder\b|still (?:valid|holds|applies|current)|months old|year[s]? old|over (?:six|twelve|12) months", re.I)
DIMENSIONS = ["specific", "correct", "cited", "fresh", "verifiable", "actionable"]
PARTS = {
    "change": re.compile(r"\*\*[^*\n]*Change", re.I),
    "why": re.compile(r"\*\*[^*\n]*Why", re.I),
    "check": re.compile(r"\*\*[^*\n]*Check", re.I),
    "evidence age": re.compile(r"\*\*[^*\n]*Evidence", re.I),
    "effort and impact": re.compile(r"\*\*[^*\n]*Effort", re.I),
    "next step": re.compile(r"make (?:the|that|this) change|run the check|apply (?:it|the change)", re.I),
    "install offer": re.compile(r"npx skills add mishaevoma/aie-brain"),
    "provenance": re.compile(r"wiki revision|published (?:copy|wiki|AI Engineering Brain)|consulted", re.I),
    "says upgrade": re.compile(r"\bupgrade", re.I),
}


def wiki_file(target: str) -> str | None:
    """The path inside this wiki that a link or URL points at, or None when it points elsewhere."""
    target = target.split("#")[0].split("?")[0]
    if target.startswith(SITE):
        path = target[len(SITE):]
    elif GITHUB.match(target):
        path = GITHUB.sub("", target)
    elif str(ROOT) in target:
        path = target.split(str(ROOT), 1)[1].lstrip("/")
    else:
        found = WIKI_PATH.search(" " + target)
        if target.startswith("http") or not found:
            return None
        path = found.group(1)
    path = path.strip("/")
    if path and "." not in path.rsplit("/", 1)[-1]:
        path += ".md"  # a rendered page address, without its extension
    return path


def source_facts(path: str) -> tuple[dt.date | None, str | None]:
    """Publication date and original URL of a source note."""
    text = (ROOT / path).read_text(encoding="utf-8")
    published = re.search(r"^published:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    url = re.search(r"^url:\s*\"?([^\"\n]+)\"?", text, re.M)
    return (dt.date.fromisoformat(published.group(1)) if published else None, url.group(1).strip() if url else None)


def same_page(a: str, b: str) -> bool:
    strip = lambda u: re.sub(r"^https?://(www\.)?", "", u).rstrip("/").lower()
    return strip(a) == strip(b)


def check_review(folder: Path, old_days: int) -> dict:
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    text = (folder / "review.md").read_text(encoding="utf-8")
    on = dt.date.fromisoformat(meta["date"])
    fixture = FIXTURES / meta["fixture"]
    paragraphs = re.split(r"\n\s*\n", text)

    targets = set(MD_LINK.findall(text)) | set(URL.findall(text)) | {m.group(1) for m in WIKI_PATH.finditer(text)}
    wiki = {t: wiki_file(t) for t in targets}
    pages = sorted({p for p in wiki.values() if p})
    broken = sorted(p for p in pages if not (ROOT / p).is_file())
    notes = [p for p in pages if p.startswith("sources/") and p not in broken]
    outside = [t for t, p in wiki.items() if p is None and t.startswith("http")]

    sources = []
    for note in notes:
        published, original = source_facts(note)
        age = (on - published).days if published else None
        citing = [para for para in paragraphs if any(wiki.get(t) == note for t in targets if t in para)]
        sources.append({
            "note": note,
            "published": published.isoformat() if published else None,
            "age_days": age,
            "old": age is not None and age > old_days,
            "labelled_older": any(OLDER.search(para) for para in citing),
            "original_given": bool(original) and any(same_page(original, link) for link in outside),
        })
    originals_without_note = [
        link for link in outside
        if not any(s["original_given"] and same_page(source_facts(s["note"])[1] or "", link) for s in sources)
        and "mishaevoma" not in link
    ]

    locations = []
    for name, line in LOCATION.findall(text):
        name = name.split(fixture.name + "/")[-1]  # an absolute path into the fixture copy
        candidates = [p for p in fixture.rglob(Path(name).name) if p.as_posix().endswith(name.lstrip("./"))]
        ok = any(int(line) <= len(p.read_text(encoding="utf-8").splitlines()) for p in candidates)
        locations.append((f"{name}:{line}", ok))

    return {
        "fixture": meta["fixture"],
        "agent": meta["agent"],
        "model": meta["model"],
        "via": meta["via"],
        "seconds_to_review": meta["seconds_to_review"],
        "seconds_total": meta["seconds_total"],
        "read_only": meta["read_only"],
        "left_behind": meta["left_behind"],
        "wiki_pages": [p for p in pages if not p.startswith("sources/")],
        "broken_links": broken,
        "sources": sources,
        "old_unlabelled": [s["note"] for s in sources if s["old"] and not s["labelled_older"]],
        "notes_without_original": [s["note"] for s in sources if not s["original_given"]],
        "originals_without_note": sorted(set(originals_without_note)),
        "locations": len(locations),
        "bad_locations": sorted({loc for loc, ok in locations if not ok}),
        "parts_missing": [name for name, pattern in PARTS.items() if not pattern.search(text)],
    }


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [row for row in csv.DictReader(handle) if any(row.values())]


def finding_score(row: dict) -> int:
    values = [int(row[d]) for d in DIMENSIONS]
    return 2 if all(v == 2 for v in values) else 0 if any(v == 0 for v in values) else 1


def scorecard(run: Path, checks: list[dict], old_days: int) -> str:
    scores = read_csv(run / "scores.csv")
    smoke = read_csv(run / "smoke.csv")
    meta = json.loads((run / checks[0]["fixture"] / "meta.json").read_text(encoding="utf-8"))
    by_fixture: dict[str, list[dict]] = {}
    for row in scores:
        by_fixture.setdefault(row["fixture"], []).append(row)

    products = [c["fixture"] for c in checks if "control" not in c["fixture"] and "seeded" not in c["fixture"]]
    control = next((c["fixture"] for c in checks if "control" in c["fixture"]), None)
    seeded = next((c["fixture"] for c in checks if "seeded" in c["fixture"]), None)
    found = sorted({i for row in by_fixture.get(seeded, []) for i in row["ids"].split() if i.startswith("S")})
    recall = len(found)
    zeros = [f"{row['fixture']}: {row['finding']}" for row in scores if finding_score(row) == 0]
    without_two = [f for f in products if not any(finding_score(r) == 2 for r in by_fixture.get(f, []))]
    invented = len(by_fixture.get(control, []))
    slow = [c["fixture"] for c in checks if c["seconds_to_review"] is None or c["seconds_to_review"] > 200]
    wrote = [c["fixture"] for c in checks if not c["read_only"]]
    stale = sorted({s for c in checks for s in c["old_unlabelled"]})
    broken = sorted({b for c in checks for b in c["broken_links"]})
    ran = [row for row in smoke if row["started_without_questions"].strip().lower() != "not run"]
    smoke_agents = sorted({row["agent"] for row in ran})
    smoke_missing = sorted({row["agent"] for row in smoke} - set(smoke_agents))
    smoke_failed = [f"{row['agent']} on {row['fixture']}" for row in ran if row["started_without_questions"].strip().lower() != "yes"]

    def tick(ok: bool) -> str:
        return "yes" if ok else "**no**"

    lines = [
        "# Scorecard",
        "",
        f"Run `{run.name}`: {meta['agent']} with {meta['model']}"
        + (f" at {meta['effort']} effort" if meta.get("effort") else "")
        + f", review started by {'the published URL' if meta['via'] == 'url' else 'the ' + meta['via'] + ' path'}, "
        f"wiki revision `{meta['wiki_revision']}`, {meta['date']}. Written by `evals/score.py`; grades are in "
        f"[`runs/{run.name}/scores.csv`](runs/{run.name}/scores.csv) and each review beside it.",
        "",
        "## Stop rule",
        "",
        "| Condition | Result | Met |",
        "|---|---|---|",
        f"| Planted issues found on the seeded fixture, at least 4 of 5 | {recall} of 5 ({' '.join(found) or 'none'}) | {tick(recall >= 4)} |",
        f"| Invented findings on the no-AI control | {invented} | {tick(invented == 0)} |",
        f"| Every product fixture has a finding scoring 2 on all six dimensions | "
        f"{len(products) - len(without_two)} of {len(products)}"
        + (f" (missing: {', '.join(without_two)})" if without_two else "") + f" | {tick(not without_two)} |",
        f"| No finding scores 0 | {len(zeros)} at 0" + (f" ({'; '.join(zeros)})" if zeros else "") + f" | {tick(not zeros)} |",
        f"| One-paste smoke check on other agents | {len(ran)} run on {', '.join(smoke_agents) or 'none'}"
        + (f"; failed: {'; '.join(smoke_failed)}" if smoke_failed else "")
        + (f"; not run: {', '.join(smoke_missing)}" if smoke_missing else "")
        + f" | {tick(bool(ran) and not smoke_failed and not smoke_missing)} |",
        f"| Links to the wiki resolve | {len(broken)} broken" + (f" ({', '.join(broken)})" if broken else "") + f" | {tick(not broken)} |",
        f"| Sources older than {old_days} days are labelled as older | {len(stale)} unlabelled"
        + (f" ({', '.join(stale)})" if stale else "") + f" | {tick(not stale)} |",
        f"| Review arrives in about 3 minutes | slowest {max((c['seconds_to_review'] or 0) for c in checks):.0f}s"
        + (f" (over: {', '.join(slow)})" if slow else "") + f" | {tick(not slow)} |",
        f"| Fixture tree left untouched | {len(checks) - len(wrote)} of {len(checks)}"
        + (f" (changed: {', '.join(wrote)})" if wrote else "") + f" | {tick(not wrote)} |",
        "",
        "`python3 tools/lint.py` has to be clean as well; CI runs it on every push.",
        "",
        "## Reviews",
        "",
        "| Fixture | Agent, model | Seconds to review | Findings | Best | At 0 | Sources cited | Older, labelled | Tree |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for c in checks:
        rows = by_fixture.get(c["fixture"], [])
        best = max((finding_score(r) for r in rows), default=None)
        old = [s for s in c["sources"] if s["old"]]
        lines.append(
            f"| [{c['fixture']}](runs/{run.name}/{c['fixture']}/review.md) | {c['agent']}, {c['model']} | "
            f"{c['seconds_to_review'] if c['seconds_to_review'] is not None else '-'} | {len(rows)} | "
            f"{best if best is not None else '-'} | {sum(finding_score(r) == 0 for r in rows)} | {len(c['sources'])} | "
            f"{sum(s['labelled_older'] for s in old)} of {len(old)} | {'untouched' if c['read_only'] else 'changed'} |"
        )
    lines += ["", "## Findings", "", "| Fixture | Finding | Matches | " + " | ".join(d.capitalize() for d in DIMENSIONS) + " | Score | Note |",
              "|---|---|---|" + "---|" * len(DIMENSIONS) + "---|---|"]
    for row in scores:
        lines.append(f"| {row['fixture']} | {row['finding']} | {row['ids'] or '-'} | "
                     + " | ".join(row[d] for d in DIMENSIONS) + f" | {finding_score(row)} | {row['note']} |")
    if not scores:
        lines.append("| - | no findings graded yet | | | | | | | | | |")
    lines += ["", "## Other agents", ""]
    if smoke:
        lines += ["| Agent, model | Fixture | Started without questions | Seconds to first finding | Note |", "|---|---|---|---|---|"]
        lines += [f"| {r['agent']}, {r['model']} | {r['fixture']} | {r['started_without_questions']} | "
                  f"{r['first_finding_seconds']} | {r['note']} |" for r in smoke]
    else:
        lines.append("No smoke check recorded for this run.")
    lines += ["", "## Mechanical checks that did not pass", ""]
    problems = []
    for c in checks:
        for label, key in [("old source not labelled", "old_unlabelled"), ("source note cited without its original", "notes_without_original"),
                           ("outside link with no source note", "originals_without_note"), ("location not in the fixture", "bad_locations"),
                           ("part missing", "parts_missing"), ("left in the tree", "left_behind")]:
            if key in ("parts_missing", "notes_without_original") and not by_fixture.get(c["fixture"]):
                continue  # a review with no finding has no parts to carry
            if c[key]:
                problems.append(f"- {c['fixture']}: {label}: {', '.join(c[key])}")
    lines += problems or ["None."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run", type=Path)
    parser.add_argument("--old-days", type=int, default=365)
    parser.add_argument("--write", action="store_true", help="write evals/scorecard.md")
    args = parser.parse_args()
    run = args.run.resolve()
    folders = sorted(p for p in run.iterdir() if (p / "meta.json").is_file())
    if not folders:
        print(f"no reviews in {run}")
        return 2
    checks = [check_review(folder, args.old_days) for folder in folders]
    (run / "checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
    for c in checks:
        old = [s for s in c["sources"] if s["old"]]
        print(f"{c['fixture']:<18} {c['seconds_to_review']}s  sources {len(c['sources'])} (old {len(old)}, unlabelled "
              f"{len(c['old_unlabelled'])})  broken {len(c['broken_links'])}  no-original {len(c['notes_without_original'])}  "
              f"stray-links {len(c['originals_without_note'])}  locations {c['locations']} (bad {len(c['bad_locations'])})  "
              f"{'untouched' if c['read_only'] else 'CHANGED'}\n{'':<18} missing parts: {', '.join(c['parts_missing']) or 'none'}")
    if args.write:
        (ROOT / "evals" / "scorecard.md").write_text(scorecard(run, checks, args.old_days), encoding="utf-8")
        print("wrote evals/scorecard.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
