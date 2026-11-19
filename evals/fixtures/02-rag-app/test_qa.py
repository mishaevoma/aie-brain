import unittest

import ingest
import qa


class ChunkTest(unittest.TestCase):
    def test_chunks_are_at_most_400_characters(self):
        pieces = ingest.chunk("a" * 1000)
        self.assertEqual([len(p) for p in pieces], [400, 400, 200])

    def test_nothing_is_dropped(self):
        text = "Expense claims must be filed within 60 days. " * 30
        self.assertEqual("".join(ingest.chunk(text)), text)


class CosineTest(unittest.TestCase):
    def test_identical_vectors_score_one(self):
        self.assertAlmostEqual(qa.cosine([1.0, 2.0], [1.0, 2.0]), 1.0)

    def test_orthogonal_vectors_score_zero(self):
        self.assertAlmostEqual(qa.cosine([1.0, 0.0], [0.0, 1.0]), 0.0)


class PromptTest(unittest.TestCase):
    def test_prompt_has_question_excerpts_and_history(self):
        prompt = qa.build_prompt(
            "How many days of leave?",
            [{"text": "Staff get 25 days of annual leave."}],
            [{"role": "user", "text": "hi"}],
        )
        self.assertIn("25 days", prompt)
        self.assertIn("user: hi", prompt)
        self.assertIn("How many days of leave?", prompt)


if __name__ == "__main__":
    unittest.main()
