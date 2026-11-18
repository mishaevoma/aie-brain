#!/usr/bin/env python3
"""Health checks and bookkeeping for the AI engineering brain. Standard library only.

Usage:
  python3 tools/lint.py
      Check everything. Exit 1 on errors.
  python3 tools/lint.py --sync
      Also rewrite the generated parts: each source note's `concepts:` list and
      the source list in index.md.
  python3 tools/lint.py --sync --log "ingest | Title of the source"
      Sync, check and, if there are no errors, append a dated entry to log.md that
      lists the files changed since the last commit. Operations: init, ingest,
      lint, refresh, edit.
  python3 tools/lint.py --ages
      Check, then print how old the sources behind each page are.

Options:
  --stale-days N   flag pages not reviewed for N days (default 120)
  --old-days N     a source is old once it was published more than N days ago (default 365).
                   Sets when a concept page is flagged because its newest source is old,
                   and what --ages counts as an old line.

Errors:
  - a relative markdown link points at a file that does not exist
  - a source note lacks required frontmatter, has an invalid value, a filename date
    that differs from `published`, or a URL another note already has
  - a concept or playbook page lacks required frontmatter or links to no source note
  - a bullet under "What to do" on a concept page has no link to a source note
  - a citation label carries a date that differs from the note's `published` date
  - a page in concepts/, playbooks/ or sources/ is not listed in index.md
  - a link in considered.md is also the URL of a source note

Warnings:
  - a source note that no concept or playbook uses
  - a page not reviewed for --stale-days days
  - a concept page whose newest cited source is older than --old-days days
  - a citation label without a date
  - a figure on a cited line that is not in any source note the line cites
  - a glossary term that does not appear on the page its entry links to
  - generated parts that are out of date (run with --sync)

What --ages reports, without raising a warning:
  - for each concept page and playbook: how many lines cite a source note, how many of those
    lines rest only on sources published more than --old-days days ago, and the dates of the
    oldest and newest source the page cites. `updated:` says when a page was last edited and
    `reviewed:` when it was last re-read; this says how old its evidence is.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".github", ".claude", ".obsidian", "raw", "node_modules", "__pycache__"}

KINDS = {"article", "x-post", "x-article", "video", "paper", "docs"}
READ_LEVELS = {"full", "partial", "summary-only"}
STATUSES = {"settled", "evolving", "contested"}
OPERATIONS = {"init", "ingest", "lint", "refresh", "edit"}
SOURCE_FIELDS = ["type", "title", "author", "publisher", "url", "published", "ingested", "kind", "read", "concepts"]
PAGE_FIELDS = {
    "concept": ["type", "title", "updated", "reviewed", "status"],
    "playbook": ["type", "title", "updated", "reviewed"],
}
MONTHS = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), start=1)}

LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_FULL = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
PAGE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
CONCEPTS_LINE = re.compile(r"^concepts:.*$", re.M)
LIST_ITEM = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
LABEL_DATE = re.compile(r"(?:(\d{1,2}) )?(" + "|".join(MONTHS) + r") (\d{4})$")
GLOSSARY_ENTRY = re.compile(r"^- \*\*(.+?)\*\* — .*\]\(([^)]+)\)\s*$")
NUMBER = re.compile(r"(?<![\w.^@])\d+(?:\.\d+)?")
WEB_LINK = re.compile(r"\]\((https?://[^)\s]+)\)")
INDEX_START = "<!-- sources:start -->"
INDEX_END = "<!-- sources:end -->"

Pages = dict  # Path -> (frontmatter fields, body)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"ERROR {rel(path)}: {message}")

    def warn(self, path: Path, message: str) -> None:
        self.warnings.append(f"WARN  {rel(path)}: {message}")


# ---------------------------------------------------------------- helpers


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def strip_digit_commas(text: str) -> str:
    """Write 2,500 as 2500 so figures compare regardless of thousands separators."""
    return re.sub(r"(?<=\d),(?=\d{3})", "", text)


def normalise(text: str) -> str:
    """Lower-case and drop markdown emphasis so 'the *verify* skill' matches 'verify skill'."""
    return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", text.lower()))


def markdown_files() -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                found.append(Path(dirpath) / name)
    return found


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Return (fields, body). Understands `key: value` and `key: [a, b]` only."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    fields: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            fields[key.strip()] = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        elif len(value) >= 2 and value[0] == value[-1] == '"':
            fields[key.strip()] = value[1:-1].replace('\\"', '"')
        else:
            fields[key.strip()] = value.strip("'")
    return fields, text[end + 4 :]


def links_in(path: Path, text: str) -> list[tuple[str, Path]]:
    """(label, resolved target) for every relative link in a piece of markdown."""
    found = []
    for label, raw in LINK.findall(text):
        if SCHEME.match(raw) or raw.startswith("#"):
            continue
        target = unquote(raw.split("#", 1)[0].split("?", 1)[0])
        if target:
            found.append((label, (path.parent / target).resolve()))
    return found


def prose_links(path: Path, body: str) -> list[tuple[str, Path]]:
    """Links in a page, ignoring anything inside code."""
    return links_in(path, INLINE_CODE.sub("", FENCE.sub("", body)))


def parse_date(value: object) -> dt.date | None:
    if not DATE.match(str(value)):
        return None
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def check_date(report: Report, path: Path, fields: dict[str, object], key: str) -> dt.date | None:
    parsed = parse_date(fields.get(key, ""))
    if parsed is None:
        report.error(path, f"`{key}` must be a real YYYY-MM-DD date, got '{fields.get(key, '')}'")
    return parsed


def sources_block(sources: set[Path], pages: Pages) -> str:
    """The generated list of source notes for index.md, newest first."""
    lines = []
    for path in sorted(sources, key=lambda p: p.name, reverse=True):
        fields = pages[path][0]
        title = str(fields.get("title", path.stem)).replace("[", "(").replace("]", ")")
        lines.append(f"- {fields.get('published', '')} · [{title}](sources/{path.name}) · {fields.get('author', '')}")
    return "\n".join(lines)


# ---------------------------------------------------------------- checks


def check_sources(report: Report, pages: Pages, sources: set[Path]) -> None:
    seen_urls: dict[str, Path] = {}
    for path in sorted(sources):
        fields, body = pages[path]
        for key in SOURCE_FIELDS:
            if key not in fields:
                report.error(path, f"missing frontmatter field `{key}`")
        if fields.get("type") != "source":
            report.error(path, "`type` must be `source`")
        if "kind" in fields and fields["kind"] not in KINDS:
            report.error(path, f"`kind` must be one of {sorted(KINDS)}")
        if "read" in fields and fields["read"] not in READ_LEVELS:
            report.error(path, f"`read` must be one of {sorted(READ_LEVELS)}")
        published = check_date(report, path, fields, "published") if "published" in fields else None
        if "ingested" in fields:
            check_date(report, path, fields, "ingested")
        name = SOURCE_NAME.match(path.name)
        if not name:
            report.error(path, "filename must look like YYYY-MM-DD-who-slug.md")
        elif published and name.group(1) != published.isoformat():
            report.error(path, f"filename date {name.group(1)} differs from `published` {published}")
        url = str(fields.get("url", ""))
        if not url.startswith("http"):
            report.error(path, "`url` must be a web address")
        elif url in seen_urls:
            report.error(path, f"same `url` as {rel(seen_urls[url])}")
        else:
            seen_urls[url] = path
        if "Delete this comment" in body:
            report.error(path, "template comment was left in the note")


def check_pages(report: Report, pages: Pages, links: dict, sources: set[Path], group: set[Path], kind: str, today: dt.date, stale_days: int) -> None:
    for path in sorted(group):
        fields, _ = pages[path]
        for key in PAGE_FIELDS[kind]:
            if key not in fields:
                report.error(path, f"missing frontmatter field `{key}`")
        if fields.get("type") != kind:
            report.error(path, f"`type` must be `{kind}`")
        if kind == "concept" and "status" in fields and fields["status"] not in STATUSES:
            report.error(path, f"`status` must be one of {sorted(STATUSES)}")
        if not PAGE_NAME.match(path.name):
            report.error(path, "filename must be kebab-case")
        if "updated" in fields:
            check_date(report, path, fields, "updated")
        if "reviewed" in fields:
            reviewed = check_date(report, path, fields, "reviewed")
            if reviewed and (today - reviewed).days > stale_days:
                report.warn(path, f"not reviewed for {(today - reviewed).days} days; re-read it against newer sources, then set `reviewed:`")
        if not any(target in sources for _, target in links.get(path, [])):
            report.error(path, "links to no source note; every claim needs a source")


def check_what_to_do(report: Report, pages: Pages, sources: set[Path], concepts: set[Path]) -> None:
    """Every bullet under "What to do" must cite a source note. Lead-in lines ending in a colon are exempt."""
    for path in sorted(concepts):
        section = ""
        for line in pages[path][1].splitlines():
            if line.startswith("## "):
                section = line[3:].strip().lower()
                continue
            if not section.startswith("what to do") or not LIST_ITEM.match(line) or line.rstrip().endswith(":"):
                continue
            if not any(target in sources for _, target in links_in(path, line)):
                report.error(path, f"bullet under 'What to do' cites no source note: {LIST_ITEM.sub('', line)[:60]}")


def check_citation_labels(report: Report, pages: Pages, links: dict, sources: set[Path], cited_pages: list[Path]) -> None:
    """A citation reads [Short title, Mon YYYY](note). The date must be the note's publication date."""
    for path in cited_pages:
        undated = set()
        for label, target in links.get(path, []):
            if target not in sources:
                continue
            published = parse_date(pages[target][0].get("published", ""))
            match = LABEL_DATE.search(label.strip())
            if not match:
                undated.add(label)
            elif published:
                day, month, year = match.groups()
                if (int(year), MONTHS[month]) != (published.year, published.month) or (day and int(day) != published.day):
                    report.error(path, f"citation '{label}' does not match the note's date {published}")
        for label in sorted(undated):
            report.warn(path, f"citation '{label}' has no date; write it as 'Short title, Mon YYYY'")


