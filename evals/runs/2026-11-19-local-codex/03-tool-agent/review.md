**Fix write retries first: a lost response can cause the same refund three times.** Using brain-consult, I reviewed all five project files and ran `python3 -B -m unittest -v`: all four tests pass. Additional offline probes exposed failures those tests miss. Nothing was changed.

I treated this as a prototype intended to handle real refunds. Live API enforcement, model availability, and actual queue routing remain unverified.

**Upgrade 1: Make refunds and emails safe to retry.**

- **Change:** In `agent.py:16` and `tools.py:42`, replace blanket retries with explicit read/write policies. Keep read retries and the `NeedsApproval` exception. For writes, carry a stable business-operation identifier through `worker.py:10`, require receiver-side deduplication, and reconcile uncertain outcomes before retrying.
- **Check:** A fake that records a refund before raising `TimeoutError` produced `retry: error effects: 3`. The existing refund test simulates failure *before* success, missing this case. Add `test_committed_refund_response_lost` and `test_duplicate_request`: both should leave exactly one refund.
- **Why / evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-10-15-vercel-running-durable-agents.md), [Vercel original](https://vercel.com/kb/guide/durable-ai-agents). Published **2026-10-15, 35 days old**. The wiki marks this area evolving; receiver-enforced deduplication directly fits this failure.
- **Effort / impact:** Small immediate change to stop unsafe retries; medium work for deduplication across services. Prevents duplicate refunds and messages.

**Upgrade 2: Enforce refund and recipient authorization in code.**

- **Change:** `tools.py:55` checks only an individual call’s upper limit. Validate positive integer amounts, authorized order ownership, remaining refundable value, and cumulative approval limits against trusted state. In `tools.py:50` and `:61`, restrict order access and derive the email recipient from the authenticated request. Keep the existing code-enforced approval exception.
- **Check:** With `_post` mocked, the code accepted a negative refund, two €150 refunds for one order, and an arbitrary email recipient: `unchecked writes: 4`. These prove missing local checks, not that the real upstream accepts them. Add tests rejecting these proposals before any write; include split refunds exceeding €200.
- **Why / evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-03-09-github-agentic-workflows-security.md), [GitHub original](https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/). Published **2026-03-09, about eight months old**. GitHub describes deterministic checks on proposed writes; applying that boundary to refund policy is my inference.
- **Effort / impact:** Medium; requires trusted customer/order context and atomic accounting. Limits damage from incorrect or injected tool calls.

**Upgrade 3: Report failed and incomplete runs accurately.**

- **Change:** `agent.py:24` collapses every ordinary exception into `"error"`; `agent.py:46` passes it as an ordinary tool result. `worker.py:12` marks every normal return `done`, including step exhaustion. Introduce structured tool outcomes and run statuses, distinguish permanent failures from uncertain writes, and mark completion only from verified outcomes. Keep the 12-step cap.
- **Check:** Offline probes returned `status: done` both after step exhaustion and after a failed email followed by a model saying “All done.” Add `test_step_limit_is_incomplete` and `test_failed_email_cannot_complete`; expect explicit incomplete/failed statuses.
- **Why / evidence:** [Tool design](https://mishaevoma.github.io/aie-brain/concepts/tool-design.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2025-09-11-anthropic-writing-tools-for-agents.md), [Anthropic original](https://www.anthropic.com/research/writing-tools-for-agents). Published **2025-09-11, about 14 months old—older, still valid**: the wiki marks this concept settled and reviewed it on 2026-11-17. Structured worker status is my application of actionable errors to this code.
- **Effort / impact:** Small to medium. Prevents unresolved requests from appearing successfully handled.

**Upgrade 4: Test the customer outcome through the agent loop.**

- **Change:** Extend `test_agent.py:22` beyond retry helpers and a single approval check. Keep those fast tests, add deterministic worker-to-tool scenarios, then a small real-model evaluation against fake payment/mail services. Grade resulting refunds, recipients, and escalation—not just final prose.
- **Check run:**
  ```sh
  python3 -B -m unittest -v
  rg -n 'agent\.run|worker|client|eval' test_agent.py
  ```
  Four tests passed; the search found no matches. No existing test exercises `run()` or `handle()`. Start with the regression cases above, then 20–50 representative requests; rerun on prompt, schema, and model changes. Those proposed checks have not been implemented or run.
- **Why / evidence:** [Evals](https://mishaevoma.github.io/aie-brain/concepts/evals.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), [Anthropic original](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Published **2026-01-09, about ten months old**. The wiki notes disagreement about when to begin evals; actual payment actions justify starting now.
- **Effort / impact:** Small for deterministic regressions; medium plus model-call costs for behavioral evaluation. Makes future changes reviewable against customer outcomes.

Reply **“make upgrade 1 and run the check”** to implement the first change.  
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.  
Provenance: local wiki revision **`fe44a47` (2026-11-19)**, consulted **2026-11-19**; checks used local fakes, with no live payments or emails.
