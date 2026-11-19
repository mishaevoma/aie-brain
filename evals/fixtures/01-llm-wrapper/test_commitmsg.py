import unittest
from types import SimpleNamespace

import commitmsg


class FakeClient:
    """Stands in for the Anthropic client and records what it was sent."""

    def __init__(self, text):
        self.sent = None
        self.messages = SimpleNamespace(create=self._create)
        self._text = text

    def _create(self, **kwargs):
        self.sent = kwargs
        return SimpleNamespace(content=[SimpleNamespace(text=self._text)])


class GenerateTest(unittest.TestCase):
    def test_returns_the_reply_without_whitespace(self):
        client = FakeClient("  Fix date parsing in importer\n")
        self.assertEqual(commitmsg.generate("diff --git a/x b/x", client), "Fix date parsing in importer")

    def test_prompt_contains_the_diff_and_the_rules(self):
        client = FakeClient("ok")
        commitmsg.generate("diff --git a/x b/x", client)
        prompt = client.sent["messages"][0]["content"]
        self.assertIn("diff --git a/x b/x", prompt)
        self.assertIn("imperative mood", prompt)

    def test_uses_the_configured_model(self):
        client = FakeClient("ok")
        commitmsg.generate("diff", client)
        self.assertEqual(client.sent["model"], commitmsg.MODEL)


if __name__ == "__main__":
    unittest.main()
