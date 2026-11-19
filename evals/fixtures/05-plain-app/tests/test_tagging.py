import unittest
from types import SimpleNamespace

from app import tagging


def client_replying(text):
    create = lambda **kwargs: SimpleNamespace(content=[SimpleNamespace(text=text)])
    return SimpleNamespace(messages=SimpleNamespace(create=create))


class TaggingTest(unittest.TestCase):
    def test_returns_the_category(self):
        self.assertEqual(tagging.tag_ticket("I was charged twice", client_replying("billing")), "billing")

    def test_strips_and_lowercases(self):
        self.assertEqual(tagging.tag_ticket("it crashes", client_replying(" Bug\n")), "bug")


if __name__ == "__main__":
    unittest.main()
