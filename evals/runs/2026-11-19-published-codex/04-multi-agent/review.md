The project needs four upgrades. **The most urgent bug is that “NOT APPROVED” is treated as approval.** Both existing tests pass, but neither checks factual accuracy.

I reviewed all four tracked files using the published brain-consult procedure. No files changed, and no live API calls ran. I treated this as a weekly CLI used to prepare customer-facing notes.

**Upgrade 1: Make the approval gate reject negative verdicts.**

- **Change:** In `crew.py:40`, replace substring matching with `verdict.strip() == "APPROVED"`, or validate a structured verdict. Keep the injectable client for regression tests.
- **Check — ran:**
  ```sh
  python3 -B -c 'import crew; from test_crew import ScriptedClient; print(crew.run([], ScriptedClient(["NOT APPROVED"])))'
  ```
  It prints release notes. Add a test with `["NOT APPROVED", "APPROVED"]`; after the fix, it must require two critic calls.
- **Why and evidence:** The wiki recommends checks that resist false success: [verification](https://mishaevoma.github.io/aie-brain/concepts/verification.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-17-osmani-claude-code-team-verification.md), [original](https://x.com/addyosmani/status/2122590683055993308). Published **17 November 2026, two days old**. The exact parser fix is my code-level judgment.
- **Effort and impact:** Small; prevents explicitly rejected notes from being returned as successful output.

**Upgrade 2: Bound the revision loop.**

- **Change:** Replace `while True` at `crew.py:37` with a configurable round limit. On exhaustion, raise a clear error requiring review. Keep the feedback-and-rewrite path within that limit.
- **Check — ran:**
  ```sh
  python3 -B -c 'import crew; from test_crew import ScriptedClient; crew.run([], ScriptedClient(["Fix it"] * 10))'
  ```
  It requests an eleventh critic response and stops only because the fake client raises `IndexError`. Add a test asserting a deliberate exhaustion error after, for example, three review rounds.
- **Why and evidence:** [Verification](https://mishaevoma.github.io/aie-brain/concepts/verification.md) recommends capped correction rounds with human escalation: [17 November source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-17-osmani-claude-code-team-verification.md), [original](https://x.com/addyosmani/status/2122590683055993308). **Two days old**; three rounds is one team’s practice, not a universal optimum.
- **Effort and impact:** Small; bounds model-call count and prevents endless revision. It does not itself bound individual API-call duration.

**Upgrade 3: Give the writer and critic original evidence; simplify the chain.**

The planner cannot change the execution path. The writer receives only the research summary; the critic receives only the draft. Neither can reliably detect a summary that reverses “removed endpoint” into “new API.”

- **Change:** At `crew.py:28–42`, use the original PR records directly for drafting and review. A sensible baseline is one writer plus an optional bounded critic. For revisions, send the PRs, current draft and latest feedback instead of every previous draft. Keep the existing direct API wrapper.
- **Check — ran:**
  ```sh
  python3 -B -c 'import crew,json; from test_crew import ScriptedClient; c=ScriptedClient(["APPROVED"]); crew.run(json.load(open("prs.json")),c); print([(x["system"].split(".")[0], "/v1/export" in x["messages"][0]["content"]) for x in c.calls])'
  ```
  Planner and researcher print `True`; writer and critic print `False`. Afterward, both drafting and review inputs should contain the original removal and migration facts.
- **Why and evidence:** [Agents and workflows](https://mishaevoma.github.io/aie-brain/concepts/agents-and-workflows.md) recommends starting simple: [source note](https://mishaevoma.github.io/aie-brain/sources/2024-12-19-anthropic-building-effective-agents.md), [original](https://www.anthropic.com/research/building-effective-agents). Published **19 December 2024, 23 months old — older, still valid:** the concept is marked settled and reviewed 17 November 2026. Avoiding summaries of summaries is also supported by the [3 November 2026 note](https://mishaevoma.github.io/aie-brain/sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md) and [original](https://x.com/addyosmani/status/2117512471930167377), **16 days old**.
- **Effort and impact:** Moderate; restores access to evidence and removes two initial calls. Quality and monetary savings still need measurement.

**Upgrade 4: Test release-note correctness, not just role sequencing.**

- **Change:** Extend `test_crew.py` with regression checks above, and add a small real-model evaluation using `prs.json`. Keep the fast scripted tests for orchestration.
- **Check — ran:** `python3 -B -m unittest -v` → **2 tests passed**. The fake writer always returns “Faster dashboard,” so these tests cannot catch the documented export hallucination.
  
  Proposed evaluation criteria: state that `/v1/export` was removed; identify `/v2/reports` as the migration path; cover the dashboard improvement and pre-1970 import fix; omit the internal eslint update; invent no new export API. Include a deliberately incorrect draft to verify that the grader rejects it. These evaluations were **not run**.
- **Why and evidence:** [Evals](https://mishaevoma.github.io/aie-brain/concepts/evals.md), [Anthropic source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), [original](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Published **9 January 2026, about ten months old**. The page marks the field evolving; this project already has a concrete incident to turn into a regression case.
- **Effort and impact:** Moderate; establishes whether simplification or prompt changes actually improve accuracy. Record latency, tokens and repeated-run success alongside quality.

Reply **“make upgrade 1 and run the check”** to implement the first fix.
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
Provenance: published wiki revision **`9b70bc0 2026-11-19`**, consulted **19 November 2026**; live model availability, quality and reported costs remain unverified.
