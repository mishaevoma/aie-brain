**Validate category output first so tickets cannot silently miss every category queue.** I traced `add → tag_ticket → SQLite → list --category` and reproduced that failure using a mock model response.

1. **Invalid model output is saved as a category.** At [app/tagging.py:25](app/tagging.py#L25), the response is only stripped and lowercased. A simulated reply of `billing: duplicate charge` produced one saved ticket visible in **none** of the four category queues.

   My recommendation: validate against `CATEGORIES` before storage and give staff an explicit recovery path for invalid or empty responses. This applies the Brain’s [output sanity-check guidance](https://mishaevoma.github.io/aie-brain/concepts/production-operations.md), supported by its [Anthropic source note, September 17, 2025](https://mishaevoma.github.io/aie-brain/sources/2025-09-17-anthropic-postmortem-three-issues.md).

   **Proposed check:** mock invalid text and empty content; verify neither creates an unreachable ticket.

2. **Classification failure prevents ticket creation.** At [app/cli.py:21](app/cli.py#L21), classification runs before insertion. A simulated timeout escaped the CLI and left the new ticket unsaved.

   My recommendation for this small helpdesk: provide a manual `--category` option that bypasses classification, and catch provider failures with a useful recovery message. The Brain does not prescribe this exact fallback; this is a project-specific design judgment.

   **Proposed check:** simulate a provider failure, then verify manual categorization saves exactly one ticket without calling the model.

3. **Classification accuracy is unverified despite existing labeled data.** [tests/test_tagging.py](tests/test_tagging.py) checks canned responses and normalization. Nothing evaluates the 40 examples in [data/labelled_tickets.csv](data/labelled_tickets.csv).

   Add a small evaluation runner using the actual `tag_ticket` path, exact category matching, per-category results, and a list of disagreements for the support lead. Record the model and prompt version. This follows the Brain’s [eval guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md) and [Anthropic source note, January 9, 2026](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md).

   **Proposed check:** evaluate all 40 rows and establish a reviewed baseline before changing the prompt or model.

Keep the single-call design: it fits this bounded classification task and aligns with [Anthropic’s simplicity guidance, December 19, 2024](https://mishaevoma.github.io/aie-brain/sources/2024-12-19-anthropic-building-effective-agents.md). These dated sources support general engineering practices, not current model-performance claims.

**Verified:** all five existing tests passed; the two failure reproductions used mocks and in-memory SQLite. No project files changed or live model calls made, so model availability and actual accuracy remain unverified.

*Provenance: public Brain wiki and linked review procedure, consulted November 19, 2026.*
