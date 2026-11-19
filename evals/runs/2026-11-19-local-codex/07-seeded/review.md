The first priority is controlling what gets sent. Synthetic checks reproduced **three sends after a lost response**, and **eight sends to an unrelated recipient** when the model repeatedly requested them.

I reviewed this as a customer-facing mail sender, as described in the README. No files changed, no live services were called, and no emails were sent.

**1. Restrict recipients and order access in application code.**

- **Change:** In `assistant/agent.py:46` and `assistant/tools.py:19`, bind the recipient to a verified customer identity instead of accepting the model’s `to` argument. Scope order lookup to that customer. Move historical customer text out of the system instructions at `assistant/agent.py:33`; preserve the existing tone rules. These are my proposed implementation choices.
- **Why:** The model sees untrusted emails, reads private information, and can send it elsewhere. The wiki recommends enforcing boundaries outside the model: [containment](https://mishaevoma.github.io/aie-brain/concepts/sandboxing-and-permissions.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-10-18-loams-coding-agent-harnesses.md), [original](https://www.loams.dev/blog/coding-agent-harnesses).
- **Check run:** `rg -n '"to"|def lookup_order|def send_reply' assistant/tools.py` confirmed model-controlled addressing and an order lookup taking only an order ID. A mocked model successfully dispatched to `other@example.invalid`. This demonstrates missing enforcement, not a measured prompt-injection success rate.
- **Acceptance check:** Synthetic requests for another recipient or another customer’s order must be rejected before any outbound request.
- **Evidence / effort:** 18 October 2026, 32 days old; an evolving practice survey. Medium effort, potentially requiring backend authorization support; prevents misdirected replies and limits data exposure.

**2. Make sending idempotent and terminal.**

- **Change:** At `assistant/agent.py:10` and `:46`, separate read retries from write recovery. Use a stable reply identifier derived from the incoming `message_id`, with deduplication enforced by the mail service. Stop after confirmed delivery. Until deduplication exists, treat a send timeout as an unknown outcome requiring reconciliation.
- **Why:** A send can succeed before its response is lost. An instruction to “call once” cannot enforce that guarantee: [side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-10-15-vercel-running-durable-agents.md), [original](https://vercel.com/kb/guide/durable-ai-agents).
- **Check run:** `rg -n 'registry\[call.name\]|with_retries|MAX_STEPS' assistant/agent.py` showed every tool sharing the retry wrapper. An in-memory accepted-then-timeout simulation recorded **three accepted sends**; repeated successful tool proposals produced **eight sends**.
- **Acceptance check:** Inject a timeout after acceptance, repeat the tool proposal, and replay the incoming message. Together these must produce exactly one delivery.
- **Evidence / effort:** 15 October 2026, 35 days old; vendor implementation guidance. Medium effort, dependent on receiver support. Keep the eight-step cap, but enforce delivery separately.

**3. Make the test gate exercise behavior, then measure reply quality.**

- **Change:** In `tests/test_agent.py`, add offline flow tests using the existing client and registry injection points. Assert the **sent body and delivery state**, not the model’s closing narration. Add a separate model evaluation using 20–50 synthetic scenarios reflecting failure categories; never copy customer emails into test files. Preserve the short `AGENTS.md` and `make test` entry point.
- **Why:** The current quality assertions inspect `reply_to()`’s returned text, which can differ from the sent email. The README reports complaint-driven review. See [verification](https://mishaevoma.github.io/aie-brain/concepts/verification.md), [Osmani’s dated note](https://mishaevoma.github.io/aie-brain/sources/2026-11-17-osmani-claude-code-team-verification.md), [original](https://x.com/addyosmani/status/2122590683055993308); and [evals](https://mishaevoma.github.io/aie-brain/concepts/evals.md), [Anthropic’s dated note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), [original](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).
- **Check run:** `PYTHONDONTWRITEBYTECODE=1 ASSISTANT_LIVE_TESTS=0 make test` printed **`OK (skipped=4)`**. Only the import test ran.
- **Acceptance check:** The same command must exercise delivery, timeout recovery, recipient restrictions, and failure handling without credentials. Separately evaluate tracking correctness, refund policy, escalation, and tone before prompt/model changes.
- **Evidence / effort:** Sources are 2 days and approximately 10 months old. Small effort for offline tests; moderate effort plus model-call costs for evaluations. Mock tests verify orchestration, not model quality.

**4. Return actionable failures and continue processing the inbox.**

- **Change:** At `assistant/agent.py:46`, validate tool names and arguments, retry only transient failures, and return structured tool errors where recovery is possible. At `assistant/run.py:9`, isolate failures per input message and record an explicit failed or needs-review outcome. “A person will follow up” should correspond to an actual handoff.
- **Why:** Unknown tools raise `KeyError`; exhausted retries escape the loop, and the CLI has no per-message exception boundary. See [tool design](https://mishaevoma.github.io/aie-brain/concepts/tool-design.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-10-18-loams-coding-agent-harnesses.md), [original](https://www.loams.dev/blog/coding-agent-harnesses).
- **Check run:** `rg -n 'registry\[call.name\]|with_retries|MAX_STEPS' assistant/agent.py`; a synthetic unknown-tool call raised **`KeyError`**.
- **Acceptance check:** Process two synthetic messages with the first failing. The second must still run; permanent argument errors must not be retried.
- **Evidence / effort:** 18 October 2026, 32 days old. Small-to-medium effort; prevents one bad request from stopping the batch.

**5. Bound customer history before assembling context.**

- **Change:** In `assistant/context.py:19`, select relevant thread/order history and impose a size budget. Keep the three small policy documents loaded initially; their size does not justify a retrieval system.
- **Why:** Every historical email is currently included without filtering or limits. See [context engineering](https://mishaevoma.github.io/aie-brain/concepts/context-engineering.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-06-anthropic-components-of-agent-memory.md), [original](https://www.anthropic.com/research/components-of-agent-memory).
- **Check run:** `rg -n 'join|Every email' assistant/context.py`; a mocked history retained an unrelated **100,000-character** body dated 2000.
- **Acceptance check:** A large synthetic history must remain within a defined budget while retaining the current order’s relevant facts. Compare reply quality before adopting the filter.
- **Evidence / effort:** 6 November 2026, 13 days old. Small-to-medium effort; reduces input growth. Quality gains here remain unmeasured.

Reply **“make upgrade 1 and run the check”** to implement it.
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
Provenance: local wiki revision **`fe44a47` (2026-11-19)**, consulted **2026-11-19**; original-publication links came from its source notes. Live model behavior and backend safeguards remain unverified.
