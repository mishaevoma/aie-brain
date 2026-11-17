#!/usr/bin/env python3
"""Check that every internal link in the built site leads to a file.

Paths are compared with exact case, the way GitHub Pages serves them. Broken
links are printed as GitHub Actions warnings. The check does not stop a deploy
unless --strict is given: the site is a view of the wiki, and one dead link
should not keep new pages from being published.

Usage: python3 site/linkcheck.py <built site dir> [<site URL>] [--strict]
Give the site URL when the site lives under a path (https://owner.github.io/repo),
so links that start with that path are checked against the right folder.
Standard library only.
"""
import pathlib
import posixpath
import re
import sys
import urllib.parse

HREF = re.compile(r'<a\b[^>]*?href="([^"]+)"', re.I)
EXTERNAL = re.compile(r"^(https?:|mailto:|#|javascript:|data:)")


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--strict"]
    if len(args) not in (1, 2):
        print(__doc__)
        return 2
    root = pathlib.Path(args[0]).resolve()
    base = urllib.parse.urlparse(args[1]).path.rstrip("/") if len(args) == 2 else ""
    files = {f.relative_to(root).as_posix() for f in root.rglob("*") if f.is_file()}

    def exists(url_path: str) -> bool:
        path = url_path.strip("/")
        candidates = [path, path + ".html", posixpath.join(path, "index.html")] if path else ["index.html"]
        return any(c in files for c in candidates)

    pages = sorted(f for f in files if f.endswith(".html"))
    total = 0
    broken = {}
    for page in pages:
        text = (root / page).read_text(encoding="utf-8", errors="replace")
        for href in HREF.findall(text):
            if EXTERNAL.match(href):
                continue
            target = urllib.parse.unquote(href.split("#")[0].split("?")[0])
            if not target:
                continue
            total += 1
            if base and (target == base or target.startswith(base + "/")):
                target = target[len(base):] or "/"
            url = posixpath.normpath(posixpath.join("/" + posixpath.dirname(page), target))
            if not exists(url):
                broken.setdefault(page, set()).add(href)

    count = sum(len(v) for v in broken.values())
    print(f"{len(pages)} html pages, {total} internal links, {count} broken")
    for page, hrefs in sorted(broken.items()):
        for href in sorted(hrefs):
            print(f"::warning title=Broken link::{page} links to {href}, which is not in the site")
    return 1 if count and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
