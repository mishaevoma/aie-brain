**Make sending a checked, deduplicated application action before relying on this assistant for unattended replies.** I traced input → customer history → model → tools; offline simulations demonstrated duplicate sends, an unrelated recipient being accepted, and completion without sending anything.

I treated this as a customer-facing service based on the README; deployment and backend safeguards remain unverified. No files were changed.

1. **High: retries can send the same reply repeatedly.**  
   [assistant/agent.py:46](<work>/07-seeded/assistant/agent.py:46) retries every tool exception, including a timeout after mail acceptance. My simulated accepted-then-timeout send produced **three effects**. Two model-requested sends also both executed; conversely, text-only output returned without sending.

   Move final sending into application-controlled logic. Use the incoming `message_id` as a stable deduplication key enforced by the mail service, reject additional sends, and distinguish `sent`, `unresolved`, and `failed` outcomes. Until deduplication exists, treat ambiguous send failures as unresolved rather than retrying blindly. This follows the [side-effects guidance](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md) and [Temporal’s November 4, 2026 analysis](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure).

   **Proposed check:** simulate acceptance followed by timeout, repeat the input message, and request two sends. Expect one delivered reply; a text-only completion must not report delivery.

2. **High: customer boundaries are left to model-generated arguments.**  
   [assistant/tools.py:26](<work>/07-seeded/assistant/tools.py:26) looks up any supplied order ID, while `send_reply` accepts any recipient. The dispatcher accepted an unrelated recipient in my simulation. Historical email bodies also enter the system prompt, increasing exposure to untrusted instructions. Backend ownership enforcement is unknown.

   Bind the recipient to verified inbound identity outside the model, enforce customer ownership before returning order details, and keep historical emails separate from trusted instructions. These are my application-specific recommendations based on [Anthropic’s containment guidance, May 25, 2026](https://www.anthropic.com/research/how-we-contain-claude).

   **Proposed check:** request another customer’s order and an unrelated recipient, including instructions planted in history. Expect rejection before data disclosure or sending.

3. **High: the green test command does not establish reply correctness.**  
   [tests/test_agent.py:9](<work>/07-seeded/tests/test_agent.py:9) gates all behavioral tests behind live access. Tracking/refund assertions inspect the model’s returned text, which can differ from the sent body. The timeout test never injects a timeout.

   Add offline tests using the existing injectable client and registry; inspect captured send payloads and delivery state. Preserve the tone rules and use synthetic fixtures only. Add a small quality evaluation set for prompt changes. [Anthropic’s January 9, 2026 guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) recommends grading outcomes; its model examples are over six months old, but this testing distinction applies directly.

   **Verified:** `ASSISTANT_LIVE_TESTS=0 PYTHONDONTWRITEBYTECODE=1 make test` passed **one import test and skipped four behavioral tests**.

4. **Medium: customer history grows without a bound.**  
   [assistant/context.py:19](<work>/07-seeded/assistant/context.py:19) loads every past email into every request. There is no relevance filter or input budget.

   Keep the small policy KB, but bound history and select relevant threads. This follows [Anthropic’s September 29, 2025 context guidance](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), older evidence whose performance impact should be measured on your model.

   **Proposed check:** add extensive unrelated synthetic history; verify bounded input size and retention of the relevant order facts.

Keep the small tool set, explicit tone rules, eight-step limit, and injectable dependencies. They provide a straightforward base for these fixes.

*Provenance: public AI Engineering Brain and linked source notes consulted November 19, 2026. Verification was offline; no customer emails, live model calls, or mail services were used.*
