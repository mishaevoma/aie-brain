import unittest

from slugkit import slugify


class SlugifyTest(unittest.TestCase):
    def test_lowercases_and_joins_words(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_removes_accents(self):
        self.assertEqual(slugify("Crème brûlée"), "creme-brulee")

    def test_collapses_punctuation_and_spaces(self):
        self.assertEqual(slugify("  Hello,   World!!  "), "hello-world")

    def test_keeps_digits(self):
        self.assertEqual(slugify("Top 10 of 2026"), "top-10-of-2026")

    def test_custom_separator(self):
        self.assertEqual(slugify("Hello World", separator="_"), "hello_world")

    def test_max_length_cuts_at_a_word(self):
        self.assertEqual(slugify("A very long title", max_length=10), "a-very")

    def test_max_length_shorter_than_first_word_gives_empty(self):
        self.assertEqual(slugify("Extraordinary", max_length=5), "")

    def test_only_symbols_gives_empty(self):
        self.assertEqual(slugify("!!!"), "")

    def test_is_idempotent(self):
        once = slugify("Crème brûlée, 2 ways!")
        self.assertEqual(slugify(once), once)


if __name__ == "__main__":
    unittest.main()
