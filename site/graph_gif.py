#!/usr/bin/env python3
"""Draw the wiki's concept graph as a dependency wheel and save it as a GIF.

Everything on screen is read from the wiki. The concepts and their grouping are the "Concepts"
section of index.md. A chord joins two concepts when one page links to the other. The bar beside
a concept is the number of source notes its page cites, with the bright part for sources published
in the last 12 months. The text under the wheel is the page's own definition and status.

Usage: python3 site/graph_gif.py [output.gif] [concept ...]
       output defaults to .github/knowledge-graph.gif
       concepts are the pages to visit in turn; six are chosen when none is given

Needs Google Chrome (or Chromium) and ffmpeg. Python is standard library only.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = (shutil.which("google-chrome") or shutil.which("chromium")
          or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
FOCUS = ["harness", "tool-design", "memory", "context-engineering", "evals", "side-effects"]
SECONDS_EACH, FPS, FRESH_DAYS = 2.0, 12, 365
LINK = re.compile(r"\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")


def wiki_graph(focus: list[str]) -> dict:
    index = (ROOT / "index.md").read_text(encoding="utf-8")
    listing = index.split("\n## Concepts", 1)[1].split("\n## ", 1)[0]
    groups, group_of, group = [], {}, None
    for line in listing.splitlines():
        heading = re.fullmatch(r"\*\*(.+)\*\*", line.strip())
        page = re.match(r"- \[[^\]]+\]\(concepts/([a-z0-9-]+)\.md\)", line)
        if heading:
            group = heading.group(1)
            groups.append(group)
        elif page and group:
            group_of[page.group(1)] = group

    sources = {p.stem: dt.date.fromisoformat(p.stem[:10]) for p in (ROOT / "sources").glob("*.md")}
    today = max(sources.values())  # ages are counted from the newest source, so a rerun draws the same picture
    concepts, edges = [], set()
    for name, group in group_of.items():
        text = (ROOT / "concepts" / f"{name}.md").read_text(encoding="utf-8")
        cited = {Path(t).stem for t in LINK.findall(text) if "sources/" in t} & set(sources)
        for target in LINK.findall(text):
            other = Path(target).stem
            if "/" not in target and other in group_of and other != name:
                edges.add(tuple(sorted((name, other))))
        definition = re.search(r"\*\*Definition:\*\*\s*(.+)", text)
        first_sentence = re.split(r"(?<=\.)\s", re.sub(r"[*`]", "", definition.group(1)))[0] if definition else ""
        concepts.append({
            "id": name,
            "group": group,
            "status": re.search(r"^status:\s*(\w+)", text, re.M).group(1),
            "definition": first_sentence,
            "sources": len(cited),
            "fresh": sum((today - sources[s]).days <= FRESH_DAYS for s in cited),
            "newest": max(sources[s] for s in cited).isoformat(),
        })
    unknown = [f for f in focus if f not in group_of]
    if unknown:
        raise SystemExit(f"not a concept page listed in index.md: {', '.join(unknown)}")
    return {"concepts": concepts, "edges": sorted(edges), "groups": groups, "sources": len(sources),
            "date": today.isoformat(), "focus": focus}


class Browser:
    """Headless Chrome driven over --remote-debugging-pipe, so no package is needed."""

    def __init__(self, width: int, height: int, scale: int) -> None:
        to_chrome, self.commands = os.pipe()
        self.replies, from_chrome = os.pipe()

        def wire() -> None:  # Chrome reads commands on descriptor 3 and writes replies on 4
            a, b = os.dup(to_chrome), os.dup(from_chrome)
            os.dup2(a, 3)
            os.dup2(b, 4)

        self.profile = tempfile.mkdtemp(prefix="graph-gif-chrome-")
        self.process = subprocess.Popen(
            [CHROME, "--headless=new", "--remote-debugging-pipe", "--no-first-run", "--hide-scrollbars",
             f"--user-data-dir={self.profile}", "about:blank"],
            preexec_fn=wire, pass_fds=(3, 4), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        os.close(to_chrome)
        os.close(from_chrome)
        self.buffer, self.sent, self.session = b"", 0, None
        target = self.call("Target.createTarget", url="about:blank")["targetId"]
        self.session = self.call("Target.attachToTarget", targetId=target, flatten=True)["sessionId"]
        self.call("Page.enable")
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=scale, mobile=False)

    def read(self) -> dict:
        while b"\0" not in self.buffer:
            self.buffer += os.read(self.replies, 1 << 20)
        raw, self.buffer = self.buffer.split(b"\0", 1)
        return json.loads(raw)

    def call(self, method: str, **params) -> dict:
        self.sent += 1
        message = {"id": self.sent, "method": method, "params": params}
        if self.session:
            message["sessionId"] = self.session
        os.write(self.commands, json.dumps(message).encode() + b"\0")
        while True:
            reply = self.read()
            if reply.get("id") == self.sent:
                if "error" in reply:
                    raise RuntimeError(f"{method}: {reply['error']}")
                return reply.get("result", {})

    def open(self, url: str) -> None:
        self.call("Page.navigate", url=url)
        while self.read().get("method") != "Page.loadEventFired":
            pass

    def close(self) -> None:
        self.process.terminate()
        self.process.wait(timeout=10)
        shutil.rmtree(self.profile, ignore_errors=True)


def main() -> int:
    args = sys.argv[1:]
    output = Path(args[0]) if args and args[0].endswith(".gif") else ROOT / ".github" / "knowledge-graph.gif"
    focus = [a for a in args if not a.endswith(".gif")] or FOCUS
    data = wiki_graph(focus)
    frames = round(len(focus) * SECONDS_EACH * FPS)
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        template = (ROOT / "site" / "graph_gif.html").read_text(encoding="utf-8")
        (temp / "wheel.html").write_text(
            template.replace("<script>", f"<script>window.DATA = {json.dumps(data)};</script>\n<script>", 1), encoding="utf-8")
        browser = Browser(960, 540, 2)
        try:
            browser.open(f"file://{temp / 'wheel.html'}")
            for frame in range(frames):
                browser.call("Runtime.evaluate", expression=f"draw({frame / frames})")
                image = browser.call("Page.captureScreenshot", format="png")["data"]
                (temp / f"{frame:04d}.png").write_bytes(base64.b64decode(image))
        finally:
            browser.close()
        output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(temp / "%04d.png"),
             "-vf", "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
             "-loop", "0", str(output)],
            check=True,
        )
    print(f"{output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}: {len(data['concepts'])} concepts, "
          f"{len(data['edges'])} links, {data['sources']} sources, {frames / FPS:.0f}s, {output.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
