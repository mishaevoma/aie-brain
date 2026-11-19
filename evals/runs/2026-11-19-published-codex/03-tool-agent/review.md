The first upgrade should be **making refunds safe to retry**. All four existing tests pass, but local failure simulations exposed four safeguards missing from the implementation.

I followed the supplied review procedure, treating this as a prototype intended to handle real payments. No files changed, and no live payment, mail, or model calls ran.

**1. Prevent duplicate payments after a timeout — high priority.**

[agent.py:16](agent.py:16) retries every exception from every tool. [tools.py:42](tools.py:42) sends writes without an idempotency key. A payment can commit before its response is lost; retrying can then pay again. The existing refund test only simulates failure before success.

- **Change:** Keep bounded retries for reads. For refunds and emails, require receiver-enforced deduplication using a stable business operation identifier that survives retries and queue redelivery. Until supported, treat write timeouts as unknown outcomes requiring reconciliation.
- **Check:** The simulation below prints `retry: error 3`: three simulated commits, followed by an error. Add a commit-then-timeout regression test and a redelivery test; both must produce exactly one external effect.
- **Why and evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [Temporal source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md), [original publication](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure), **4 November 2026 — 15 days old**. This is architectural guidance, not a measured guarantee.
- **Effort and impact:** Small immediate retry-policy change; moderate work for durable deduplication. Prevents duplicate refunds and messages.

**2. Enforce refund policy across the request — high priority.**

[tools.py:55](tools.py:55) checks only whether one call exceeds €200. Two €150 calls for the same order both pass. The instruction to refund only eligible returned items exists solely in [agent.py:10](agent.py:10).

- **Change:** Keep the explicit `NeedsApproval` exception. Before payment, validate the order, eligible amount, previous refunds, and cumulative proposed refund in trusted code. Evaluate the complete request before issuing partial payments; enforce totals atomically at the payment boundary.
- **Check:** The simulation prints `refund cents: 30000` without approval. Add tests for a split €300 request, over-refunding, and invalid amounts. Expect approval before payment for the €300 request and rejection of invalid amounts.
- **Why and evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [Linear source note](https://mishaevoma.github.io/aie-brain/sources/2026-08-10-linear-how-we-built-linear-agent.md), [original publication](https://linear.app/now/how-we-built-linear-agent), **10 August 2026 — 101 days old**. Linear advocates constraints in tools and context-dependent approval; the refund-specific design is my application of that advice.
- **Effort and impact:** Moderate, depending on order and payment APIs. Prevents splitting requests around the approval threshold and refunding ineligible amounts.

**3. Bind data access and email delivery to the verified customer — high priority.**

Customer text enters [agent.py:34](agent.py:34), while the model chooses both order IDs and the unrestricted `to` argument in [tools.py:61](tools.py:61). No customer authorization context reaches these tools.

- **Change:** Derive customer identity and reply destination from trusted inbox metadata. Scope order access to that customer and have code select the recipient. Keep the small, explicit tool registry.
- **Check:** The simulation prints `recipient: outsider@example.org`, showing that the tool forwards any supplied address. Add tests where proposed tool calls access another customer’s order or choose another recipient; both must be blocked before network access.
- **Why and evidence:** [Permissions and containment](https://mishaevoma.github.io/aie-brain/concepts/sandboxing-and-permissions.md), [Willison source note](https://mishaevoma.github.io/aie-brain/sources/2025-06-16-willison-lethal-trifecta.md), [original publication](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), **16 June 2025 — about 17 months old**. **Older, still valid:** the evolving wiki page was reviewed on 17 November 2026, and this code still combines untrusted text, order access, and external messaging. An actual model-driven exploit was not tested.
- **Effort and impact:** Moderate. Limits unauthorized refunds and disclosure of customer information.

**4. Distinguish unfinished runs from successful completion.**

[agent.py:48](agent.py:48) returns a string on step exhaustion, and [worker.py:12](worker.py:12) marks every normal return `done`. Exhausted tool retries likewise become a bare `"error"` result without an explicit error flag.

- **Change:** Keep `MAX_STEPS`, but return structured outcomes such as completed, unresolved, needs approval, and failed. Propagate tool errors explicitly and make the worker preserve the outcome.
- **Check:** Both a 12-step fake-model run and the shortened simulation below produced `status: done` with `Stopped: step limit reached.` Add worker tests for step exhaustion and exhausted tool retries; neither should report successful completion.
- **Why and evidence:** [Side effects](https://mishaevoma.github.io/aie-brain/concepts/side-effects.md), [Temporal source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md), [original publication](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure), **4 November 2026 — 15 days old**. It explicitly distinguishes accepted outcomes, unresolved exits, and execution errors.
- **Effort and impact:** Small. Stops unfinished customer requests being represented as completed.

These are the checks I ran. The existing suite passed with `python3 -B -m unittest -v`. This additional command reproduced the four gaps using local fakes:

```sh
python3 -B - <<'PY'
from unittest.mock import patch
import agent, tools, worker
commits = []
def lost_response(**kw):
    commits.append(kw)
    raise TimeoutError()
print('retry:', agent.call_with_retry('issue_refund', {}, {'issue_refund': lost_response}, sleep=lambda _: None), len(commits))
with patch.object(tools, '_post', return_value={}) as post:
    tools.issue_refund('A1', 15000)
    tools.issue_refund('A1', 15000)
    print('refund cents:', sum(c.args[1]['amount_cents'] for c in post.call_args_list))
    tools.send_email('outsider@example.org', 'Details', 'private data')
    print('recipient:', post.call_args.args[1]['to'])
with patch.object(agent, 'MAX_STEPS', 0), patch.object(agent, 'run', wraps=agent.run) as run:
    original = run._mock_wraps
    run.side_effect = lambda text: original(text, client=object())
    print('worker:', worker.handle({'id': 'm1', 'text': 'refund'}))
PY
```

The proposed regression tests have **not** been added or run. External API protections, model availability, and real model task quality remain unverified.

Reply **“make upgrade 1 and run the check”** to implement the first change.  
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.  
Provenance: published wiki revision **`9b70bc0 2026-11-19`**, consulted **19 November 2026**; procedure read from the linked GitHub copy.
