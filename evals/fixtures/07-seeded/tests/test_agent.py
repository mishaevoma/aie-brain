import os
import unittest

from assistant import agent, tools

LIVE = os.environ.get("ASSISTANT_LIVE_TESTS") == "1"


@unittest.skipUnless(LIVE, "needs the shop sandbox and an API key")
class ReplyTest(unittest.TestCase):
    EMAIL = {
        "message_id": "m-1",
        "customer_id": "c-204",
        "from": "dana@example.com",
        "subject": "Where is my fern?",
        "body": "Order 5512 was due on Monday.",
    }

    def test_late_order_reply_has_tracking_link(self):
        self.assertIn("track", agent.reply_to(self.EMAIL).lower())

    def test_reply_never_promises_a_refund(self):
        email = dict(self.EMAIL, subject="Broken pot", body="The pot arrived cracked. I want my money back.")
        self.assertNotIn("we will refund", agent.reply_to(email).lower())

    def test_reply_is_sent_once(self):
        sent = []
        registry = dict(tools.TOOLS, send_reply=lambda **kw: sent.append(kw) or {"ok": True})
        agent.reply_to(self.EMAIL, registry=registry)
        self.assertEqual(len(sent), 1)


@unittest.skipUnless(LIVE, "needs the shop sandbox and an API key")
class RetryTest(unittest.TestCase):
    def test_lookup_survives_one_timeout(self):
        self.assertIn("status", agent.with_retries(tools.lookup_order, {"order_id": "5512"}))


class ImportTest(unittest.TestCase):
    def test_modules_import(self):
        self.assertTrue(callable(agent.reply_to))


if __name__ == "__main__":
    unittest.main()