def check_source_age(report: Report, pages: Pages, links: dict, sources: set[Path], concepts: set[Path], today: dt.date, max_days: int) -> None:
    for path in sorted(concepts):
        dates = [parse_date(pages[t][0].get("published", "")) for _, t in links.get(path, []) if t in sources]
        dates = [d for d in dates if d]
        if dates and (today - max(dates)).days > max_days:
            report.warn(path, f"newest cited source is from {max(dates)}; look for newer material on this topic")


def sync_backlinks(report: Report, pages: Pages, links: dict, sources: set[Path], concepts: set[Path], playbooks: set[Path], sync: bool) -> None:
    used_by: dict[Path, set[str]] = {s: set() for s in sources}
    used_at_all: set[Path] = set()
    for path in concepts | playbooks:
        for _, target in links.get(path, []):
            if target in used_by:
                used_at_all.add(target)
                if path in concepts:
                    used_by[target].add(path.stem)
    for path in sorted(sources):
        if path not in used_at_all:
            report.warn(path, "no concept or playbook page uses this source")
        wanted = sorted(used_by[path])
        if wanted == pages[path][0].get("concepts", []):
            continue
        if not sync:
            report.warn(path, "`concepts:` is out of date; run `python3 tools/lint.py --sync`")
            continue
        text = path.read_text(encoding="utf-8")
        updated, count = CONCEPTS_LINE.subn("concepts: [" + ", ".join(wanted) + "]", text, count=1)
        if count:
            path.write_text(updated, encoding="utf-8")
        else:
            report.error(path, "no `concepts:` line to update")


