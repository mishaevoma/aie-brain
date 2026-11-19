**The main upgrade is making refund retries safe.** The current wrapper can issue a refund multiple times after a timeout, while all four existing tests pass.

I reviewed this as a prototype intended to handle real refunds. No files changed. I ran `python3 -B -m unittest -v` and local failure probes with mocked services; no payments, emails, or model calls were made.

**Upgrade 1: Prevent duplicate refunds and emails.**

- **Observed:** `agent.py:16–26` retries every exception for every tool. `tools.py:42–62` sends writes without an idempotency key. A fake payment that committed before timing out was executed three times, then reported `"error"`.
- **Change:** Keep retries for transient lookup failures. Give writes a stable business-operation key enforced by the receiving service, including across queue redelivery. Until that exists, treat a write timeout as an unknown outcome requiring reconciliation. Keep the existing immediate propagation of `NeedsApproval`.
- **Check run:** With a fake that records a committed payment and then raises `TimeoutError`:
  ```python
  agent.call_with_retry('issue_refund', {'order_id':'A1','amount_cents':4200}, {'issue_refund':committed_then_timeout}, sleep=lambda _:None)
  ```
  Result: **three committed writes**. Add a regression test covering lost responses and redelivery; expect exactly one refund.
- **Evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md) → [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md) → [Temporal publication](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure). Published **4 November 2026, 15 days old**. This is implementation-review evidence, not a measured reliability guarantee.
- **Effort and impact:** Small immediate retry-policy fix; larger integration for receiver-side deduplication. Prevents duplicate financial actions and customer messages.

**Upgrade 2: Enforce refund and recipient policy in code.**

- **Observed:** `tools.py:55` checks only whether an individual amount exceeds €200. It forwards negative amounts and repeated €150 refunds without consulting order state. `send_email` accepts any recipient. The instruction to refund only returned items exists solely in the prompt.
- **Change:** Bind tools to a trusted customer/order context. Validate positive integer amounts, returned-item eligibility, remaining refundable balance, and the aggregate amount requiring approval. Derive the email recipient from that context. Keep the existing €200 approval exception.
- **Check run:** With `_post` mocked:
  ```python
  tools.issue_refund('A1', -1)
  ```
  Result: **negative refund forwarded**. Additional probes forwarded two €150 requests and an arbitrary email destination. Add tests asserting invalid or unauthorized actions never reach `_post`; include split-refund and cross-customer cases.
- **Evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md) → [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-03-09-github-agentic-workflows-security.md) → [GitHub publication](https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/). Published **9 March 2026, about eight months old**. GitHub describes deterministic checks on proposed writes; the refund-specific rules above are my application of that principle.
- **Effort and impact:** Moderate; requires trusted identity and order-state integration. Prevents model mistakes or injected instructions from directly authorizing inappropriate actions. Upstream protections may exist, but this repository does not establish them.

**Upgrade 3: Report incomplete runs as incomplete.**

- **Observed:** `agent.py:48` returns a string on step exhaustion; `worker.py:12` labels every normal return `"done"`. Tool failures become the undifferentiated string `"error"`.
- **Change:** Return structured outcomes distinguishing completion, approval, unresolved execution, and failure. Preserve actionable tool errors and confirmed effects. Keep the 12-step cap and existing approval status.
- **Check run:** Using a fake model that repeatedly requests a lookup:
  ```python
  worker.handle({'id':'M1','text':'refund'})
  ```
  After all 12 steps, the result was:
  ```text
  {'id': 'M1', 'status': 'done', 'summary': 'Stopped: step limit reached.'}
  ```
  Add worker-through-agent tests for step exhaustion, exhausted tool retries, and successful completion; only confirmed completion should produce `"done"`.
- **Evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md) → [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md) → [Temporal publication](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure). **4 November 2026, 15 days old**; it explicitly separates accepted, unresolved, and failed outcomes.
- **Effort and impact:** Small to moderate. Makes unsuccessful requests visible to the queue consumer and support team.

The simple loop, bounded execution, approval exception, and documented offline test command are worth keeping. Existing tests establish retry mechanics and the single-call approval threshold; they do not establish model quality, safe recovery, or end-to-end refund completion.

Reply **“make upgrade 1 and run the check”** to implement the first change.  
Brain-consult is already installed in this project.  
Provenance: local wiki revision **`fe44a47` (2026-11-19)**, consulted **19 November 2026**; live service behavior remains unverified.
