#!/usr/bin/env python3
"""Add the agent-facing files to a built site.

For every page Quartz published, copy the page's markdown source next to it, so
that <page URL>.md returns the raw file. Then write llms.txt (the wiki's index.md
with absolute links to those raw files) and llms-full.txt (overview, glossary,
playbooks and concepts in one file).

Usage: python3 site/agentfiles.py <wiki dir> <built site dir> <site URL>
Standard library only.
"""
import pathlib
import posixpath
import re
import shutil
import sys

SUMMARY = (
    "A wiki of current practice for building AI products, written and maintained by AI agents "
    "and read by both agents and people. Every link below returns raw markdown."
)
# What goes into llms-full.txt, in reading order. Source notes stay out: they are long and one click away.
FULL_FILES = ["overview.md", "glossary.md"]
FULL_DIRS = ["playbooks", "concepts"]

LINK = re.compile(r"\]\((?!https?:|mailto:|#)([^)#\s]+\.md)(#[^)]*)?\)")
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    wiki = pathlib.Path(sys.argv[1]).resolve()
    public = pathlib.Path(sys.argv[2]).resolve()
    site = sys.argv[3].rstrip("/")

    # Quartz decides what is published and lower-cases page addresses (AGENTS.md becomes /agents).
    # Follow its output instead of repeating its ignore list here.
    html = {p.relative_to(public).as_posix().lower(): p.relative_to(public) for p in public.rglob("*.html")}

    raw = {}  # wiki path of a published page -> path of its raw copy in the site
    skipped = []
    for source in sorted(wiki.rglob("*.md")):
        rel = source.relative_to(wiki)
        if any(part.startswith(".") for part in rel.parts):
            continue
        page = html.get(rel.with_suffix(".html").as_posix().lower().replace(" ", "-"))
        if page is None:
            skipped.append(rel.as_posix())
            continue
        dest = public / page.with_suffix(".md")
        shutil.copyfile(source, dest)
        raw[rel.as_posix()] = dest.relative_to(public).as_posix()

    if "index.md" not in raw:
        print("error: index.md was not published, so llms.txt cannot be written")
        return 1

    def absolute(text: str, folder: str) -> str:
        """Rewrite relative .md links to absolute links to the raw copies."""

        def swap(match: re.Match) -> str:
            target = posixpath.normpath(posixpath.join(folder, match.group(1)))
            return f"]({site}/{raw.get(target, target)}{match.group(2) or ''})"

        return LINK.sub(swap, text)

    index = (wiki / "index.md").read_text(encoding="utf-8")
    body = FRONTMATTER.sub("", index, count=1).lstrip("\n")
    body = re.sub(r"\A# .*\n", "", body, count=1).lstrip("\n")  # the page's own heading; llms.txt has its own
    llms = f"# AI Engineering Brain\n\n> {SUMMARY}\n\n{absolute(body, '.')}"
    (public / "llms.txt").write_text(llms, encoding="utf-8")

    chosen = [f for f in FULL_FILES if f in raw]
    for folder in FULL_DIRS:
        chosen += sorted(p for p in raw if p.startswith(folder + "/"))
    parts = []
    for path in chosen:
        text = FRONTMATTER.sub("", (wiki / path).read_text(encoding="utf-8"), count=1).strip()
        parts.append(f"<!-- source: {site}/{raw[path]} -->\n\n{absolute(text, posixpath.dirname(path) or '.')}")
    full = "\n\n---\n\n".join(parts) + "\n"
    (public / "llms-full.txt").write_text(full, encoding="utf-8")

    print(f"{len(raw)} raw .md copies, llms.txt {len(llms.encode())} bytes, "
          f"llms-full.txt {len(full.encode())} bytes from {len(parts)} pages")
    if skipped:
        print("not published, so no raw copy: " + ", ".join(skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
