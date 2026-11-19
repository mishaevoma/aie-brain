**Make refund retries safe first: a lost response can currently trigger a second payment.** I traced `worker.handle → agent.run → call_with_retry → issue_refund` and reproduced two simulated payment commits when the first succeeded but its response timed out.

1. **High: retries can duplicate refunds and emails.** [agent.py:16](agent.py:16) retries every exception, while [tools.py:42](tools.py:42) sends writes without an idempotency key. The existing refund test simulates failure before a payment commits, so it misses this case. First verify the payments API’s deduplication contract; then persist a business operation ID and reuse it across retries and queue redelivery. Until that works, treat write timeouts as unknown outcomes requiring reconciliation.

   **Proposed check:** simulate “commit, then timeout” and redeliver the request. Expect exactly one payment and one email.

   This follows the wiki’s [side-effect guidance](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md) and its [Vercel source, 2026-10-15](https://mishaevoma.github.io/aie-brain/sources/2026-10-15-vercel-running-durable-agents.md): receiver-enforced deduplication remains necessary even with a durable runtime.

2. **High: splitting a refund bypasses the €200 approval boundary.** [tools.py:55](tools.py:55) checks each call independently. With the HTTP write mocked, two €150 calls for the same order submitted €300 without approval. The existing exception correctly blocks a single oversized call; retain it, but enforce the limit against the refund request’s cumulative amount and validated refundable balance, atomically across runs.

   **Proposed check:** request two €150 refunds for one case. Expect approval before the cumulative amount exceeds €200.

   This design recommendation applies the deterministic write checks described in [GitHub’s source, 2026-03-09](https://mishaevoma.github.io/aie-brain/sources/2026-03-09-github-agentic-workflows-security.md). That source is over six months old and describes batch automation; the refund-specific application is my judgment.

3. **Medium: unfinished requests are reported as done.** [agent.py:48](agent.py:48) returns a string on step exhaustion, and [worker.py:12](worker.py:12) labels every normal return `done`. A fake model repeatedly requesting lookups reproduced `status: done` with `summary: Stopped: step limit reached.` Return structured outcomes and reserve `done` for verified completion.

   **Proposed check:** exhaust the step budget and simulate exhausted tool retries. Expect explicit unresolved/error outcomes, never `done`.

   The wiki’s [Temporal source, 2026-11-04](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md) supports separating accepted results, unresolved exits, and execution errors.

All four existing tests passed. Additional reproductions used mocks only; no files changed or live payments were made. External API deduplication and actual support-queue routing remain unverified.

Reviewed against the published AI Engineering Brain and linked raw review procedure, consulted 2026-11-19.
