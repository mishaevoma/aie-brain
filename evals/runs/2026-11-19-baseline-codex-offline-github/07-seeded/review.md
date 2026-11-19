Found four issues worth fixing before relying on automatic sending. These are independent code findings: I read the [brain-consult skill](https://github.com/mishaevoma/aie-brain/blob/main/.agents/skills/brain-consult/SKILL.md), but its procedure and public wiki were inaccessible, so the requested source-backed comparison remains incomplete.

1. **High — Retries can send duplicate replies.** [assistant/agent.py:46](assistant/agent.py#L46) retries every tool after any exception. If the mail service accepts a message but its response times out, the same message is sent again. An offline simulation produced three sends. Add server-enforced idempotency keyed by incoming `message_id`; distinguish read retries from uncertain write outcomes.

2. **High — Tool permissions aren’t bound to the customer.** [assistant/tools.py:26](assistant/tools.py#L26) accepts arbitrary order IDs, and `send_reply` accepts arbitrary recipients. The dispatcher executes model arguments without checking ownership or recipient identity. Historical customer emails also enter the system prompt through [assistant/context.py:19](assistant/context.py#L19). Bind tools to the authenticated customer, enforce order ownership, fix the recipient in application code, and treat email history as untrusted data. Backend authorization was unavailable to verify.

3. **High — Completion doesn’t guarantee exactly one reply.** [assistant/agent.py:41](assistant/agent.py#L41) returns successfully when the model produces text without sending, and executes repeated send calls without a guard. Offline simulations confirmed both zero-send completion and two sends in one response. Track delivery explicitly, reject repeated sends, and return a distinct unsent or escalation outcome.

4. **Medium — Tests don’t validate the delivered message.** [tests/test_agent.py:19](tests/test_agent.py#L19) checks the model’s final text, which can differ from the `send_reply` body. All behavioral tests require live services; the retry test doesn’t inject a timeout. Add synthetic, offline tests that capture outgoing messages and exercise timeout-after-acceptance, repeated sends, unauthorized lookups, and text-only completion.

`make test` completed successfully: **1 passed, 4 skipped**. Additional checks used fake clients and tools; no messages were sent or files changed.

To complete the skill-based comparison, provide its `references/project-review.md` and an accessible wiki copy.
