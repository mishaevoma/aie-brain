**Fix the send boundary and duplicate-delivery handling first.** The project is small and understandable, but its green test command currently proves only that modules import.

I followed the linked review procedure, reviewing both the AI feature and repository instructions. I assumed real customer use because the README describes automatic sending. No files changed, no live APIs were called, and all diagnostic inputs were synthetic.

**1. Bind tool permissions to the current customer.**

- **Observed:** [assistant/tools.py:26](assistant/tools.py#L26) fetches any model-supplied order ID, and `send_reply` accepts any recipient. Historical customer text is also inserted into the system prompt at [assistant/agent.py:33](assistant/agent.py#L33).
- **Change:** Bind the recipient to a verified customer identity in application code; enforce order ownership before returning data. Put historical emails in explicitly untrusted context. Keep the existing tone rules and small tool set. Prompt separation supplements authorization; it cannot replace it.
- **Check run:** An offline fake-model probe, executed with `python3 -B -`, supplied a different recipient. Output: `unbound_recipient: other@example.invalid`. This demonstrates missing application enforcement, not a measured prompt-injection success rate. Add tests requiring rejection of an unauthorized recipient and another customer’s order before any external action.
- **Why/evidence:** [Containment guidance](https://mishaevoma.github.io/aie-brain/concepts/sandboxing-and-permissions.md), [source note dated 2026-05-25](https://mishaevoma.github.io/aie-brain/sources/2026-05-25-anthropic-how-we-contain-claude.md), [original Anthropic publication](https://www.anthropic.com/research/how-we-contain-claude). About six months old; the specific authorization design above is my application of that guidance. Backend protections remain unverified.
- **Effort/impact:** Medium, depending on shop authentication; restricts unintended disclosure and delivery.

**2. Make sending idempotent and enforce one reply per incoming message.**

- **Observed:** [assistant/agent.py:46](assistant/agent.py#L46) retries every tool after any exception. [assistant/tools.py:31](assistant/tools.py#L31) supplies no idempotency key. “Call this once” is only a tool description.
- **Change:** Keep bounded retries for transient read failures. For sending, use a stable business key derived from the incoming message, enforce deduplication at the receiver, and reject repeated send proposals. Until receiver-side deduplication exists, record ambiguous delivery outcomes for reconciliation instead of blindly retrying.
- **Check run:** Offline probes with `python3 -B -` printed `ambiguous_send_deliveries: 3` when delivery preceded a timeout, and `same_turn_sends: 2` for two send proposals. Add regression tests for response loss, repeated proposals, and reprocessing the same message; each should produce exactly one delivery.
- **Why/evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [source note dated 2026-11-04](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md), [original Temporal publication](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure). Fifteen days old; architectural failure analysis, not measured incident frequency.
- **Effort/impact:** Medium; prevents duplicate customer emails across retries and restarts.

**3. Return explicit delivery outcomes and isolate failures per email.**

- **Observed:** [assistant/agent.py:42](assistant/agent.py#L42) returns text successfully without requiring a send. Unknown tools and exhausted retries escape as exceptions. [assistant/run.py:8](assistant/run.py#L8) has no per-message exception boundary, so one failure stops the remaining input.
- **Change:** Return structured outcomes such as `sent`, `needs_review`, and `delivery_unknown`, based on actual tool results. Handle expected failures per input record and continue processing subsequent records. Keep `MAX_STEPS`, but turn exhaustion into an actionable unresolved outcome.
- **Check run:** Offline probes with `python3 -B -` printed `text_only_result: 'Your tracking link' sent: 0` and `unknown_tool_escapes: KeyError`. Add tests requiring a text-only response to remain unsent, and a failed first input to leave a valid second input processable.
- **Why/evidence:** [Side effects and unresolved outcomes](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [2026-11-04 source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md), [original](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure). Fifteen days old; applying explicit outcome categories to this CLI is my recommendation.
- **Effort/impact:** Small to medium; prevents silent non-delivery and batch interruption.

**4. Make the mandatory test command exercise behavior offline.**

- **Observed:** [tests/test_agent.py:9](tests/test_agent.py#L9) skips every behavioral test unless live services are enabled. The retry test does not inject a timeout.
- **Change:** Keep `make test` and the concise `AGENTS.md`. Use the existing client/registry injection points plus mocked context to test actual loop behavior, failure handling, and captured sends without credentials. Keep all fixtures synthetic.
- **Check run:**

  ```sh
  PYTHONDONTWRITEBYTECODE=1 ASSISTANT_LIVE_TESTS=0 make test
  ```

  Result: **5 tests, 4 skipped, 1 import check passed**. Afterward, this same command should execute the behavioral regressions above without network access.
- **Why/evidence:** [Verification](https://mishaevoma.github.io/aie-brain/concepts/verification.md), [source note dated 2026-11-17](https://mishaevoma.github.io/aie-brain/sources/2026-11-17-osmani-claude-code-team-verification.md), [original publication](https://x.com/addyosmani/status/2122590683055993308). Two days old; one team’s practice, not a universal performance guarantee.
- **Effort/impact:** Small; makes the repository’s required gate meaningful.

**5. Evaluate the actual outgoing message before changing prompts or models.**

- **Observed:** [tests/test_agent.py:19](tests/test_agent.py#L19) checks the returned assistant text, which can differ from the sent body. Checking for `"track"` or absence of one refund phrase does not establish correct support behavior. The README reports complaint-driven quality review.
- **Change:** Add a separate real-model evaluation using synthetic scenarios and intercepted delivery. Start with 20–50 cases covering tracking accuracy, refunds, uncertain information, malicious instructions, and tone. Grade the captured recipient/body and delivery outcome. Preserve the existing tone rules; run the suite on prompt, schema, and model changes.
- **Check run:** The test command above skips these checks; the text-only probe also demonstrates that a tracking assertion can pass with zero sends. Proposed acceptance check: a real-model scenario must produce one captured message containing the correct fixture tracking URL and no unauthorized refund promise. This evaluation was **not run**.
- **Why/evidence:** [Evals](https://mishaevoma.github.io/aie-brain/concepts/evals.md), [source note dated 2026-01-09](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), [original Anthropic publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). About ten months old; outcome-based grading fits this customer-facing application.
- **Effort/impact:** Medium plus ongoing model cost; detects quality regressions that deterministic loop tests cannot.

**6. Bound customer history while preserving relevant context.**

- **Observed:** [assistant/context.py:19](assistant/context.py#L19) includes every historical email without a size or relevance limit.
- **Change:** Keep the three short policy documents loaded directly. Budget history separately, prefer the current thread and relevant order references, and provide a way to retrieve omitted material.
- **Check run:** Synthetic history probes with `python3 -B -` grew context from **1,758 characters for one email to 1,025,733 for 1,000 emails**. Add a test enforcing the chosen budget while retaining relevant order information; measure answer quality separately.
- **Why/evidence:** [Context engineering](https://mishaevoma.github.io/aie-brain/concepts/context-engineering.md), [source note dated 2025-09-29](https://mishaevoma.github.io/aie-brain/sources/2025-09-29-anthropic-context-engineering.md), [original Anthropic publication](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents). About fourteen months old: **older, still valid** as budget guidance; the wiki marks it settled and reviewed on 2026-11-17. No model-specific quality loss was measured here.
- **Effort/impact:** Small to medium; bounds input growth and reduces irrelevant history.

Reply **“make upgrade 1 and run the check”** to implement the first change.  
Optional repeat-review installation: `npx skills add mishaevoma/aie-brain --skill brain-consult`.  
Provenance: published wiki revision **9b70bc0, 2026-11-19**, consulted **2026-11-19**; live model behavior and backend enforcement remain unverified.