def sync_index(report: Report, pages: Pages, links: dict, sources: set[Path], listed_pages: set[Path], sync: bool) -> None:
    """The source list between the markers is generated. The rest of index.md is written by hand."""
    index = ROOT / "index.md"
    if index not in pages:
        report.error(index, "index.md is missing")
        return
    text = index.read_text(encoding="utf-8")
    if INDEX_START not in text or INDEX_END not in text:
        report.error(index, f"missing the {INDEX_START} / {INDEX_END} markers")
    else:
        head, rest = text.split(INDEX_START, 1)
        current, tail = rest.split(INDEX_END, 1)
        wanted = "\n" + sources_block(sources, pages) + "\n"
        if current != wanted and sync:
            text = head + INDEX_START + wanted + INDEX_END + tail
            index.write_text(text, encoding="utf-8")
            links[index] = prose_links(index, split_frontmatter(text)[1])
        elif current != wanted:
            report.warn(index, "source list is out of date; run `python3 tools/lint.py --sync`")
    listed = {target for _, target in links.get(index, [])}
    for path in sorted(listed_pages):
        if path not in listed:
            report.error(path, "not listed in index.md")


def check_ledger(report: Report, pages: Pages, sources: set[Path]) -> None:
    """considered.md lists sources that were looked at and left out. None of them may also be a note."""
    ledger = ROOT / "considered.md"
    if ledger not in pages:
        return
    passed_over = {url.rstrip("/") for url in WEB_LINK.findall(pages[ledger][1])}
    for path in sorted(sources):
        for key in ("url", "via"):
            if str(pages[path][0].get(key, "")).rstrip("/") in passed_over:
                report.error(ledger, f"lists a source that has a note: {rel(path)}")


