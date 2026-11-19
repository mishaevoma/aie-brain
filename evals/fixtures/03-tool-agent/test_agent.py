import unittest

import agent
import tools


class Flaky:
    """A tool that times out a set number of times before it answers."""

    def __init__(self, failures, result):
        self.failures = failures
        self.result = result
        self.calls = []

    def __call__(self, **arguments):
        self.calls.append(arguments)
        if len(self.calls) <= self.failures:
            raise TimeoutError("upstream timed out")
        return self.result


class RetryTest(unittest.TestCase):
    def test_lookup_is_retried_until_it_answers(self):
        lookup = Flaky(failures=2, result={"order_id": "A1", "total_cents": 4200})
        result = agent.call_with_retry("lookup_order", {"order_id": "A1"}, {"lookup_order": lookup}, sleep=lambda _: None)
        self.assertEqual(result["total_cents"], 4200)
        self.assertEqual(len(lookup.calls), 3)

    def test_refund_is_retried_after_a_timeout(self):
        refund = Flaky(failures=1, result={"refund_id": "R9"})
        result = agent.call_with_retry(
            "issue_refund", {"order_id": "A1", "amount_cents": 4200}, {"issue_refund": refund}, sleep=lambda _: None
        )
        self.assertEqual(result, {"refund_id": "R9"})
        self.assertEqual(len(refund.calls), 2)

    def test_gives_up_after_three_attempts(self):
        dead = Flaky(failures=99, result=None)
        result = agent.call_with_retry("send_email", {"to": "a@example.com", "subject": "s", "body": "b"}, {"send_email": dead}, sleep=lambda _: None)
        self.assertEqual(result, "error")
        self.assertEqual(len(dead.calls), 3)


class ApprovalTest(unittest.TestCase):
    def test_large_refunds_are_not_issued(self):
        with self.assertRaises(tools.NeedsApproval):
            tools.issue_refund("A1", 25_000)


if __name__ == "__main__":
    unittest.main()
