import unittest
from types import SimpleNamespace

import crew


class ScriptedClient:
    """Answers each role with a canned reply and records the calls."""

    def __init__(self, critic_replies):
        self.calls = []
        self.critic_replies = list(critic_replies)
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        role = kwargs["system"]
        if role == crew.CRITIC:
            text = self.critic_replies.pop(0)
        elif role == crew.WRITER:
            text = "## This week\n- Faster dashboard"
        else:
            text = "ok"
        return SimpleNamespace(content=[SimpleNamespace(text=text)])


class CrewTest(unittest.TestCase):
    def test_returns_notes_when_the_critic_approves(self):
        client = ScriptedClient(["APPROVED"])
        self.assertIn("Faster dashboard", crew.run([{"number": 1, "title": "t", "labels": [], "body": "b"}], client))
        self.assertEqual(len(client.calls), 4)

    def test_writer_tries_again_after_feedback(self):
        client = ScriptedClient(["Mention the breaking change.", "APPROVED"])
        crew.run([{"number": 1, "title": "t", "labels": [], "body": "b"}], client)
        roles = [call["system"] for call in client.calls]
        self.assertEqual(roles.count(crew.WRITER), 2)
        self.assertEqual(roles.count(crew.CRITIC), 2)


if __name__ == "__main__":
    unittest.main()