def check_numbers(report: Report, pages: Pages, sources: set[Path], cited_pages: list[Path]) -> None:
    """A figure on a cited line must appear in one of the source notes that line cites."""
    source_text = {s: strip_digit_commas(s.read_text(encoding="utf-8")) for s in sources}
    for path in cited_pages:
        for line in pages[path][1].splitlines():
            cited = [target for _, target in links_in(path, line) if target in source_text]
            if not cited:
                continue
            prose = strip_digit_commas(LIST_ITEM.sub("", INLINE_CODE.sub("", LINK_FULL.sub("", line))))
            for number in sorted(set(NUMBER.findall(prose))):
                pattern = re.compile(r"(?<![\d.])" + re.escape(number) + r"(?!\d)")
                if not any(pattern.search(source_text[s]) for s in cited):
                    report.warn(path, f"number {number} is not in the source notes cited on its line: {prose.strip()[:70]}")


def check_glossary(report: Report, pages: Pages) -> None:
    """Every term must appear by name on the page its entry points to."""
    glossary = ROOT / "glossary.md"
    if glossary not in pages:
        report.error(glossary, "glossary.md is missing")
        return
    for line in pages[glossary][1].splitlines():
        entry = GLOSSARY_ENTRY.match(line)
        if not entry:
            continue
        target = (ROOT / entry.group(2)).resolve()
        if target not in pages:
            continue  # already reported as a broken link
        page_text = normalise(pages[target][1])
        names = [n for n in re.split(r"\s*/\s*|,\s*|\s*\(|\)", entry.group(1)) if n.strip()]
        if not any(normalise(name) in page_text for name in names):
            report.warn(glossary, f"term '{entry.group(1)}' does not appear on {rel(target)}")


def ages_report(group: list[Path], pages: Pages, sources: set[Path], today: dt.date, old_days: int) -> list[str]:
    """One row per page, the pages resting most on old sources first."""
    published_on = {s: parse_date(pages[s][0].get("published", "")) for s in sources}
    rows = []
    for path in group:
        fields, body = pages[path]
        cited_lines = 0
        old_lines = 0
        dates: list[dt.date] = []
        for line in body.splitlines():
            line_dates = [published_on[t] for _, t in links_in(path, line) if published_on.get(t)]
            if not line_dates:
                continue
            cited_lines += 1
            dates.extend(line_dates)
            if (today - max(line_dates)).days > old_days:
                old_lines += 1
        if dates:
            label = str(fields.get("status", fields.get("type", "-")))
            rows.append((old_lines, cited_lines, rel(path), label, min(dates), max(dates)))
    rows.sort(key=lambda row: (-row[0], -row[0] / row[1], row[2]))
    width = max([len(row[2]) for row in rows] + [len("page")])
    lines = [
        f"Source ages. A line is old when every source it cites was published more than {old_days} days ago.",
        f"{'page':<{width}}  {'status':<9}  {'cited':>5}  {'old':>3}  {'oldest':<10}  newest",
    ]
    for old_lines, cited_lines, name, label, oldest, newest in rows:
        lines.append(f"{name:<{width}}  {label:<9}  {cited_lines:>5}  {old_lines:>3}  {oldest.isoformat()}  {newest.isoformat()}")
    lines.append(
        f"{sum(row[0] for row in rows)} of {sum(row[1] for row in rows)} cited lines "
        f"rest only on sources older than {old_days} days"
    )
    return lines


