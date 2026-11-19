I couldn’t retrieve the linked review guide, so this is a code review rather than a verified application of that guide.

Found five issues, ordered by priority:

1. **[P1] Sending retries can duplicate emails.** `assistant/agent.py:46` retries every tool call, including `send_reply`. If the mail service accepts a message but its response times out, the same message is submitted again. A mocked reproduction recorded three accepted sends. Add server-backed idempotency using the incoming `message_id`, plus a guard against repeated model send calls.

2. **[P1] Tool access isn’t bound to the customer.** `assistant/tools.py:26–36` accepts model-selected order IDs and recipients without checking ownership or binding the recipient to the incoming email. The mocked loop successfully sent to a different address. Enforce recipient selection in application code and verify order ownership before exposing order details.

3. **[P1] Customer email history becomes system instructions.** `assistant/context.py:21–22` concatenates raw historical emails into content inserted into the system prompt at `assistant/agent.py:33`. This gives attacker-controlled text a privileged instruction position. Keep history in explicitly untrusted message content, separate from policies, and enforce tool permissions independently.

4. **[P2] The loop can finish without sending a reply.** `assistant/agent.py:42–43` returns any text-only response as the result, even when no send occurred. The mocked reproduction returned `"Draft only"` with zero sends. Track delivery explicitly and distinguish an unsent draft from successful completion.

5. **[P2] Tests don’t verify the actual outgoing reply.** `tests/test_agent.py:19–24` checks returned model text, which may be a post-send acknowledgement rather than the sent body. The retry test also never injects a timeout. Capture outgoing payloads and add deterministic mocked tests for delivery, ambiguous failures, and customer boundaries.

Validation: `make test` passed with **one test executed and four skipped**. Additional in-memory reproductions confirmed missing delivery, repeated sends, unrestricted recipient selection, and duplicate retry effects. No files changed.
