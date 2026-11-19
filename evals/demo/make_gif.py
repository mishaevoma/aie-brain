#!/usr/bin/env python3
"""Render the review demo to a GIF: three real upgrades, about eleven seconds.

Each scene names a primitive and the gist of the upgrade, in the words of overview.md, then the
evidence, copied by hand from a real review in evals/runs/ (the scene's `credit` says which). Each step of demo.html is captured with
headless Chrome and the frames are joined with ffmpeg. Both have to be installed.

Usage: python3 evals/demo/make_gif.py [output.gif]     (default: .github/review-demo.gif)
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SIZE = (960, 540)
TYPING, GIST, PROOF, LAST = 0.35, 1.1, 2.1, 1.6  # seconds each kind of step stays on screen


def main() -> int:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".github" / "review-demo.gif"
    demo = json.loads((HERE / "showcases.json").read_text(encoding="utf-8"))
    holds = [TYPING] * demo["typing_steps"] + [GIST, PROOF] * len(demo["scenes"]) + [LAST]
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        page = temp / "demo.html"
        page.write_text(
            (HERE / "demo.html").read_text(encoding="utf-8").replace(
                "<script>", f"<script>window.DEMO = {json.dumps(demo)};</script>\n<script>", 1),
            encoding="utf-8",
        )
        listing = []
        for step, hold in enumerate(holds):
            frame = temp / f"{step:02d}.png"
            subprocess.run(
                [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={SIZE[0]},{SIZE[1]}",
                 "--force-device-scale-factor=1", f"--screenshot={frame}", f"file://{page}?step={step}"],
                check=True, capture_output=True,
            )
            listing += [f"file '{frame}'", f"duration {hold}"]
        # ffmpeg's concat reader wants the last frame named twice, and shows it for its duration both times.
        listing[-1] = f"duration {holds[-1] / 2}"
        listing += [f"file '{frame}'", f"duration {holds[-1] / 2}"]
        (temp / "frames.txt").write_text("\n".join(listing) + "\n", encoding="utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(temp / "frames.txt"),
             "-vf", "fps=10,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none",
             "-loop", "0", str(output)],
            check=True,
        )
    print(f"{output} · {sum(holds):.1f}s · {output.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