def run_checks(args: argparse.Namespace, today: dt.date) -> tuple[Report, str, list[str]]:
    report = Report()
    pages: Pages = {}
    links: dict[Path, list[tuple[str, Path]]] = {}

    for path in markdown_files():
        pages[path] = split_frontmatter(path.read_text(encoding="utf-8"))
        if path.name.endswith("-template.md"):
            continue
        links[path] = prose_links(path, pages[path][1])
        for _, target in links[path]:
            if not target.exists():
                report.error(path, f"broken link to {os.path.relpath(target, ROOT)}")

    sources = {p for p in pages if p.parent == ROOT / "sources"}
    concepts = {p for p in pages if p.parent == ROOT / "concepts"}
    playbooks = {p for p in pages if p.parent == ROOT / "playbooks"}
    cited_pages = sorted(concepts | playbooks | ({ROOT / "overview.md"} & set(pages)))

    check_sources(report, pages, sources)
    check_pages(report, pages, links, sources, concepts, "concept", today, args.stale_days)
    check_pages(report, pages, links, sources, playbooks, "playbook", today, args.stale_days)
    check_what_to_do(report, pages, sources, concepts)
    check_citation_labels(report, pages, links, sources, cited_pages)
    check_source_age(report, pages, links, sources, concepts, today, args.old_days)
    sync_backlinks(report, pages, links, sources, concepts, playbooks, args.sync)
    sync_index(report, pages, links, sources, sources | concepts | playbooks, args.sync)
    check_ledger(report, pages, sources)
    check_numbers(report, pages, sources, cited_pages)
    check_glossary(report, pages)

    summary = (
        f"{len(sources)} sources, {len(concepts)} concepts, {len(playbooks)} playbooks: "
        f"{len(report.errors)} errors, {len(report.warnings)} warnings"
    )
    ages = ages_report(sorted(concepts | playbooks), pages, sources, today, args.old_days) if args.ages else []
    return report, summary, ages


# ---------------------------------------------------------------- bookkeeping


@contextlib.contextmanager
def repo_lock():
    """One writer at a time: two sessions syncing or logging in the same folder take turns."""
    try:
        import fcntl
    except ImportError:  # not available on Windows
        yield
        return
    name = "aie-brain-" + hashlib.sha1(str(ROOT).encode()).hexdigest()[:12] + ".lock"
    with open(Path(tempfile.gettempdir()) / name, "w") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def changed_files() -> list[str]:
    """Files changed since the last commit, or nothing if this is not a git checkout."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    paths = [line[3:].split(" -> ")[-1].strip().strip('"') for line in out.splitlines()]
    return sorted(p for p in paths if p and p != "log.md")


def append_log(operation: str, title: str, today: dt.date) -> None:
    groups: dict[str, list[str]] = {}
    for path in changed_files():
        groups.setdefault(path.split("/", 1)[0] if "/" in path else "", []).append(path)
    lines = []
    for head in sorted(groups):
        if head and len(groups[head]) > 8:
            lines.append(f"- {head}/ ({len(groups[head])} files)")
        else:
            lines.extend(f"- {path}" for path in groups[head])
    log = ROOT / "log.md"
    existing = log.read_text(encoding="utf-8") if log.exists() else "# Log\n"
    entry = f"\n## [{today.isoformat()}] {operation} | {title}\n"
    if lines:
        entry += "\n" + "\n".join(lines) + "\n"
    log.write_text(existing.rstrip("\n") + "\n" + entry, encoding="utf-8")
    print(f"logged: [{today.isoformat()}] {operation} | {title}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the AI engineering brain.")
    parser.add_argument("--sync", action="store_true", help="rewrite `concepts:` in source notes and the source list in index.md")
    parser.add_argument("--log", metavar='"OPERATION | TITLE"', help="append an entry to log.md if there are no errors")
    parser.add_argument("--stale-days", type=int, default=120, help="flag pages not reviewed for this long (default 120)")
    parser.add_argument("--ages", action="store_true", help="also print how old the sources behind each concept page and playbook are")
    parser.add_argument("--old-days", type=int, default=365, help="a source is old after this many days: flags concept pages whose newest source is older, and sets what --ages counts as an old line (default 365)")
    args = parser.parse_args()

    entry = None
    if args.log is not None:
        entry = re.match(r"^\s*([a-z]+)\s*\|\s*(\S.*?)\s*$", args.log)
        if not entry or entry.group(1) not in OPERATIONS:
            parser.error(f'--log takes "OPERATION | TITLE" with one of: {", ".join(sorted(OPERATIONS))}')

    today = dt.date.today()
    with repo_lock() if (args.sync or entry) else contextlib.nullcontext():
        report, summary, ages = run_checks(args, today)
        for line in report.errors + report.warnings + ages:
            print(line)
        print(summary)
        if entry and report.errors:
            print("log entry not written: fix the errors and run again")
        elif entry:
            append_log(entry.group(1), entry.group(2), today)
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
