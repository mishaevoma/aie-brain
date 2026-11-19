"""Exercise the published review starting from the generated llms.txt."""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/brain-consult"
SITE = "https://mishaevoma.github.io/aie-brain"


def markdown_links(page):
    return re.findall(r"\]\(([^)\s]+)\)", page.read_text(encoding="utf-8"))


class ReviewPublicationTest(unittest.TestCase):
    def test_published_review(self):
        with tempfile.TemporaryDirectory() as temp:
            public = Path(temp).resolve()  # macOS keeps temporary folders behind a symlink
            (public / "index.html").touch()  # Minimal Quartz output.
            subprocess.run(
                [sys.executable, ROOT / "site/agentfiles.py", ROOT, public, SITE],
                check=True, stdout=subprocess.DEVNULL,
            )

            self.assertIn(f"{SITE}/review.md", markdown_links(public / "llms.txt"))
            review = public / "review.md"
            self.assertEqual(review.read_bytes(), (SKILL / "SKILL.md").read_bytes())

            self.assertRegex((public / "revision.txt").read_text(encoding="utf-8"), r"^[0-9a-f]{7,} \d{4}-\d{2}-\d{2}\n$")

            links = markdown_links(review)
            self.assertIn("references/project-review.md", links)
            for href in links:
                url = urlsplit(href)
                if url.scheme or url.netloc or not url.path:
                    continue
                path = Path(unquote(url.path))
                with self.subTest(link=href):
                    target = (public / path).resolve()
                    self.assertTrue(target.is_relative_to(public), f"Link leaves the site: {href}")
                    self.assertTrue(target.is_file(), f"Missing published link: {href}")
                    self.assertEqual(target.read_bytes(), (SKILL / path).read_bytes())


if __name__ == "__main__":
    unittest.main()
