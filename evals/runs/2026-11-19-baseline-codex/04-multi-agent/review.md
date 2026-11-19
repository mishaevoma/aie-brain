**First, fix the approval check and cap revisions so rejected release notes cannot be returned as approved or loop indefinitely.** I traced `prs.json → planner → researcher → writer → critic → stdout`; simulated responses demonstrated both failures.

1. **High: a rejection can pass the approval gate.** In [crew.py:40](<work>/04-multi-agent/crew.py:40), substring matching accepts `NOT APPROVED: missing breaking change.` I reproduced this: the run returned notes after four calls. Require an exact normalized `APPROVED` response, or validate a structured verdict.

   **Proposed check:** feed `NOT APPROVED`, `DISAPPROVED`, and an explicit approval; only the last may return notes.

2. **High: revision attempts have no stopping condition.** The loop at [crew.py:37](<work>/04-multi-agent/crew.py:37) continues while accumulating every draft and critique. Ten simulated rejections triggered an eleventh review attempt; only exhaustion of the fake responses stopped it. This mechanism is consistent with the README’s reported hangs, though those runs were unavailable. Add a revision cap and an explicit failure exit; send only the source, latest draft, and latest feedback on retries.

   **Proposed check:** an always-rejecting client must terminate within the configured call budget without emitting approved notes.

   These changes follow the wiki’s [workflow guidance](https://mishaevoma.github.io/aie-brain/concepts/agents-and-workflows.md) and [Anthropic, December 19, 2024](https://mishaevoma.github.io/aie-brain/sources/2024-12-19-anthropic-building-effective-agents.md): define completion criteria and hard stopping conditions.

3. **High: factual review has no access to the facts.** At [crew.py:34](<work>/04-multi-agent/crew.py:34), the writer receives only a short research summary; the critic receives only the draft. Neither can reliably recover a removal misrepresented upstream as an addition. Pass original PR records to both, and require factual coverage and breaking-change checks. Keep the injectable client—it makes these boundaries easy to test.

   **Proposed check:** use `prs.json` as a regression case: identify `/v1/export` as removed, retain migration to `/v2/reports`, and reject an invented “new export API.” Existing tests check canned responses and call counts, so they cannot establish factual quality. This follows [eval guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md) and [Anthropic, January 9, 2026](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md).

4. **Medium: four roles lack demonstrated value here.** [crew.py:28](<work>/04-multi-agent/crew.py:28) starts a fixed sequential workflow; the planner does not control execution. My recommendation is to benchmark one writer given the original PRs, optionally followed by one grounded review, before retaining all four roles.

   **Proposed check:** compare factual errors, breaking-change coverage, latency, and token cost on identical historical weeks. The [multi-agent guidance](https://mishaevoma.github.io/aie-brain/concepts/multi-agent-systems.md) favors separable work; [Anthropic’s June 13, 2025 research system](https://mishaevoma.github.io/aie-brain/sources/2025-06-13-anthropic-multi-agent-research-system.md) studied parallel research with Claude 4 models, not this release-note workflow.

Both existing unit tests passed. No files were changed or live model calls made; model availability and real output quality remain unverified.

Provenance: published AI Engineering Brain consulted November 19, 2026. The cited foundational sources are over six months old; architecture benefits require measurement in this project.
