The project needs three upgrades: a reliable stopping rule, direct access to PR facts when writing and reviewing, and tests that measure release-note accuracy.

I reviewed all four tracked files using the local brain wiki. Both existing tests pass. No files changed or live model calls made. I treated this as a small weekly batch tool; the README’s latency, cost, and incorrect announcement are reported incidents, not measurements I reproduced.

**Upgrade 1: Bound the review loop and reject false approvals.**

In `crew.py:37–42`, the loop can continue indefinitely, and `"APPROVED" in verdict` accepts **“NOT APPROVED.”**

- **Change:** Require an exact approval value, cap critic rounds—for example, three—and return an explicit failure when exhausted. Keep client injection and the existing retry test.
- **Why and evidence:** The wiki’s [verification guidance](https://mishaevoma.github.io/aie-brain/concepts/verification.md) recommends bounded correction rounds, citing [Osmani’s source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-17-osmani-claude-code-team-verification.md) and [original publication](https://x.com/addyosmani/status/2122590683055993308), **17 November 2026, two days old**. This is one team’s practice; the exact approval check is my code-level fix.
- **Check run:**

  ```sh
  python3 -B -c 'import crew; from test_crew import ScriptedClient; c=ScriptedClient(["NOT APPROVED"]); print(crew.run([], c))'
  ```

  It returned release notes. A separate bounded fake-client probe consumed six rejections and attempted a seventh critic call; only the fake’s exhausted response list stopped it.
- **After-change check:** Add tests asserting that `NOT APPROVED` cannot finish successfully and an always-rejecting critic stops after the configured limit. These tests are proposed, not run.
- **Effort and impact:** Small. Prevents false acceptance and unlimited rewrite costs. A round cap alone does not bound an individual API request’s duration.

**Upgrade 2: Give the writer and critic the original PRs; simplify the fixed chain.**

In `crew.py:28–42`, the planner cannot change execution order. The writer receives only the researcher’s summary, and the critic receives only the draft. Neither can reliably recover a removal that the summary misrepresents.

- **Change:** First pass original PR records to both writer and critic, including during rewrites. Keep PR numbers, labels, and bodies. Then benchmark a direct PR-to-writer path with bounded review against the current chain; remove planner/researcher calls if accuracy holds. Send only original records, the current draft, and current feedback during revisions.
- **Why and evidence:** [Agents and workflows](https://mishaevoma.github.io/aie-brain/concepts/agents-and-workflows.md) supports simpler generation paths; [Theo’s source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-09-theo-harness-difference-approaching-zero.md), [original](https://x.com/theo/status/2119692972233281688), is dated **9 November 2026, ten days old**. It is practitioner opinion, not comparative evidence for this project. Preserving original evidence follows [Osmani’s note](https://mishaevoma.github.io/aie-brain/sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md), [original](https://x.com/addyosmani/status/2117512471930167377), **3 November, sixteen days old**.
- **Check run:**

  ```sh
  python3 -B -c 'import crew,json; from test_crew import ScriptedClient; c=ScriptedClient(["APPROVED"]); crew.run(json.load(open("prs.json")),c); print(len(c.calls), ["/v1/export" in x["messages"][0]["content"] for x in c.calls])'
  ```

  Output: `4 [True, True, False, False]`—four calls; only planner and researcher receive the endpoint.
- **After-change check:** Assert original PR facts reach every writer/critic call, including revisions. Compare factual accuracy, token cost, and elapsed time across both designs before removing stages. Not run.
- **Effort and impact:** Small context fix; modest comparison work. Addresses the observed information loss. Removing two calls would reduce call count, but actual savings remain unmeasured.

**Upgrade 3: Turn the export-removal incident into a quality evaluation.**

`test_crew.py` always makes the writer return “Faster dashboard.” The tests prove orchestration works, while allowing the breaking change to disappear.

- **Change:** Keep those unit tests. Add a separately runnable evaluation using `prs.json`, then expand with historical failures. Require removal of `/v1/export`, migration to `/v2/reports`, accurate performance and import fixes, and no invented export launch. Include both acceptable and incorrect examples to validate the grader.
- **Why and evidence:** [Evals](https://mishaevoma.github.io/aie-brain/concepts/evals.md) recommends grading outcomes from real failures. [Anthropic’s source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), [original publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), is dated **9 January 2026, about ten months old**. Starting with this one incident is my project-specific adaptation.
- **Check run:**

  ```sh
  python3 -B -m unittest -v
  ```

  Output: `Ran 2 tests … OK`. Neither test evaluates factual release-note quality.
- **After-change check:** The grader must reject “new export API” and missing migration guidance, accept a correct reference, and score repeated real-model runs. Report accuracy alongside cost and latency. Not run.
- **Effort and impact:** Modest initial work plus evaluation API costs. Makes simplification and prompt changes assessable before customers encounter mistakes.

Reply **“make upgrade 1 and run the check”** to implement the first fix.

For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.

Provenance: local wiki revision **`fe44a47` (2026-11-19)**, consulted **2026-11-19**. Original publications were linked from the source notes; live model behavior remains unverified.
