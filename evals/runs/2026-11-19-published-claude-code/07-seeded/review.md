Review of inbox-assistant (read-only; nothing in the project was changed). I read the README, AGENTS.md, Makefile and every Python file. I ran `make test`'s command, and nothing else.

I assumed this is a live service that sends real emails to real customers, so a failure costs customer trust and possibly duplicate or wrong mail. There are four upgrades, ranked by cost of failure and then by effort.

**Upgrade 1: Make `send_reply` safe to run twice, so a timeout can't email a customer twice.** `agent.py:46` wraps every tool call, including the `send_reply` POST in `tools.py:31-37`, in the same 3-attempt retry. A send that succeeds but times out on the response gets sent again.

- **Change.**
  - Split the policy per tool. Retry `lookup_order`, which is a read. Do not blind-retry `send_reply`.
  - Send an idempotency key with the send, for example derived from `message_id`, and have the mail API deduplicate on it.
  - Also catch `Exception` less broadly in `with_retries` (`agent.py:15`).
  - Keep the step cap (`MAX_STEPS = 8`) and the 10-second timeouts. Those are good.
- **Why.**
  - Wiki page: [Upgrading an existing AI app, check 6](https://mishaevoma.github.io/aie-brain/playbooks/upgrading-an-agent-app.md).
  - Source notes: [What survives failure, Nov 2026](https://mishaevoma.github.io/aie-brain/sources/2026-11-04-temporal-deciding-what-survives-failure.md) and [Running durable agents, Oct 2026](https://mishaevoma.github.io/aie-brain/sources/2026-10-15-vercel-running-durable-agents.md).
  - Originals: https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure and https://vercel.com/kb/guide/durable-ai-agents.
- **Check.**
  - Shows the problem today. I ran `grep -n "with_retries(registry" assistant/agent.py`, which printed `46: output = with_retries(registry[call.name], call.input)`. Running `grep -ric idempot assistant` finds no matches (I ran an equivalent count and got 0).
  - Passes after the fix, and I have not run this one. Add an offline test where a fake `send_reply` raises once after recording the call. It should assert that the receiver sees one send, or the same key twice.
- **Evidence.** Both sources are from Oct to Nov 2026, so they are current. They are practitioner guidance, not measurements on a specific model.
- **Effort and impact.** Small, about an hour. It prevents duplicate customer emails.

**Upgrade 2: Add a small eval that runs offline and fails when replies get worse.** Every test that touches the feature (4 of 5) is skipped unless `ASSISTANT_LIVE_TESTS=1`. `make test` is green while proving only that the module imports. The README says quality is judged by "reading a few sent replies when a customer complains."

- **Change.**
  - Build 20 to 50 cases from past complaints and put the tone rules from the prompt into deterministic checks. Examples are no "we will refund", a tracking link on late orders, the sign-off, and exactly one send.
  - Run them with a fake client or tool registry in `make test`, plus a live variant for prompt changes.
  - Keep the three existing assertions as the seed cases.
- **Why.**
  - Wiki page: [Upgrading an existing AI app, checks 1 to 3](https://mishaevoma.github.io/aie-brain/playbooks/upgrading-an-agent-app.md).
  - Source note: [Demystifying evals, Jan 2026](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md).
  - Original: https://www.anthropic.com/research/demystifying-evals-for-ai-agents.
  - The prompt comment at `agent.py:27` says it has been "tweaked a few times" since October with nothing that reruns. The playbook treats that as the pattern a broad suite guards against ([Claude Code postmortem, Apr 2026](https://mishaevoma.github.io/aie-brain/sources/2026-04-23-anthropic-claude-code-quality-postmortem.md), original https://www.anthropic.com/research/april-23-postmortem).
- **Check.**
  - Shows the problem today. I ran `python3 -B -m unittest discover -s tests -v`, which printed `Ran 5 tests ... OK (skipped=4)`.
  - Passes after the fix, and I have not run this one. The same command should show the new offline cases running, not skipped.
- **Evidence.** Published Jan 2026 and Apr 2026, so both are current. Anthropic's own figures were measured on Claude Code and its models, not on this app.
- **Effort and impact.** Medium, about a day to collect and label cases. It tells you whether any later change helped or hurt.

**Upgrade 3: Stop pasting the entire email history and the whole knowledge base into every call.** `context.py:21-22` includes "Every email this customer has sent us" plus all of `kb/*.md`. It is unbounded by customer, and it is fetched before the model runs. The model already has `lookup_order` to pull specifics on demand.

- **Change.**
  - Limit the history to the last few emails, or only ones that mention the order or topic.
  - Load the knowledge-base file that matches the topic instead of all of them.
  - Measure the effect with the Upgrade 2 cases before and after.
- **Why.**
  - Wiki page: [Upgrading an existing AI app, check 4](https://mishaevoma.github.io/aie-brain/playbooks/upgrading-an-agent-app.md).
  - Source note: [Context rot, Jul 2025](https://mishaevoma.github.io/aie-brain/sources/2025-07-14-chroma-context-rot.md).
  - Original: https://www.trychroma.com/research/context-rot.
  - Stale or look-alike records, such as old late-order emails, hurt more than neutral filler.
- **Check.**
  - Shows the problem today. Reading `context.py:21-22` shows an unbounded join. I did not run it, because it needs the internal shop API.
  - Passes after the fix, and I have not run this one. A test with a 200-email fake history should show a bounded prompt length.
- **Evidence.** Published Jul 2025, about 16 months ago, so it is older than the 12-month window. I'd call it older, still valid, but I didn't check this page's `status` or `reviewed:` date, so I can't say which condition applies. Chroma measured several vendors' models, not this app's.
- **Effort and impact.** Small to medium. It means lower token cost per email and less chance that an old email misleads the reply.

**Upgrade 4: Break the lethal trifecta, or put a gate before `send_reply`.** This app has all three parts of what Willison calls the lethal trifecta. Untrusted customer text goes into the prompt (`agent.py:35`). Private data is in the context (order history, other emails). And `send_reply` takes a free-form `to` argument (`tools.py:15-22`) that the model fills in. A crafted email could steer a reply, or a copy of private data, to an address you didn't intend.

- **Change.**
  - Remove the model's control over the recipient. Have code set `to` from `email["from"]` and ignore the model's value.
  - Optionally hold replies for human approval when the model has called anything unusual.
- **Why.**
  - Wiki page: [Upgrading an existing AI app, check 10](https://mishaevoma.github.io/aie-brain/playbooks/upgrading-an-agent-app.md).
  - Source note: [Lethal trifecta, Jun 2025](https://mishaevoma.github.io/aie-brain/sources/2025-06-16-willison-lethal-trifecta.md).
  - Original: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/.
- **Check.**
  - Shows the problem today. Reading `tools.py:31` shows `to` is a model-supplied parameter.
  - Passes after the fix, and I have not run this one. A test where the model asks to send to another address should assert the mail goes to the sender.
- **Evidence.** Published Jun 2025, so it is older than the 12-month window. The idea is a threat model, not a measurement. I didn't check this page's `status` or `reviewed:` date either, so I'm labelling it older, still valid on that basis only.
- **Effort and impact.** Small. It closes a data-exfiltration path.

I did not report two things. The prompt has no obvious problem to fix. And the three retry/step-limit details I saw (8-step cap, timeouts) are sound.

Reply "make upgrade 1 and run the check" and I'll do it. Until then I change nothing.
For repeat reviews, install the skill in the project: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
Provenance: wiki revision `9b70bc0 2026-11-19` (from the published `revision.txt`), read on the public site on 2026-11-19. I read one playbook page and six source-note headers; I did not read the concept pages. The ranking and the verdict that nothing else is worth reporting are my own judgment.

## Run notes (for the tester)

1. Fetches, in order:
   1. WebFetch, https://mishaevoma.github.io/aie-brain/review.md. This returned a model-written summary, not the raw file.
   2. Bash curl, https://mishaevoma.github.io/aie-brain/review.md. Raw file text.
   3. Bash curl, https://raw.githubusercontent.com/mishaevoma/aie-brain/main/.agents/skills/brain-consult/references/project-review.md. Raw text.
   4. Bash curl, https://mishaevoma.github.io/aie-brain/playbooks/upgrading-an-agent-app.md. Raw text.
   5. Bash curl, https://mishaevoma.github.io/aie-brain/revision.txt. Raw text.
   6. Bash curl, six source notes under https://mishaevoma.github.io/aie-brain/sources/, header lines only (via `head`). Raw text.
2. Questions I needed to ask first: none.
3. Elapsed between the first and last timestamp: 26 seconds. The whole subagent run took 55 seconds.
4. Final `git status --porcelain --untracked-files=all --ignored` printed nothing. I created and deleted no file in the project. I ran the tests with `python3 -B` and `PYTHONDONTWRITEBYTECODE=1`.
