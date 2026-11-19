import datetime
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import memory


def client_replying(text):
    create = lambda **kwargs: SimpleNamespace(content=[SimpleNamespace(text=text)])
    return SimpleNamespace(messages=SimpleNamespace(create=create))


class MemoryTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "memory.jsonl"

    def tearDown(self):
        self.folder.cleanup()

    def test_notes_are_appended_with_the_date(self):
        added = memory.remember(
            "Ich gehe in der Schule.", "in die Schule", client_replying("Uses dative after 'in' for direction"),
            self.path, datetime.date(2026, 7, 1),
        )
        self.assertEqual(added, 1)
        self.assertEqual(memory.load_all(self.path), "[2026-07-01] Uses dative after 'in' for direction")

    def test_none_adds_nothing(self):
        self.assertEqual(memory.remember("Guten Tag!", "Guten Tag!", client_replying("NONE"), self.path), 0)
        self.assertEqual(memory.load_all(self.path), "")

    def test_notes_accumulate(self):
        for _ in range(3):
            memory.remember("x", "y", client_replying("Mixes up wann and wenn"), self.path, datetime.date(2026, 7, 1))
        self.assertEqual(len(memory.load_all(self.path).splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
