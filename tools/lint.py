#!/usr/bin/env python3
"""Health checks for the AI engineering brain. Standard library only.

Usage:
  python3 tools/lint.py                  check everything, exit 1 on errors
  python3 tools/lint.py --sync           also rewrite the generated parts: each source note's
                                         `concepts:` list and the source list in index.md
  python3 tools/lint.py --stale-days 90  change the age at which a page is flagged for review

What it checks:
  - every relative markdown link points at a file that exists
  - source notes: required frontmatter, valid values, filename date matches `published`, no duplicate URLs
  - concept and playbook pages: required frontmatter, at least one link to a source note
  - index.md lists every page in concepts/, playbooks/ and sources/
  - every glossary term appears by name on the page its entry links to (warning)
  - every figure on a cited line appears in a source note that line cites (warning)
  - source notes that no concept or playbook uses (warning)
  - concept and playbook pages not updated for --stale-days days (warning)
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".claude", ".obsidian", "raw", "node_modules", "__pycache__"}

KINDS = {"article", "x-post", "x-article", "video", "paper", "docs"}
READ_LEVELS = {"full", "partial", "summary-only"}
STATUSES = {"settled", "evolving", "contested"}
SOURCE_FIELDS = ["type", "title", "author", "publisher", "url", "published", "ingested", "kind", "read", "concepts"]
PAGE_FIELDS = {
    "concept": ["type", "title", "updated", "status"],
    "playbook": ["type", "title", "updated"],
}

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
PAGE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
CONCEPTS_LINE = re.compile(r"^concepts:.*$", re.M)
INDEX_START = "<!-- sources:start -->"
INDEX_END = "<!-- sources:end -->"
GLOSSARY_ENTRY = re.compile(r"^- \*\*(.+?)\*\* — .*\]\(([^)]+)\)\s*$")
LINK_FULL = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
NUMBER = re.compile(r"(?<![\w.^@])\d+(?:\.\d+)?")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"ERROR {rel(path)}: {message}")

    def warn(self, path: Path, message: str) -> None:
        self.warnings.append(f"WARN  {rel(path)}: {message}")


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


def sources_block(sources: set[Path], pages: dict[Path, tuple[dict[str, object], str]]) -> str:
    """The generated list of source notes for index.md, newest first."""
    lines = []
    for path in sorted(sources, key=lambda p: p.name, reverse=True):
        fields = pages[path][0]
        title = str(fields.get("title", path.stem)).replace("[", "(").replace("]", ")")
        lines.append(f"- {fields.get('published', '')} · [{title}](sources/{path.name}) · {fields.get('author', '')}")
    return "\n".join(lines)


def local_links(path: Path, body: str) -> list[Path]:
    """Resolved targets of the relative links in a page, ignoring code and web links."""
    prose = INLINE_CODE.sub("", FENCE.sub("", body))
    targets = []
    for raw in LINK.findall(prose):
        if re.match(r"^[a-z][a-z0-9+.-]*:", raw, re.I) or raw.startswith("#"):
            continue
        target = unquote(raw.split("#", 1)[0].split("?", 1)[0])
        if target:
            targets.append((path.parent / target).resolve())
    return targets


def check_date(report: Report, path: Path, fields: dict[str, object], key: str) -> dt.date | None:
    value = str(fields.get(key, ""))
    if not DATE.match(value):
        report.error(path, f"`{key}` must be a YYYY-MM-DD date, got '{value}'")
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        report.error(path, f"`{key}` is not a real date: '{value}'")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the AI engineering brain.")
    parser.add_argument("--sync", action="store_true", help="rewrite `concepts:` in source notes and the source list in index.md")
    parser.add_argument("--stale-days", type=int, default=120, help="flag concept and playbook pages older than this (default 120)")
    args = parser.parse_args()

    report = Report()
    today = dt.date.today()
    pages: dict[Path, tuple[dict[str, object], str]] = {}
    links: dict[Path, list[Path]] = {}

    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        fields, body = split_frontmatter(text)
        pages[path] = (fields, body)
        if path.name.endswith("-template.md"):
            continue
        links[path] = local_links(path, body)
        for target in links[path]:
            if not target.exists():
                report.error(path, f"broken link to {os.path.relpath(target, ROOT)}")

    sources = {p for p in pages if p.parent == ROOT / "sources"}
    concepts = {p for p in pages if p.parent == ROOT / "concepts"}
    playbooks = {p for p in pages if p.parent == ROOT / "playbooks"}

    # Source notes
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

    # Concept and playbook pages
    for kind, group in (("concept", concepts), ("playbook", playbooks)):
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
                updated = check_date(report, path, fields, "updated")
                if updated and (today - updated).days > args.stale_days:
                    report.warn(path, f"not updated for {(today - updated).days} days; review against newer sources")
            if not any(t in sources for t in links.get(path, [])):
                report.error(path, "links to no source note; every claim needs a source")

    # Backlinks: which concept pages use each source
    used_by: dict[Path, set[str]] = {s: set() for s in sources}
    used_at_all: set[Path] = set()
    for path in concepts | playbooks:
        for target in links.get(path, []):
            if target in used_by:
                used_at_all.add(target)
                if path in concepts:
                    used_by[target].add(path.stem)
    for path in sorted(sources):
        if path not in used_at_all:
            report.warn(path, "no concept or playbook page uses this source")
        wanted = sorted(used_by[path])
        current = pages[path][0].get("concepts", [])
        if wanted != current:
            if args.sync:
                text = path.read_text(encoding="utf-8")
                new_line = "concepts: [" + ", ".join(wanted) + "]"
                updated_text, count = CONCEPTS_LINE.subn(new_line, text, count=1)
                if count:
                    path.write_text(updated_text, encoding="utf-8")
                else:
                    report.error(path, "no `concepts:` line to update")
            else:
                report.warn(path, "`concepts:` is out of date; run `python3 tools/lint.py --sync`")

    # Index: the source list between the markers is generated, the rest is written by hand
    index = ROOT / "index.md"
    if index not in pages:
        report.error(ROOT / "index.md", "index.md is missing")
    else:
        text = index.read_text(encoding="utf-8")
        if INDEX_START not in text or INDEX_END not in text:
            report.error(index, f"missing the {INDEX_START} / {INDEX_END} markers")
        else:
            head, rest = text.split(INDEX_START, 1)
            current, tail = rest.split(INDEX_END, 1)
            wanted_block = "\n" + sources_block(sources, pages) + "\n"
            if current != wanted_block:
                if args.sync:
                    text = head + INDEX_START + wanted_block + INDEX_END + tail
                    index.write_text(text, encoding="utf-8")
                    links[index] = local_links(index, split_frontmatter(text)[1])
                else:
                    report.warn(index, "source list is out of date; run `python3 tools/lint.py --sync`")
        listed = set(links.get(index, []))
        for path in sorted(sources | concepts | playbooks):
            if path not in listed:
                report.error(path, "not listed in index.md")

    # Numbers: a figure on a cited line must appear in one of the source notes that line cites
    source_text = {s: strip_digit_commas(s.read_text(encoding="utf-8")) for s in sources}
    for path in sorted(concepts | playbooks | ({ROOT / "overview.md"} & set(pages))):
        for line in pages[path][1].splitlines():
            cited = [t for t in (
                (path.parent / unquote(raw.split("#", 1)[0])).resolve()
                for raw in LINK.findall(line) if not re.match(r"^[a-z][a-z0-9+.-]*:", raw, re.I)
            ) if t in source_text]
            if not cited:
                continue
            prose = strip_digit_commas(re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", INLINE_CODE.sub("", LINK_FULL.sub("", line))))
            for number in sorted(set(NUMBER.findall(prose))):
                pattern = re.compile(r"(?<![\d.])" + re.escape(number) + r"(?!\d)")
                if not any(pattern.search(source_text[s]) for s in cited):
                    report.warn(path, f"number {number} is not in the source notes cited on its line: {prose.strip()[:70]}")

    # Glossary: every term must appear by name on the page its entry points to
    glossary = ROOT / "glossary.md"
    if glossary not in pages:
        report.error(glossary, "glossary.md is missing")
    else:
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

    for line in report.errors + report.warnings:
        print(line)
    print(
        f"{len(sources)} sources, {len(concepts)} concepts, {len(playbooks)} playbooks: "
        f"{len(report.errors)} errors, {len(report.warnings)} warnings"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
