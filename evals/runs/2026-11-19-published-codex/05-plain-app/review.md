Two upgrades are worth making: validate categories before saving tickets, and turn the 40 labelled tickets into a quality check. All five existing tests pass. No project files were changed.

I treated this as a small internal helpdesk, as described in the README, and followed the published Brain review procedure.

**Upgrade 1: Prevent unexpected model replies from hiding tickets from category lists.**

- **Observed:** [app/tagging.py:25](app/tagging.py#L25) returns arbitrary model text after normalization. The CLI saves it, but only accepts four predefined categories when filtering. An in-memory CLI check with a mocked reply of `billing.` produced:
  ```text
  #1 [billing.]
  all tickets: 1
  billing tickets: 0
  ```
- **Change:** Validate the reply against `CATEGORIES` before insertion and return an actionable error for invalid or empty responses. Keep the existing normalization and injectable client.
- **Why:** The Brain’s [tool-design guidance](https://mishaevoma.github.io/aie-brain/concepts/tool-design.md) puts deterministic code between model output and action. Applying that boundary to classification is my inference. Its [dated source note](https://mishaevoma.github.io/aie-brain/sources/2025-03-30-humanlayer-12-factor-agents.md) links to [12-Factor Agents](https://github.com/humanlayer/12-factor-agents), published March 30, 2025—about 20 months old. **Older, still valid:** the concept is marked settled and reviewed November 17, 2026.
- **Check:** Add a CLI regression test using an in-memory database: `billing.` must produce a controlled error and no insert; `billing` must appear in the billing list. Run `python3 -B -m unittest discover -s tests -v`. I ran the existing suite and reproduction; the proposed regression test does not yet exist.
- **Effort and impact:** Small change; prevents silently unroutable tickets.

**Upgrade 2: Measure classification quality using the existing labelled dataset.**

- **Observed:** [tests/test_tagging.py:7](tests/test_tagging.py#L7) supplies canned answers. These tests prove normalization, not classification accuracy or provider compatibility. The 40 rows in `data/labelled_tickets.csv` are unused by code or tests.
- **Change:** Add a small evaluation runner that calls `tag_ticket` on those rows and reports exact-match accuracy, per-category failures, invalid outputs and API errors. Record the model and prompt alongside results; rerun before changing either. Keep the fast offline unit tests.
- **Why:** The Brain’s [eval guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md), its [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), and [Anthropic’s original article](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) recommend starting with a few dozen real cases and deterministic grading. Published January 9, 2026—about ten months old. The wiki marks this topic evolving; here, existing human-labelled examples make a small evaluation practical.
- **Check:** I ran:
  ```sh
  rg -n 'labelled_tickets|client_replying' app tests README.md
  ```
  Dataset references appeared only in README; both classifier tests use the mock. After implementation, a proposed `python3 -B -m app.eval_tagging` should score all 40 rows and fail when the agreed quality threshold is missed. That command does not exist yet.
- **Effort and impact:** A few hours plus 40 model calls per run; makes prompt/model regressions visible before staff encounter them.

Keep the simple single-call design. Live API behavior, the configured model’s availability, and classification accuracy remain unverified; no customer data was sent to a provider.

Reply **“make upgrade 1 and run the check”** to implement the first change.
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
Provenance: published wiki revision `9b70bc0` (2026-11-19), consulted November 19, 2026.
